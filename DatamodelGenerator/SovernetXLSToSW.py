
import XLSToSWFieldManager
import XLSToSWUnitTestGenerator
import XLSToSWField
import XLSToSWExceptions
import MagikCodeWriter
import xlrd
import operator

SSHEETCOLUMN_FOREIGNTABLENAME = 2
SSHEETCOLUMN_FOREIGNATTRIBUTENAME = 4
SSHEETCOLUMN_FOREIGNGROUP = 7
SSHEETCOLUMN_MAPFIELD_P = 9
SSHEETCOLUMN_PNITABLENAME = 10
SSHEETCOLUMN_PNITABLEEXTERNALNAME = 26
SSHEETCOLUMN_PNIATTRIBUTENAME = 11
SSHEETCOLUMN_PNIATTRIBUTETYPE = 13
SSHEETCOLUMN_PNIATTRIBUTEDEFAULTVALUE = 12
SSHEETCOLUMN_PNIATTRIBUTELENGTH = 14
SSHEETCOLUMN_PNIATTRIBUTEPRIORITY = 28
SSHEETCOLUMN_FEATUREPOINTDESCRIPTION = 25
SSHEETCOLUMN_PNIJOINTYPE = 29
SSHEETCOLUMN_PNIJOINTO = 28
SSHEETSTARTTABNO = 3
SSHEETENDTABNO = 16


class SovernetXLSToSW():

    s_filename='not set'
    s_workbook='not set'
    s_show_features_p=True
    s_magikcodewriter='not set'
#    s_base_folder='/home/glennx/Dropbox/Sovernet/'
    s_base_folder='e:/data/Custom Datamodel Builder/'
    s_code_folder='C:/Users/Glenn.Nicholls/Documents/CogecoDataReaders/DatamodelGenerator/'
    
     
    s_fieldmanager=XLSToSWFieldManager.XLSToSWFieldManager()

    def __init__(self):
        self.s_magikcodewriter = MagikCodeWriter.MagikCodeWriter()
        

    def sheetIsACoaxSheet (self, pSheetNumber):
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        lValue = lsheet.cell_value(2, SSHEETCOLUMN_FOREIGNGROUP)
        return lValue.lower()=='coax'

    def buildSWFieldComment(self, pSheet, pRow):
        lText=pSheet.cell_value (pRow, 0)
        lText=lText + ':'
        lText=lText + pSheet.cell_value (pRow, SSHEETCOLUMN_FOREIGNTABLENAME)
        lText=lText + ':'
        lText=lText + pSheet.cell_value (pRow, SSHEETCOLUMN_FOREIGNATTRIBUTENAME)
        return lText
    

    def buildSWField (self, pSheet, pRow):
        lUsed = pSheet.cell_value(pRow,SSHEETCOLUMN_MAPFIELD_P)
        if operator.or_(lUsed.lower()=='no', lUsed.lower()=='no-temporary'):
            raise XLSToSWExceptions.FieldNotMapped(repr(pSheet) + ':' + repr(pRow))

        lFieldDefaultValue=''
        lClassName = pSheet.cell_value(pRow,SSHEETCOLUMN_PNITABLENAME)
        lFieldName = pSheet.cell_value(pRow, SSHEETCOLUMN_PNIATTRIBUTENAME)
        lFieldExternalName = pSheet.cell_value(pRow,SSHEETCOLUMN_PNITABLEEXTERNALNAME)
        lFieldType = pSheet.cell_value(pRow,SSHEETCOLUMN_PNIATTRIBUTETYPE)
        lFieldDefaultValue = pSheet.cell_value(pRow, SSHEETCOLUMN_PNIATTRIBUTEDEFAULTVALUE)
        lFieldLength = pSheet.cell_value(pRow,SSHEETCOLUMN_PNIATTRIBUTELENGTH)
        # lFieldPriority = pSheet.cell_value(pRow,SSHEETCOLUMN_PNIATTRIBUTEPRIORITY)
        lFieldPriority = 10
        lFieldText = self.buildSWFieldComment(pSheet, pRow)

        lFeaturePoint=pSheet.cell_value(pRow,SSHEETCOLUMN_FEATUREPOINTDESCRIPTION)
        if operator.and_(lFeaturePoint!="", self.s_show_features_p==True):
            print ("----------Feature " + lFeaturePoint)

        lField = XLSToSWField.XLSToSWField(lClassName, lFieldName, lFieldType)
        lField.s_field_external_name = lFieldExternalName
        if lFieldLength!='':
            lField.s_field_length = lFieldLength
        if lFieldPriority!='':
            lField.s_field_priority=lFieldPriority
        if lFieldText!='':
            lField.s_field_comment=lFieldText
        if lFieldDefaultValue!='':
            lField.s_field_default_value=lFieldDefaultValue
        if lField.fieldType().lower() == "join":
            lField.s_field_join_type=pSheet.cell_value(pRow,SSHEETCOLUMN_PNIJOINTYPE)
            lField.s_field_join_to  =pSheet.cell_value(pRow,SSHEETCOLUMN_PNIJOINTO)
            print ("is a valid join " + repr(lField.isValidJoin()))
            if lField.isValidJoin()==False:
                print ("found an invalid join ")
            
        # lField.showMe()
        return lField

    def fieldManager(self):
        return self.s_fieldmanager

    def resetFieldManager(self):
        self.s_fieldmanager=XLSToSWFieldManager.XLSToSWFieldManager()

    def parseDynamicEnumeratorsSheet(self, pSheetNumber):
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        lenumerators=[]
        try:
            for iRow in range(2, 11):
                lEnumeratorName=lsheet.cell_value(iRow, 0)
                lEnumeratorValues=lsheet.cell_value(iRow, 1)
                lEnumeratorDefault=lsheet.cell_value(iRow, 2)
                lenumerators.append ([lEnumeratorName, lEnumeratorValues, lEnumeratorDefault])

        except IndexError:
            lblankcode= 0   #print("index error went off")

        return lenumerators


    def getVersion(self):
        lsheet = self.s_workbook.sheet_by_index(2)
        lversion = lsheet.cell_value(0, 1)
        print ("version = " + lversion)

        return lversion
    
        

    def parseExternalNamesSheet(self, pSheetNumber):
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        lexternalnames=[]
        try:
            for iRow in range(3, 38):
                lInternalName=lsheet.cell_value(iRow, 0)
                lPNIExternalName=lsheet.cell_value(iRow, 1)
                lCustomExternalName=lsheet.cell_value(iRow, 2)
                lexternalnames.append ([lInternalName, lPNIExternalName, lCustomExternalName])

                

        except IndexError:
            lblankcode= 0   #print("index error went off")

        return lexternalnames

        
                
    def writeEnumCallingLine(self, pEnum, pFD):
        lEnumValues=pEnum[1].split(',')
        lEnumValuesStr = '{'
        lCtr=0
        for ienumvalue in lEnumValues:
            if lCtr>0:
                lEnumValuesStr+=','
            lEnumValuesStr = lEnumValuesStr + '"' + ienumvalue + '"'
            lCtr=+1

        lEnumValuesStr+='}'
        if pEnum[0].find('sov')==-1:
            pFD.write('#')
        pFD.write ("custom_upgrade_enums(l_make_changes?, p_case_name, " + '"' + pEnum[0] + '"' + ',' + lEnumValuesStr + ',' + '"' + pEnum[2] + '"' + ")\n")
        
    def parseSheet(self, pSheetNumber=0):

        if self.sheetIsACoaxSheet(pSheetNumber):
            raise XLSToSWExceptions.SheetIsCoax(pSheetNumber)
            
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        # try:
        for iRow in range(2, 130):
            try:
                lField=self.buildSWField (lsheet, iRow)
                self.s_fieldmanager.addField(lField)
                
            except XLSToSWExceptions.FieldNotMapped:
                    # print ('field not mapped went off')
                    lblankcode =0
            except XLSToSWExceptions.InvalidDSType:
                    print ('Invalid ds type in sheet ' + lsheet.name + ' line ' + repr (iRow))
                    lField.showMe()
            

            except IndexError:
                # print ('indexerror went off')
                lblankcode= 0
            
    def writeCaseCallingLines (self, pCallingTexts, pCustomOnly, pFD):
        for iCallingText in pCallingTexts:
            if operator.and_ (pCustomOnly==True, iCallingText.find("_sovernet")!=-1):
                pFD.write (iCallingText + "(l_make_changes?, p_case_name)\n")
            if operator.and_ (pCustomOnly==False, iCallingText.find("_sovernet")==-1):
                pFD.write (iCallingText + "(l_make_changes?, p_case_name)\n")

    def writeCasePreamble(self, pFD):
        lFIn = open (self.s_code_folder + 'CasePreamble.txt', 'r')
        for iline in lFIn:
            pFD.write(iline)
#        lFIn = open (self.s_code_folder + 'CogeoCasePreamble.txt', 'r')
#        for iline in lFIn:
#            pFD.write(iline)

    def writeManualUpdatesToEnums(self, pFD):
        lFIn = open (self.s_code_folder +'SovernetManualUpdatesToEnums.txt', 'r')
        for iline in lFIn:
            pFD.write(iline)

    def writeEnumUsages(self, pFD):
        pFD.write ("_global custom_make_enum_usages<<\n")
        pFD.write ("_proc(p_make_changes?)\n")
        for iClassName in self.fieldManager().classesManaged():
            for iField in self.fieldManager().findFieldsForClass(iClassName):
                if iField.isEnumField():
                    	pFD.write ('custom_make_enum_use (' + ':' + iField.fieldType() + ',' + ':' + iField.className() + ',' + ':' + iField.fieldName() + ',p_make_changes?)\n')
        pFD.write ("gis_program_manager.cached_dataset(:dynamic_enumerator).commit()\n")            	
        pFD.write ("_endproc\n")


    def writeCaseField (self, pClassName, pField, pFD):

        if pField.isValidJoin():
            return

        if pField.isIDField():
            pFD.write("custom_make_id_field(o, l_make_changes?)\n")
            return
        
        if pField.isPNIField():
            if pField.isStringType():
                pFD.write("custom_update_length_of_pni_field(o, " + "'" + pField.fieldName() + "'" + ", " + repr(pField.fieldLength()) + ",  p_make_changes?)\n")
            else:
                pFD.write("# Using PNI field " + pClassName + "." + pField.fieldName() + "\n")
            return 

        if pField.isPhysicalField():
            pFD.write ("custom_make_physical_field(o, :" + pField.fieldName() + ", " + '"' + pField.fieldExternalName() + '"' + ", :" + pField.fieldType() + ", l_make_changes?, " + pField.convertToString() + "," + "'" + pField.fieldComment() + "'" + ")\n")
            return
        
        if pField.isGeometryField():
            pFD.write ("custom_make_geometry_field(o, :" + pField.fieldName() + ", " + '"' + pField.fieldExternalName() + '"' + ", :" + pField.fieldType() + ", l_make_changes?, " + "(" + repr(pField.fieldPriority()) + ")" + ".floor" + ")\n")
            return

        if pField.fieldDefaultValue!='':   
            pFD.write ('custom_make_enum_field (o, ' + ':' + pField.fieldName() + ',' + '"' + pField.fieldExternalName() + '"' + ',' + ':' + pField.fieldType() + ',' + 'l_make_changes?' + ',' + '"' + pField.fieldDefaultValue() + '"' + ')\n')
        else:
            pFD.write ('custom_make_enum_field (o, ' + ':' + pField.fieldName() + ',' + '"' + pField.fieldExternalName() + '"' + ',' + ':' + pField.fieldType() + ',' + 'l_make_changes?)\n')


    def writeCaseObjectTail (self, pFD):
        pFD.write ("_endproc\n")
        pFD.write ("$\n")

    def writeCaseDefinition (self, pClassName, pFD, pX=12000, pY=12000):

        lCallingText = self.s_magikcodewriter.writeCaseObjectHeader(pClassName, pFD, pX, pY)
        lFields = self.fieldManager().findFieldsForClass(pClassName)
        if (len(lFields)==0):
            raise XLSToSWExceptions.ClassNotManaged (pClassName)
    
        for iField in lFields:
            self.writeCaseField(pClassName, iField, pFD)
                
        self.writeCaseObjectTail(pFD)
        
        return lCallingText

    def writeObjectSelectLine(self, pObjectName, pFD):
        pFD.write ("lSelectCaseObject(" + "'" + pObjectName + "'" + "," + "l_case_name"+ ")\n")
            
            
        

    def processMainDBWorkBook (self, pFileName):

        self.s_filename=self.s_base_folder + pFileName
        self.s_workbook=xlrd.open_workbook(self.s_filename)
        
        lEnumerators = []
    
        lEnumerators = self.parseDynamicEnumeratorsSheet(1)
        lExternalNames = self.parseExternalNamesSheet(2)
        lVersion = self.getVersion()
        
        for iSheetNumber in range (SSHEETSTARTTABNO, SSHEETENDTABNO):
            try:
                lsheet = self.s_workbook.sheet_by_index(iSheetNumber)
                print ('sheet ' + repr(lsheet.name))
                self.parseSheet(iSheetNumber)
               
                    
            except XLSToSWExceptions.SheetIsCoax:
                lblankcode = 0  # print ('sheet is a coax sheet' + repr(iSheetNumber))

        

        lClassesManaged=self.fieldManager().classesManaged()
        self.fieldManager().showClassesManaged()

        lCallingLines=[]
        
        with open(self.s_base_folder + 'case_upgrade.magik', 'w') as lFD:

            lFD.write ("# Custom Case Upgrade for " + lVersion + "\n")
            
            self.writeCasePreamble(lFD)
            self.writeManualUpdatesToEnums(lFD)

            self.writeEnumUsages(lFD)
            
            for iClass in lClassesManaged:
                lCallingLines.append(self.writeCaseDefinition(iClass, lFD))

            self.s_magikcodewriter.writeMakeJoinsMagikCodePreamble(lFD)
            
            for iJoinField in self.fieldManager().joinFields():
                lFD.write ('make_a_join (p_case_view, ' + '"' + iJoinField.s_field_join_type + '"' + ',' + ':' + iJoinField.className() + ',' + ':' + iJoinField.s_field_join_to + ', p_make_changes?)\n')

            self.s_magikcodewriter.writeEndProcandDollar(lFD)
   
            self.s_magikcodewriter.writeMakeCaseSelectMagikCodePreamble(lFD)
                
            for iClass in lClassesManaged:
                self.writeObjectSelectLine(iClass, lFD)
                
            lFD.write ("lSelectCaseObject(" + "'" + "mit_cable" + "'" + "," + "l_case_name"+ ")\n")            
            self.s_magikcodewriter.writeEndProcandDollar(lFD)

            self.s_magikcodewriter.writeCaseUpgradeMagikCodePreamble(lFD)
        
            for iEnum in lEnumerators:
                self.writeEnumCallingLine(iEnum, lFD)

            
            lFD.write ("custom_make_enum_usages(l_make_changes?)\n")
            
            self.writeCaseCallingLines(lCallingLines, False, lFD)
            lFD.write ("_if l_make_changes? _is _true\n")
            lFD.write ("_then\n")
            self.writeCaseCallingLines(lCallingLines, True, lFD)
          
            
            lFD.write ("custom_make_joins(l_case_view, l_make_changes?)\n")
            lFD.write ("custom_miscellaneous_changes(l_case_view, l_make_changes?)\n")
            for iextname in lExternalNames:
                lFD.write ("change_external_name(" + ":" + iextname[0] + "," + "'" + iextname[1] + "'" + "," + "'" + iextname[2] + "'" + "," + "l_case_view" + "," + "l_make_changes?" + ")\n")
            lFD.write ("_endif\n")        

            self.s_magikcodewriter.writeEndProcandDollar(lFD)

            ltestgen = XLSToSWUnitTestGenerator.XLSToSWUnitTestGenerator(self.fieldManager(), self.s_base_folder)
            ltestgen.writeUnitTests (lExternalNames, "MainModel", 'gis_view')
            
        lFD.closed

        

if __name__== "__main__":

    lXLSToSW = SovernetXLSToSW()

    lXLSToSW.resetFieldManager()
    lXLSToSW.processMainDBWorkBook ('Data Model Mapping 0412.xls')

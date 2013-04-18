
import XLSToSWFieldManager
import XLSToSWUnitTestGenerator
import XLSToSWField
import XLSToSWExceptions
import MagikCodeWriter
import xlrd
import operator


class SovernetXLSToSW():

    s_filename='not set'
    s_workbook='not set'
    s_show_features_p=True
    s_magikcodewriter='not set'
    s_base_folder='/home/glennx/Dropbox/Sovernet/'
    
     
    s_fieldmanager=XLSToSWFieldManager.XLSToSWFieldManager()

    def __init__(self):
        self.s_magikcodewriter = MagikCodeWriter.MagikCodeWriter()
        

    def sheetIsACoaxSheet (self, pSheetNumber):
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        lValue = lsheet.cell_value(2, 7)
        return lValue.lower()=='coax'

    def buildSWFieldComment(self, pSheet, pRow):
        lText=pSheet.cell_value (pRow, 0)
        lText=lText + ':'
        lText=lText + pSheet.cell_value (pRow, 2)
        lText=lText + ':'
        lText=lText + pSheet.cell_value (pRow, 4)
        return lText
    

    def buildSWField (self, pSheet, pRow):
        lUsed = pSheet.cell_value(pRow,9)
        if operator.or_(lUsed.lower()=='no', lUsed.lower()=='no-temporary'):
            raise XLSToSWExceptions.FieldNotMapped(repr(pSheet) + ':' + repr(pRow))

        lFieldDefaultValue=''
        lClassName = pSheet.cell_value(pRow,10)
        lFieldName = pSheet.cell_value(pRow, 11)
        lFieldExternalName = pSheet.cell_value(pRow,26)
        lFieldType = pSheet.cell_value(pRow,13)
        lFieldDefaultValue = pSheet.cell_value(pRow, 12)

        lFieldLength = pSheet.cell_value(pRow,14)
        # lFieldPriority = pSheet.cell_value(pRow,28)
        lFieldPriority = 10
        lFieldText = self.buildSWFieldComment(pSheet, pRow)

        lFeaturePoint=pSheet.cell_value(pRow,25)
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
            lField.s_field_join_type=pSheet.cell_value(pRow,32)
            lField.s_field_join_to  =pSheet.cell_value(pRow,31)
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
        pFD.write ("cogeco_upgrade_enums(l_make_changes?, p_case_name, " + '"' + pEnum[0] + '"' + ',' + lEnumValuesStr + ',' + '"' + pEnum[2] + '"' + ")\n")
        
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
            print ("case calling " + iCallingText)
            if operator.and_ (pCustomOnly==True, iCallingText.find("_cogeco")!=-1):
                pFD.write (iCallingText + "(l_make_changes?, p_case_name)\n")
            if operator.and_ (pCustomOnly==False, iCallingText.find("_cogeco")==-1):
                pFD.write (iCallingText + "(l_make_changes?, p_case_name)\n")

    def writeCasePreamble(self, pFD):
        lFIn = open (self.s_base_folder + 'CasePreamble.txt', 'r')
        for iline in lFIn:
            pFD.write(iline)

    def writeManualUpdatesToEnums(self, pFD):
        lFIn = open (self.s_base_folder +'ManualUpdatesToEnums.txt', 'r')
        for iline in lFIn:
            pFD.write(iline)

    def writeEnumUsages(self, pFD):
        pFD.write ("_global cogeco_make_enum_usages<<\n")
        pFD.write ("_proc(p_make_changes?)\n")
        for iClassName in self.fieldManager().classesManaged():
            for iField in self.fieldManager().findFieldsForClass(iClassName):
                if iField.isEnumField():
                    	pFD.write ('cogeco_make_enum_use (' + ':' + iField.fieldType() + ',' + ':' + iField.className() + ',' + ':' + iField.fieldName() + ',p_make_changes?)\n')
        pFD.write ("gis_program_manager.cached_dataset(:dynamic_enumerator).commit()\n")            	
        pFD.write ("_endproc\n")


    def writeCaseField (self, pClassName, pField, pFD):

        if pField.isValidJoin():
            return

        if pField.isIDField():
            pFD.write("cogeco_make_id_field(o, l_make_changes?)\n")
            return
        
        if pField.isPNIField():
            if pField.isStringType():
                pFD.write("cogeco_update_length_of_pni_field(o, " + "'" + pField.fieldName() + "'" + ", " + repr(pField.fieldLength()) + ",  p_make_changes?)\n")
            else:
                pFD.write("# Using PNI field " + pClassName + "." + pField.fieldName() + "\n")
            return 

        if pField.isPhysicalField():
            pFD.write ("cogeco_make_physical_field(o, :" + pField.fieldName() + ", " + '"' + pField.fieldExternalName() + '"' + ", :" + pField.fieldType() + ", l_make_changes?, " + pField.convertToString() + "," + "'" + pField.fieldComment() + "'" + ")\n")
            return
        
        if pField.isGeometryField():
            pFD.write ("cogeco_make_geometry_field(o, :" + pField.fieldName() + ", " + '"' + pField.fieldExternalName() + '"' + ", :" + pField.fieldType() + ", l_make_changes?, " + "(" + repr(pField.fieldPriority()) + ")" + ".floor" + ")\n")
            return

        if pField.fieldDefaultValue!='':   
            pFD.write ('cogeco_make_enum_field (o, ' + ':' + pField.fieldName() + ',' + '"' + pField.fieldExternalName() + '"' + ',' + ':' + pField.fieldType() + ',' + 'l_make_changes?' + ',' + '"' + pField.fieldDefaultValue() + '"' + ')\n')
        else:
            pFD.write ('cogeco_make_enum_field (o, ' + ':' + pField.fieldName() + ',' + '"' + pField.fieldExternalName() + '"' + ',' + ':' + pField.fieldType() + ',' + 'l_make_changes?)\n')


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
            
            
    def processLandbaseWorkBook (self, pSrcFileName, pTargetFileName, pUnitTestNameStem, pDatasetName, pOriginX=2000, pOriginY=2000, pUpperTabNo=10):

        loriginX=pOriginX
        loriginY=pOriginY
        
        self.s_filename=self.s_base_folder + pSrcFileName
        self.s_workbook=xlrd.open_workbook(self.s_filename)

        lExternalNames = self.parseExternalNamesSheet(1)
        lVersion = self.getVersion()
         
        for iSheetNumber in range (2,pUpperTabNo):
            try:
                lsheet = self.s_workbook.sheet_by_index(iSheetNumber)
                print ('sheet ' + repr(lsheet.name))
                self.parseSheet(iSheetNumber)
            except XLSToSWExceptions.SheetIsCoax:
                lblankcode = 0  # print ('sheet is a coax sheet' + repr(iSheetNumber))


        lClassesManaged=self.fieldManager().classesManaged()
        self.fieldManager().showClassesManaged()
        lCallingLines=[]
        
        with open(self.s_base_folder + pTargetFileName, 'w') as lFD:

            lFD.write ("# Cogeco Case Upgrade for " + lVersion + "\n")
            
            self.writeCasePreamble(lFD)
            
            for iClass in lClassesManaged:
                lCallingLines.append(self.writeCaseDefinition(iClass, lFD, loriginX, loriginY))
                loriginX=loriginX+2500
                loriginY=loriginY+4500

            self.s_magikcodewriter.writeMakeJoinsMagikCodePreamble(lFD)            
            for iJoinField in self.fieldManager().joinFields():
                lFD.write ('make_a_join (p_case_view, ' + '"' + iJoinField.s_field_join_type + '"' + ',' + ':' + iJoinField.className() + ',' + ':' + iJoinField.s_field_join_to + ', p_make_changes?)\n')
            self.s_magikcodewriter.writeEndProcandDollar(lFD)

            self.s_magikcodewriter.writeMakeCaseSelectMagikCodePreamble(lFD)
            for iClass in lClassesManaged:
                self.writeObjectSelectLine(iClass, lFD)
            self.s_magikcodewriter.writeEndProcandDollar(lFD)

            self.s_magikcodewriter.writeCaseUpgradeMagikCodePreamble(lFD)

            if pUnitTestNameStem == 'CCAD_landbase':
                lFD.write ('gMakeLandbaseEnumerators()\n')
                
            self.writeCaseCallingLines(lCallingLines, False, lFD)
            lFD.write ("_if l_make_changes? _is _true\n")
            lFD.write ("_then\n")
            self.writeCaseCallingLines(lCallingLines, True, lFD)
            lFD.write ("cogeco_make_joins(l_case_view, l_make_changes?)\n")
            for iextname in lExternalNames:
                lFD.write ("change_external_name(" + ":" + iextname[0] + "," + "'" + iextname[1] + "'" + "," + "'" + iextname[2] + "'" + "," + "l_case_view" + "," + "l_make_changes?" + ")\n")
            lFD.write ("_endif\n")        
            self.s_magikcodewriter.writeEndProcandDollar(lFD)

            ltestgen = XLSToSWUnitTestGenerator.XLSToSWUnitTestGenerator(self.fieldManager(), self.s_base_folder)
            ltestgen.writeUnitTests (lExternalNames, pUnitTestNameStem, pDatasetName)
        
        lFD.closed
    
        
        

    def processMainDBWorkBook (self, pFileName):

        self.s_filename=self.s_base_folder + pFileName
        self.s_workbook=xlrd.open_workbook(self.s_filename)
        
        lEnumerators = []
    
        lEnumerators = self.parseDynamicEnumeratorsSheet(1)
        lExternalNames = self.parseExternalNamesSheet(3)
        lVersion = self.getVersion()
        
        for iSheetNumber in range (4,15):
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

            lFD.write ("# Cogeco Case Upgrade for " + lVersion + "\n")
            
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

            
            lFD.write ("cogeco_make_enum_usages(l_make_changes?)\n")
            
            self.writeCaseCallingLines(lCallingLines, False, lFD)
            lFD.write ("_if l_make_changes? _is _true\n")
            lFD.write ("_then\n")
            self.writeCaseCallingLines(lCallingLines, True, lFD)
          
            
            lFD.write ("cogeco_make_joins(l_case_view, l_make_changes?)\n")
            lFD.write ("cogeco_miscellaneous_changes(l_case_view, l_make_changes?)\n")
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
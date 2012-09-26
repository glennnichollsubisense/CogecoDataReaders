
import CogecoFieldManager
import CogecoField
import CogecoExceptions
import xlrd
import operator


class CogecoXLSToSW():

    s_filename='not set'
    s_workbook='not set'
    s_show_features_p=False
    # s_base_folder='/home/glennx/Dropbox/'
    s_base_folder='D:/Cogeco/Data/'
     
    s_fieldmanager=CogecoFieldManager.CogecoFieldManager()

    def __init__(self):
        self.s_filename=self.s_base_folder + 'CCAD datamodel for conversion v9 new.xls'
        self.s_workbook=xlrd.open_workbook(self.s_filename)
        

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
            raise CogecoExceptions.FieldNotMapped(repr(pSheet) + ':' + repr(pRow))

        lFieldDefaultValue=''
        lClassName = pSheet.cell_value(pRow,10)
        lFieldName = pSheet.cell_value(pRow, 11)
        lFieldExternalName = pSheet.cell_value(pRow,26)
        lFieldType = pSheet.cell_value(pRow,13)
        lFieldDefaultValue = pSheet.cell_value(pRow, 12)            
        lFieldLength = pSheet.cell_value(pRow,14)
        lFieldPriority = pSheet.cell_value(pRow,28)
        lFieldText = self.buildSWFieldComment(pSheet, pRow)

        lFeaturePoint=pSheet.cell_value(pRow,25)
        if operator.and_(lFeaturePoint<>"", self.s_show_features_p==True):
            print ("----------Feature " + lFeaturePoint)

        lField = CogecoField.CogecoField(lClassName, lFieldName, lFieldType)
        lField.s_field_external_name = lFieldExternalName
        if lFieldLength<>'':
            lField.s_field_length = lFieldLength
        if lFieldPriority<>'':
            lField.s_field_priority=lFieldPriority
        if lFieldText<>'':
            lField.s_field_comment=lFieldText
        if lFieldDefaultValue<>'':
            lField.s_field_default_value=lFieldDefaultValue
        if lField.fieldType().lower() == "join":
            lField.s_field_join_type=pSheet.cell_value(pRow,32)
            lField.s_field_join_to  =pSheet.cell_value(pRow,31)
            if lField.isValidJoin()==False:
                print ("found an invalid join ")
                lField.showMe()
            
        # lField.showMe()
        return lField

    def fieldManager(self):
        return self.s_fieldmanager

    def parseDynamicEnumeratorsSheet(self, pSheetNumber):
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        lenumerators=[]
        try:
            for iRow in range(2, 30):
                lEnumeratorName=lsheet.cell_value(iRow, 0)
                lEnumeratorValues=lsheet.cell_value(iRow, 1)
                lEnumeratorDefault=lsheet.cell_value(iRow, 2)
                lenumerators.append ([lEnumeratorName, lEnumeratorValues, lEnumeratorDefault])

                

        except IndexError:
            lblankcode= 0   #print("index error went off")

        return lenumerators


    def getVersion(self):
        lsheet = self.s_workbook.sheet_by_index(0)
        lversion = lsheet.cell_value(0, 2)
        print ("version = " + lversion)

        return lversion
    
        

    def parseExternalNamesSheet(self, pSheetNumber):
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        lexternalnames=[]
        try:
            for iRow in range(3, 32):
                lInternalName=lsheet.cell_value(iRow, 0)
                lPNIExternalName=lsheet.cell_value(iRow, 1)
                lCogecoExternalName=lsheet.cell_value(iRow, 2)
                lexternalnames.append ([lInternalName, lPNIExternalName, lCogecoExternalName])

                

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
        if pEnum[0].find('cogeco_')==-1:
            pFD.write('#')
        pFD.write ("cogeco_upgrade_enums(l_make_changes?, p_case_name, " + '"' + pEnum[0] + '"' + ',' + lEnumValuesStr + ',' + '"' + pEnum[2] + '"' + ")\n")
        
    def parseSheet(self, pSheetNumber=0):

        if self.sheetIsACoaxSheet(pSheetNumber):
            raise CogecoExceptions.SheetIsCoax(pSheetNumber)
            
        lsheet = self.s_workbook.sheet_by_index(pSheetNumber)
        # try:
        for iRow in range(2, 130):
            try:
                lField=self.buildSWField (lsheet, iRow)
                self.s_fieldmanager.addField(lField)
                
            except CogecoExceptions.FieldNotMapped:
                    #print ('field not mapped went off')
                    lblankcode =0
            except CogecoExceptions.InvalidDSType:
                    print ('Invalid ds type in sheet ' + lsheet.name + ' line ' + repr (iRow))
                    lField.showMe()
            

            except IndexError:
                # print ('indexerror went off')
                lblankcode= 0
            
    def writeCaseCallingLines (self, pCallingTexts, pCogecoOnly, pFD):
        for iCallingText in pCallingTexts:
            if operator.and_ (pCogecoOnly==True, iCallingText.find("_cogeco")<>-1):
                pFD.write (iCallingText + "(l_make_changes?, p_case_name)\n")
            if operator.and_ (pCogecoOnly==False, iCallingText.find("_cogeco")==-1):
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


    def writeCaseObjectHeader (self, pClassName, pFD):
        lMethodName="cogeco_update_" + pClassName
        pFD.write ("_global " + lMethodName + "<<\n")
        pFD.write ("_proc ( _optional p_make_changes?, p_case_name)\n")
        pFD.write ("_local l_case_name << p_case_name.default(cogeco_get_default_case_name())\n")
        pFD.write ("_local  l_make_changes? << p_make_changes?.default(_false)\n")
        pFD.write ("_local o, an_f, a_pred\n")
        pFD.write ("_local gpm << gis_program_manager\n")
        pFD.write ("_local cv  << gpm.cached_dataset(l_case_name)\n")
        pFD.write ("_if cv.object_map _is _unset _then cv.object_map << hash_table.new() _endif\n")
        pFD.write ("_if cv.object_offset _is _unset _then cv.object_offset<< coordinate.new(0,0) _endif\n")
        pFD.write ("_dynamic !current_dsview! << cv\n")
        pFD.write ("_dynamic !current_world! << cv.world\n")
        pFD.write ("a_pred << predicate.eq (:name, :" + pClassName + ")\n")
        pFD.write ("o << cv.collections[:sw_gis!case_object].select(a_pred).an_element()\n")
        pFD.write ("_if o _is _unset _then\n")
        pFD.write ("l_info_string << 'made " + pClassName + "'\n")
        pFD.write ("_if l_make_changes? _is _true _then\n")
        pFD.write ("o << case_object.new_from_archive(\n")
        pFD.write ("{47234,\n")
        pFD.write ('"' + pClassName + '",\n')
        pFD.write ("write_string('" + pClassName + "'),\n")
        pFD.write ("'" + pClassName + "',\n")
        pFD.write (" _unset,{0,0,0},0} ,12000.0000000, 12000.0000000)\n")
        pFD.write ("o.set_trigger(:insert,'insert_trigger()')\n")
        pFD.write ("o.set_trigger(:insert,'update_trigger()')\n")
        pFD.write ("o.set_trigger(:insert,'delete_trigger()')\n")
        pFD.write ("_else\n")
        pFD.write ("l_info_string << ''.concatenation ('!! NOT WRITING:: ', l_info_string)\n")
        pFD.write ("_endif\n")
        pFD.write ("write (l_info_string)\n")
        pFD.write ("_endif\n")
        return lMethodName


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

        if pField.fieldDefaultValue<>'':   
            pFD.write ('cogeco_make_enum_field (o, ' + ':' + pField.fieldName() + ',' + ':' + pField.className() + ',' + ':' + pField.fieldType() + ',' + 'l_make_changes?' + ',' + '"' + pField.fieldDefaultValue() + '"' + ')\n')
        else:
            pFD.write ('cogeco_make_enum_field (o, ' + ':' + pField.fieldName() + ',' + ':' + pField.className() + ',' + ':' + pField.fieldType() + ',' + 'l_make_changes?)\n')


    def writeCaseObjectTail (self, pFD):
        pFD.write ("_endproc\n")
        pFD.write ("$\n")

    def writeCaseDefinition (self, pClassName, pFD):

        lCallingText = self.writeCaseObjectHeader(pClassName, pFD)
        lFields = self.fieldManager().findFieldsForClass(pClassName)
        if (len(lFields)==0):
            raise CogecoExceptions.ClassNotManaged (pClassName)
    
        for iField in lFields:
            self.writeCaseField(pClassName, iField, pFD)
                
        self.writeCaseObjectTail(pFD)
        
        return lCallingText

    def writeObjectSelectLine(self, pObjectName, pFD):
        pFD.write ("lSelectCaseObject(" + "'" + pObjectName + "'" + "," + "l_case_name"+ ")\n")



if __name__== "__main__":

    print ('######### CogecoXLSToSW')
    lXLSToSW = CogecoXLSToSW()
    lEnumerators = []
    
    lEnumerators = lXLSToSW.parseDynamicEnumeratorsSheet(2)
    lExternalNames = lXLSToSW.parseExternalNamesSheet(3)
    lVersion = lXLSToSW.getVersion()
    
    for iSheetNumber in range (4,122):
        try:
            lsheet = lXLSToSW.s_workbook.sheet_by_index(iSheetNumber)
            print ('sheet ' + repr(lsheet.name))
            lXLSToSW.parseSheet(iSheetNumber)
           
                
        except CogecoExceptions.SheetIsCoax:
            lblankcode = 0  # print ('sheet is a coax sheet' + repr(iSheetNumber))

    

    lClassesManaged=lXLSToSW.fieldManager().classesManaged()
    lCallingLines=[]
    
    with open(lXLSToSW.s_base_folder + 'case_upgrade.magik', 'w') as lFD:
        lXLSToSW.writeCasePreamble(lFD)
        lXLSToSW.writeManualUpdatesToEnums(lFD)

        lXLSToSW.writeEnumUsages(lFD)
        
        for iClass in lClassesManaged:
            lCallingLines.append(lXLSToSW.writeCaseDefinition(iClass, lFD))

        lFD.write ("_global cogeco_make_joins<<\n")
        lFD.write ("_proc (p_case_view, p_make_changes?)\n")
        lFD.write("_local make_a_join<<\n")
        lFD.write("_proc (pCaseView, pType, pParentTable, pChildTable, pMakeChanges?)\n")
        lFD.write("\n")
        lFD.write("_local lInfoString<<''\n")
        lFD.write("_local a_pred << predicate.eq (:name, pParentTable)\n")
        lFD.write("_local o << pCaseView.collections[:sw_gis!case_object].select(a_pred).an_element()\n")
        lFD.write("_if o _is _unset\n")
        lFD.write("_then\n")
        lFD.write("lInfoString<< 'tried to make a join to an unknown table ' + pParentTable\n")
        lFD.write("_else\n")
        lFD.write("_if o.get_field (pChildTable) _is _unset\n")
        lFD.write("_then\n")
        lFD.write("lInfoString<< 'made a join ' + pType + '.' + pParentTable + '.' + pChildTable\n")
        lFD.write("_if pMakeChanges?\n")
        lFD.write("_then\n")
        lFD.write("pCaseView.create_relationship (pType, pParentTable, pChildTable)\n")
        lFD.write("_else\n")
        lFD.write("lInfoString<< ''.concatenation ('!! NOT WRITING:: ', lInfoString)\n")
        lFD.write("_endif\n")
        lFD.write("_endif\n")
        lFD.write("_endif\n")
        lFD.write("write (lInfoString)\n")
        lFD.write("_endproc\n")
        
        for iJoinField in lXLSToSW.fieldManager().joinFields():
            lFD.write ('make_a_join (p_case_view, ' + '"' + iJoinField.s_field_join_type + '"' + ',' + ':' + iJoinField.className() + ',' + ':' + iJoinField.s_field_join_to + ', p_make_changes?)\n')
        lFD.write ("_endproc\n")
        lFD.write ("$\n")

        lFD.write ("_global cogeco_case_select<<\n")
        lFD.write ("_proc(_optional p_case_name)\n")
        lFD.write ("_local l_case_name << p_case_name.default(cogeco_get_default_case_name())\n")


        lFD.write("_local lSelectCaseObject << _proc(pObjectName, pCaseName)\n")
        lFD.write("_local gpm << gis_program_manager\n")
        lFD.write("\n")
        lFD.write("_local lCaseApplication\n")
        lFD.write("_for i _over smallworld_product.applications.fast_elements() \n")
        lFD.write("_loop\n")
        lFD.write("_if i.soc_name _is pCaseName\n")
        lFD.write("_then\n")
        lFD.write("lCaseApplication << i\n")
        lFD.write("_endif\n")
        lFD.write("_endloop\n")
        lFD.write("_local lPlugin << lCaseApplication.plugin(:maps)\n")
        lFD.write("_local l_map << lPlugin.current_map_document_gui.map_manager.current_map\n")
        lFD.write("\n")
        lFD.write("_local v_c << gpm.cached_dataset (pCaseName)\n")
        lFD.write("_local a_pred << predicate.eq (:name, pObjectName)\n")
        lFD.write("_local a_cobj << v_c.collections[:sw_gis!case_object].select(a_pred).an_element()\n")
        lFD.write("\n")
        lFD.write("_if a_cobj _is _unset _orif\n")
        lFD.write("a_cobj.position _is _unset _orif\n")
        lFD.write("a_cobj.outline _is _unset\n")
        lFD.write("_then\n")
        lFD.write("condition.raise (:user_error, :string, pObjectName + ' object not available for selection ')\n")
        lFD.write("_endif \n")
        lFD.write("\n")
        lFD.write("write ('adding ', a_cobj.name, ' to the selection' )\n")
        lFD.write("l_map.add_geometry_to_selection(geometry_set.new_with(a_cobj.position))\n")
        lFD.write("l_map.add_geometry_to_selection(geometry_set.new_with(a_cobj.outline))\n")
        lFD.write("_endproc \n")            


            
        for iClass in lClassesManaged:
            lXLSToSW.writeObjectSelectLine(iClass, lFD)        
            
        lFD.write ("_endproc\n")
        lFD.write ("$\n")

        lFD.write ("_global cogeco_make_case_upgrade<<\n")
        lFD.write ("_proc(_optional p_make_changes?, p_case_name)\n")
        lFD.write ("_local l_make_changes?<< p_make_changes?.default(_false)\n")
        lFD.write ("_local l_case_view<< gis_program_manager.cached_dataset(p_case_name.default(cogeco_get_default_case_name()))\n")
    
        for iEnum in lEnumerators:
            lXLSToSW.writeEnumCallingLine(iEnum, lFD)

        
        lFD.write ("cogeco_make_enum_usages(l_make_changes?)\n")
        
        lXLSToSW.writeCaseCallingLines(lCallingLines, False, lFD)
        lFD.write ("_if l_make_changes? _is _true\n")
        lFD.write ("_then\n")
        lXLSToSW.writeCaseCallingLines(lCallingLines, True, lFD)
      
        
        lFD.write ("cogeco_make_joins(l_case_view, l_make_changes?)\n")
        lFD.write ("cogeco_miscellaneous_changes(l_case_view, l_make_changes?)\n")
        for iextname in lExternalNames:
            lFD.write ("change_external_name(" + ":" + iextname[0] + "," + "'" + iextname[1] + "'" + "," + "'" + iextname[2] + "'" + "," + "l_case_view" + "," + "l_make_changes?" + ")\n")
        lFD.write ("_endif\n")        

        lFD.write ("_endproc\n")
        lFD.write ("$\n")
    
    lFD.closed

        

import xlrd

class MagikCodeWriter():


    def __init__(self):
        ldonothing=0
        

    def writeCaseUpgradeMagikCodePreamble(self, pFD):
        pFD.write ("_global cogeco_make_case_upgrade<<\n")
        pFD.write ("_proc(_optional p_make_changes?, p_case_name)\n")
        pFD.write ("_local l_make_changes?<< p_make_changes?.default(_false)\n")
        pFD.write ("_local l_case_view<< gis_program_manager.cached_dataset(p_case_name.default(cogeco_get_default_case_name()))\n")

        
    def writeMakeJoinsMagikCodePreamble(self, pFD):
        
        pFD.write ("_global cogeco_make_joins<<\n")
        pFD.write ("_proc (p_case_view, p_make_changes?)\n")
        pFD.write("_local make_a_join<<\n")
        pFD.write("_proc (pCaseView, pType, pParentTable, pChildTable, pMakeChanges?)\n")
        pFD.write("\n")
        pFD.write("_local lInfoString<<''\n")
        pFD.write("_local a_pred << predicate.eq (:name, pParentTable)\n")
        pFD.write("_local o << pCaseView.collections[:sw_gis!case_object].select(a_pred).an_element()\n")
        pFD.write("_if o _is _unset\n")
        pFD.write("_then\n")
        pFD.write("lInfoString<< 'tried to make a join to an unknown table ' + pParentTable\n")
        pFD.write("_else\n")
        pFD.write("_local l_joinname<<pChildTable\n")
        pFD.write("_if pTYpe='1:n' _orif\n")
        pFD.write("pType ='0:n'\n")
        pFD.write("_then\n")
        pFD.write("l_joinname << l_joinname+ 's'\n")
        pFD.write("_endif\n")
        pFD.write("_if o.get_field (l_joinname) _is _unset\n")        
        pFD.write("_then\n")
        pFD.write("lInfoString<< 'made a join ' + pType + '.' + pParentTable + '.' + pChildTable\n")
        pFD.write("_if pMakeChanges?\n")
        pFD.write("_then\n")
        pFD.write("pCaseView.create_relationship (pType, pParentTable, pChildTable)\n")
        pFD.write("_else\n")
        pFD.write("lInfoString<< ''.concatenation ('!! NOT WRITING:: ', lInfoString)\n")
        pFD.write("_endif\n")
        pFD.write("_endif\n")
        pFD.write("_endif\n")
        pFD.write("write (lInfoString)\n")
        pFD.write("_endproc\n")


    def writeEndProcandDollar(self, pFD):

        pFD.write ("_endproc\n")
        pFD.write ("$\n\n")

        

    def writeCaseObjectHeader (self, pClassName, pFD, pX=12000.0, pY=12000.0):
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
        pFD.write (" _unset,{0,0,0},0} ," + repr(pX) + "," + repr(pY) + ")\n")
        pFD.write ("o.set_trigger(:insert,'insert_trigger()')\n")
        pFD.write ("o.set_trigger(:insert,'update_trigger()')\n")
        pFD.write ("o.set_trigger(:insert,'delete_trigger()')\n")
        pFD.write ("_else\n")
        pFD.write ("l_info_string << ''.concatenation ('!! NOT WRITING:: ', l_info_string)\n")
        pFD.write ("_endif\n")
        pFD.write ("write (l_info_string)\n")
        pFD.write ("_endif\n")
        return lMethodName

    
    def writeMakeCaseSelectMagikCodePreamble(self, pFD):
            pFD.write ("_global cogeco_case_select<<\n")
            pFD.write ("_proc(_optional p_case_name)\n")
            pFD.write ("_local l_case_name << p_case_name.default(cogeco_get_default_case_name())\n")


            pFD.write("_local lSelectCaseObject << _proc(pObjectName, pCaseName)\n")
            pFD.write("_local gpm << gis_program_manager\n")
            pFD.write("\n")
            pFD.write("_local lCaseApplication\n")
            pFD.write("_for i _over smallworld_product.applications.fast_elements() \n")
            pFD.write("_loop\n")
            pFD.write("_if i.soc_name _is pCaseName\n")
            pFD.write("_then\n")
            pFD.write("lCaseApplication << i\n")
            pFD.write("_endif\n")
            pFD.write("_endloop\n")
            pFD.write("_local lPlugin << lCaseApplication.plugin(:maps)\n")
            pFD.write("_local l_map << lPlugin.current_map_document_gui.map_manager.current_map\n")
            pFD.write("\n")
            pFD.write("_local v_c << gpm.cached_dataset (pCaseName)\n")
            pFD.write("_local a_pred << predicate.eq (:name, pObjectName)\n")
            pFD.write("_local a_cobj << v_c.collections[:sw_gis!case_object].select(a_pred).an_element()\n")
            pFD.write("\n")
            pFD.write("_if a_cobj _is _unset _orif\n")
            pFD.write("a_cobj.position _is _unset _orif\n")
            pFD.write("a_cobj.outline _is _unset\n")
            pFD.write("_then\n")
            pFD.write("condition.raise (:user_error, :string, pObjectName + ' object not available for selection ')\n")
            pFD.write("_endif \n")
            pFD.write("\n")
            pFD.write("write ('adding ', a_cobj.name, ' to the selection' )\n")
            pFD.write("l_map.add_geometry_to_selection(geometry_set.new_with(a_cobj.position))\n")
            pFD.write("l_map.add_geometry_to_selection(geometry_set.new_with(a_cobj.outline))\n")
            pFD.write("_endproc \n")          

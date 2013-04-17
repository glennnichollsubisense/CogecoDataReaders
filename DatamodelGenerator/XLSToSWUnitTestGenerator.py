
import XLSToSWFieldManager
import XLSToSWField
import XLSToSWExceptions
import xlrd
import operator

class XLSToSWUnitTestGenerator():

    s_base_folder='D:/Cogeco/Data'
    s_no_hand_edit="## This file is machine generated.  Dont add any hand-edits\n"
    s_fieldmanager="Nothing"


    def __init__(self, pFieldManager, pBaseFolder):
        self.s_base_folder=pBaseFolder
        self.s_fieldmanager=pFieldManager

    def fieldManager(self):
        return self.s_fieldmanager




    def writeUnitTestsAnnoMethods(self, pFilename):
        ## Writes out unit tests checking for the method behind the annotations
        with open(self.s_base_folder + pFilename + '.magik', 'w') as lFD:
            lFD.write("_package user\n")
            lFD.write ("$\n")
            lFD.write ("\n\n")
            lFD.write("## Tests that the annotation methods are available in the image\n")
            lFD.write (self.s_no_hand_edit)

            lClassesManaged = self.fieldManager().classesManaged()
            for iclass in lClassesManaged:
                
                for ifield in self.fieldManager().findFieldsForClass (iclass):
                    if ifield.isGeometryField():
                        if ifield.fieldType().find("text")!=-1:
                            lFD.write("## testing for class " + iclass + "\n")
                            lFD.write ("_method tc!" + iclass + ".test_method_for_" + ifield.fieldName() + "()\n")
                            lFD.write ("_self.assert_not_unset (" + iclass + ".method(:|" + ifield.fieldName() + "_text|), 'missing an annotation method')\n")
                            lFD.write ("_endmethod\n")
                            lFD.write ("$\n")
                            lFD.write ("\n\n")                           
        lFD.closed


    def writeUnitTestsSysIDs(self, pFilename, pDatasetName):
        ## Writes out unit tests checking for the method behind the annotations
        with open(self.s_base_folder + pFilename + '.magik', 'w') as lFD:

            lFD.write("_package user\n")
            lFD.write ("$\n")
            lFD.write ("\n\n")
            lFD.write("## Tests that the cogeco tables are not 64-bit ids\n")
            lFD.write (self.s_no_hand_edit)

            lClassesManaged = self.fieldManager().classesManaged()
            for iclass in lClassesManaged:
                if iclass.find('cogeco')!=-1:
                    lFD.write("## testing for class " + iclass + "\n")
                    lFD.write ("_method tc!" + iclass + ".test_sysid()\n")
                    lFD.write ("_local l_obj << _self." + pDatasetName + ".collections[:" + iclass + "]\n")
                    lFD.write ("_local l_descriptor<< l_obj.descriptor\n")
                    lFD.write ("_self.assert_not_equals (l_descriptor.all_fields[:id].type.name, 'sys_id64', '64 bit id !!')\n")                    
                    lFD.write ("_self.assert_true (l_descriptor.all_fields[:id].is_key?, 'id field should be a key field')\n")                    
                    lFD.write ("_endmethod\n")
                    lFD.write ("$\n")
                    lFD.write ("\n\n")

        lFD.closed


    def writeUnitTestsBooleansAreMandatory(self, pFilename, pDatasetName):
        ## Writes out unit tests checking that the booleans are mandatory

        with open(self.s_base_folder + pFilename + '.magik', 'w') as lFD:


            lFD.write("_package user\n")
            lFD.write ("$\n")
            lFD.write ("\n\n")
            lFD.write("## Tests that the boolean fields are mandatory\n")
            lFD.write (self.s_no_hand_edit)

            lClassesManaged = self.fieldManager().classesManaged()
            for iclass in lClassesManaged:

                lhaveaboolean=False
                for ifield in self.fieldManager().findFieldsForClass(iclass):
                    if ifield.isBooleanField():
                        lhaveaboolean=True


                if lhaveaboolean==True:        
                    lFD.write("## testing for class " + iclass + "\n")
                    lFD.write ("_method tc!" + iclass + ".test_booleans_are_mandatory()\n")
                    lFD.write("_local ldescriptor << _self." + pDatasetName + ".collections[:" + iclass + "].descriptor\n")
                    lFD.write ("_local lfielddescriptor<< 'not set'\n")

                    for ifield in self.fieldManager().findFieldsForClass(iclass):
                        if ifield.isBooleanField():
                            lFD.write("lfielddescriptor << ldescriptor.all_fields[:" + ifield.fieldName() + "]\n")
                            lFD.write("_self.assert_true (lfielddescriptor.mandatory?, 'expecting a mandatory field')\n")


                                                    
                    lFD.write ("_endmethod\n")
                    lFD.write ("$\n")
                    lFD.write ("\n\n")


        lFD.closed
        


    def writeUnitTestsVisibleinAce(self, pFilename):
        ## Writes out unit tests checking for the fields being visible in the ace
        with open(self.s_base_folder + pFilename + '.magik', 'w') as lFD:

            lFD.write("_package user\n")
            lFD.write ("$\n")
            lFD.write ("\n\n")
            lFD.write("## Tests that the field is visible in the ace\n")
            lFD.write (self.s_no_hand_edit)

            lClassesManaged = self.fieldManager().classesManaged()
            for iclass in lClassesManaged:
                    lFD.write("## testing for class " + iclass + "\n")
                    lFD.write ("_method tc!" + iclass + ".test_visible_in_ace()\n")

                    lFD.write ("_local l_in_ace<< false\n")
                    for ifield in self.fieldManager().findFieldsForClass(iclass):

                        if ifield.isPhysicalField():

                            lFD.write ("l_in_ace << _self.is_field_visible_in_ace(" + ":"+ iclass + "," + ":" + ifield.fieldName() + ")\n")
                            lFD.write ("_self.assert_true(l_in_ace)\n")

                        
                    lFD.write ("_endmethod\n")
                    lFD.write ("$\n")
                    lFD.write ("\n\n")

        lFD.closed

    def writeUnitTestsDataModel(self, pFilename, pDatasetName):
        ## Writes out unit tests checking the datamodel
        with open(self.s_base_folder + pFilename + '.magik', 'w') as lFD:
            lFD.write ("_package user\n")
            lFD.write ("$\n")
            lFD.write ("\n\n")
            lFD.write (self.s_no_hand_edit)

            lClassesManaged = self.fieldManager().classesManaged()
            for iclass in lClassesManaged:
                
                lFD.write ("## testing for class " + iclass + "\n")
                lFD.write ("_pragma(classify_level=advanced,topic={unit_tests,cogeco},usage={subclassable})\n")
                lFD.write ("_method tc!" + iclass + ".test_datamodel()\n")

                lFD.write ("_local l_obj << _self." + pDatasetName + ".collections[:" + iclass + "]\n")
                lFD.write ("_local l_descriptor<< l_obj.descriptor\n")
                lFD.write ("_local lfields << l_descriptor.all_fields\n")
                for ifield in self.fieldManager().findFieldsForClass (iclass):

                    if ifield.isValidJoin()!=True:
                        lFD.write("_self.assert_not_unset (lfields[:" + ifield.fieldName() + "], " + "'" + "no field called " + ifield.fieldName() + "'" + ")\n")
                        lFD.write("_self.assert_equals (lfields[:" + ifield.fieldName() + "].external_name, " + "'" + ifield.fieldExternalName() + "'" + "," + "'" + "field should be called " + ifield.fieldExternalName() + "'" + ")\n")                       
                        if ifield.isStringType():
                            lFD.write ("_self.assert_equals (lfields[:" + ifield.fieldName() + "].print_width, " + repr(ifield.fieldLength()) + "," + "'" + " Expecting the " + ifield.fieldName() + " field to be of length " + repr(ifield.fieldLength()) + "')" + "\n")

                lFD.write ("_endmethod\n")
                lFD.write ("$\n")
                lFD.write ("\n\n")
            
                lFD.write ("_method tc!" + iclass + ".suite(_gather keys_and_elements)\n")
                lFD.write ("_return test_suite.new( tc!" + iclass + ")\n")
                lFD.write ("_endmethod\n")
                lFD.write ("$\n")
                lFD.write ("\n\n")


        lFD.closed



    def writeUnitTestsExternalNames(self, pExternalNames, pFilename, pDatasetName):
        ## Writes out unit tests checking the external names of the tables
        ## pExternalNames holds the names in a set of
        ## [0] - internal name
        ## [1] - PNI name
        ## [2] - Required Cogeco Name
        with open(self.s_base_folder + pFilename + '.magik', 'w') as lFD:
            lFD.write ("_package user\n")
            lFD.write ("$\n")
            lFD.write ("\n\n")
            lFD.write (self.s_no_hand_edit)

            for inameset in pExternalNames:
                linternalname = inameset[0]
                lcogeconame = inameset[2]
                lFD.write ("## testing for class " + linternalname + "\n")
                lFD.write ("_pragma(classify_level=advanced,topic={unit_tests,cogeco},usage={subclassable})\n")
                lFD.write ("_method tc!" + linternalname + ".test_externalname()\n")
                lFD.write ("_local l_obj << _self." + pDatasetName + ".collections[:" + linternalname + "]\n")
                lFD.write ("_local l_descriptor<< l_obj.descriptor\n")
                lFD.write("_self.assert_equals (l_descriptor.external_name, " + "'" + lcogeconame + "'" + "," + "'" + "external name should be " + lcogeconame + "'" + ")\n")
                lFD.write ("_endmethod\n")
                lFD.write ("$\n")
                lFD.write ("\n\n")


        lFD.closed


    def writeUnitTests (self, pExternalNames, pFilenameStem, pDatasetName):
        
        ## Writes out all the unit tests        
        self.writeUnitTestsBooleansAreMandatory('unit_tests_booleans_are_mandatory_' + pFilenameStem, pDatasetName)
        self.writeUnitTestsExternalNames(pExternalNames, 'unit_tests_external_names_'  + pFilenameStem, pDatasetName)
        self.writeUnitTestsAnnoMethods('unit_tests_anno_methods_'  + pFilenameStem)
        self.writeUnitTestsSysIDs('unit_tests_sys_ids_'  + pFilenameStem, pDatasetName)
        self.writeUnitTestsDataModel('unit_tests_datamodel_'  + pFilenameStem, pDatasetName)
        self.writeUnitTestsVisibleinAce('unit_tests_ace_visibilities_'  + pFilenameStem)


        

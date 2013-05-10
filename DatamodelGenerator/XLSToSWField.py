import XLSToSWExceptions
import XLSToSWCustomEnumeratorGenerator
import operator


class XLSToSWField():
    
    s_class_name=''
    s_field_name=''
    s_field_external_name=''
    s_field_type=''
    s_field_length=0
    s_field_unit=''
    s_field_comment=''
    s_field_join_type=''
    s_field_join_to=''
    s_field_priority=99
    s_field_default_value=''
    s_field_from_table=''
    s_field_from_field=''
    
    s_valid_field_types=['ds_date', 'ds_uint', 'ds_float', 'ds_bool', 'ds_char16canon_vec', 'ds_char16_vec', 'join', 'simple_area', 'simple_point', 'simple_chain', 'chain', 'point', 'sys_id', 'text', 'ds_int']
    s_valid_enumerator_names=['alt_transportation_type', 'anchor_type', 'conduit_color', 'construction_status_type_type', 'drop_type', 'figure_eight_type', 'material_type', 'mit_hub_type', 'pole_usage', 'splice_method_type', 'waterway_type']
    
    def __init__(self, pclassname='', pfieldname='', pfieldtype=''):
        
        if pclassname.find(' ')!=-1:
            raise XLSToSWExceptions.TrailingSpaceInClassName (pclassname)
        if pfieldname.find(' ')!=-1:
            raise XLSToSWExceptions.TrailingSpaceInFieldName (pfieldname)
            
        self.s_class_name=pclassname
        self.s_field_name=pfieldname
        self.s_field_type=pfieldtype
        self.s_field_length=0
        self.s_field_comment = ""



    def className(self):
        return self.s_class_name

    def fieldName(self):
        return self.s_field_name

    def fieldExternalName(self):
        return self.s_field_external_name

    def fieldType(self):
        return self.s_field_type

    def fieldLength(self):
        return self.s_field_length

    def fieldUnit(self):
        return self.s_field_unit

    def fieldComment(self):
        return self.s_field_comment

    def fieldPriority(self):
        return self.s_field_priority

    def fieldDefaultValue(self):
        return self.s_field_default_value

    def fieldFromTable(self):
        return self.s_field_from_table

    def fieldFromField(self):
        return self.s_field_from_field

    def isValidType(self):

        # checks through the set of valid data types and then the known enumerator names
        # if the type is not found in either of those places, a false is returned.   
        for iType in self.s_valid_field_types:
            if self.fieldType() == iType:
                return True
        for iType in self.s_valid_enumerator_names:
            if self.fieldType() == iType:
                return True
        l_custom_enums = XLSToSWCustomEnumeratorGenerator.XLSToSWCustomEnumeratorGenerator()
        for iType in l_custom_enums.customEnums('Sovernet'):
            if self.fieldType() == iType:
                return True

        return False

    def isGeometryField(self):
        if self.fieldType().lower() == "simple_area":
            return True
        if self.fieldType().lower() == "area":
            return True
        if self.fieldType().lower() == "simple_point":
            return True
        if self.fieldType().lower() == "point":
            return True
        if self.fieldType().lower() == "simple_chain":
            return True
        if self.fieldType().lower() == "chain":
            return True
        if self.fieldType().lower() == "text":
            return True
        return False

    def isPhysicalField(self):
        if self.fieldType().lower() == "ds_uint":
            return True
        if self.fieldType().lower() == "ds_float":
            return True
        if self.fieldType().lower() == "ds_bool":
            return True
        if self.fieldType().lower() == "ds_date":
            return True
        if self.isStringType():
            return True
        return False

    def isIDField(self):
        return self.fieldType().lower() == 'sys_id'
            

    def isEnumField(self):
        if self.fieldType().lower().find('sov_')!=-1:
            return True
        return False

    
    def isBooleanField(self):
        if self.fieldType().lower().find('bool')!=-1:
            return True
        return False
    

    def isStringType(self):
        if self.fieldType().lower() == "ds_char16canon_vec":
            return True
        if self.fieldType().lower() == "ds_char16_vec":
            return True
        return False
    
        

    def __isJoin(self):
        return self.fieldType().lower() == 'join'

    
    def isValidJoin(self):

        if self.__isJoin() == False:
            return False
        if self.s_field_join_type=='':
            print ('failing because join type is not set')
            self.showMe()
            return False
        if self.s_field_join_to=='':
            print ('failing because join to is not set')
            self.showMe()
            return False

        return True

    def convertToString(self):
        lLength=self.fieldLength()
        if lLength == 0:
            return ("_unset")
        else:
            return repr(lLength) + '.floor'

    def isPNIField(self, pIdentifier):
        if operator.and_(self.className().find(pIdentifier)==-1, self.fieldName().find(pIdentifier)==-1):
            return True

        return False
        
        
    def showMe(self):
        print ('--------')
        print (self.className() + ":" + self.fieldName() + ":" + self.fieldExternalName() + ":" + self.fieldType() + ":" + repr(self.fieldLength()) + ":" + self.fieldUnit()  + ":" + repr(self.fieldPriority()) + ":" + repr(self.fieldComment()))
        if self.__isJoin():
            print (self.s_field_join_type + ":" + self.s_field_join_to)
        print ('*** FROM ***' + self.fieldFromTable() + '.' + self.fieldFromField())
        print ('--------')
        


if __name__ == "__main__":
    l_cfield = XLSToSWField()

    print ("Test1:" + repr(l_cfield.s_class_name == ''))
    print ("Test2:" + repr(l_cfield.s_field_name == ''))
    print ("Test3:" + repr(l_cfield.s_field_length == 0))
    print ("Test4:" + repr(l_cfield.s_field_priority == 99))

    lCfield2 = XLSToSWField ('slartey', 'bartfarst')
    print ("Test5:" + repr(lCfield2.s_class_name == 'slartey'))
    print ("Test6:" + repr(lCfield2.s_field_name == 'bartfarst'))
    lCfield2.showMe()
    
    



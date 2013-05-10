
import XLSToSWExceptions
import XLSToSWField
import operator
import math

class XLSToSWFieldManager():


    s_fields='No Set'
    


    def __init__(self):
        self.s_fields=[]


    def addField (self, p_field):
        # Checks that the field is allowed to be added and then adds it if all ok
        if self.canAddField(p_field):
            self.s_fields.append(p_field)

    def fieldsInSet(self):
        # Accessor for the s_fields slot
        return self.s_fields

    def numberofFields(self):
        return len(self.s_fields)

    def classesManaged(self):
        # Returns a dictionary of class names in the s_fields set
        lClassNames=[]
        for iField in self.s_fields:
            lClassNames.append(iField.className())
        lClassNames.sort()
        return set(lClassNames)

    def showClassesManaged(self):
        # Prints out the set of classes managed
        lclassesmanaged=self.classesManaged()
        print ('Set of Classnames')
        print (set(lclassesmanaged))
        

    def findField (self, pClassName, pFieldName):
        
        # Returns the XLSToSWField for th epClassName, pFieldName pair
        for iField in self.s_fields:
            if operator.and_((iField.className() == pClassName),(iField.fieldName() == pFieldName)):
                return iField                

        return False


    def findFieldsForClass (self, pClassName):
        lClassFields=[]
        for iField in self.s_fields:
            if (iField.className()==pClassName):
                lClassFields.append(iField)
        return lClassFields

    def findMappingsFromSourceTable (self, pSourceTableName):
        lFields = []
        for iField in self.s_fields:
            if (iField.fieldFromTable().lower()==pSourceTableName.lower()):
                lFields.append(iField)
        return lFields
        
        


    def strClashingNames(self, pBaseproblem, pThisObject, pThatObject):
        lStr = pBaseproblem + ' :'
        lStr = lStr + "(" + pThisObject.className() + ":" + pThisObject.fieldName() + ")"
        lStr = lStr + "(" + pThatObject.className() + ":" + pThatObject.fieldName() + ")"
        return lStr
        

    
    def canAddField (self, p_field):
        
        # Returns true if the field is not already in the set with different attributes
        # Returns true if the field is not in the set
        # Raises a condition (XLSToSWExceptions.InequalityInFields) if the field is already defined with different parameters

        if p_field.className().find(' ')!=-1:
            raise XLSToSWExceptions.TrailingSpaceInClassName (p_field.className)
        if p_field.fieldName().find(' ')!=-1:
            raise XLSToSWExceptions.TrailingSpaceInFieldName (p_field.fieldName)
            

        if p_field.isValidType() == False:
            raise XLSToSWExceptions.InvalidDSType (p_field.fieldType())

        if p_field.isValidJoin() == True:
            if p_field.isValidJoin() == False:
                raise XLSToSWExceptions.InvalidJoinType (p_field.fieldName())

        if float(math.fabs(float(p_field.fieldPriority())))< float(0.001):    
            raise XLSToSWExceptions.PriorityZero ("Adding a field with priority 0??")

        if self.findField (p_field.className(), p_field.fieldName())==False:
            return True
        
        l_field = self.findField (p_field.className(), p_field.fieldName())
        if p_field.fieldExternalName()!=l_field.fieldExternalName():
            raise XLSToSWExceptions.InequalityInFields (self.strClashingNames('External Name', p_field, l_field))
        if p_field.fieldType()!=l_field.fieldType():
            raise XLSToSWExceptions.InequalityInFields (self.strClashingNames('Type', p_field, l_field))
        if p_field.fieldLength()!=l_field.fieldLength():
            raise XLSToSWExceptions.InequalityInFields (self.strClashingNames('Length', p_field, l_field))
        if p_field.fieldUnit()!=l_field.fieldUnit():
            raise XLSToSWExceptions.InequalityInFields (self.strClashingNames('Unit', p_field, l_field))
##        if p_field.fieldComment()!=l_field.fieldComment():
##            raise XLSToSWExceptions.InequalityInFields (self.strClashingNames('Comment', p_field, l_field))
        if p_field.fieldPriority()!=l_field.fieldPriority():
            raise XLSToSWExceptions.InequalityInFields (self.strClashingNames('Priority', p_field, l_field))

            
        # I am here having found the field and it is already the same with no errors
        # I dont need to re-add it,
        # however I will take its comment and add it to the one in store
        l_field.s_field_comment = l_field.s_field_comment + ',' + p_field.s_field_comment
        return False

    def findUpdatedPNIFields (self, pClassName):
        lClassFields=[]
        for iField in self.s_fields:
            if (iField.className()==pClassName):
                if iField.isPNIField():
                    lClassFields.append(iField)

        return lClassFields

    def joinFields (self):
        lFields=[]
        for iField in self.s_fields:
            if iField.isValidJoin():
                lFields.append(iField)
        return lFields
        
    def writeCaseDescription (self, pClassName, pFD=0, pLongOrShortOrCase='long'):
       
        lFields = self.findFieldsForClass(pClassName)
        if (len(lFields)==0):
            raise XLSToSWExceptions.ClassNotManaged (pClassName)
        
        print ("------------- Class: " + pClassName + '----------------')

        if pLongOrShortOrCase=='long':
            for iField in lFields:
                print ('-- Field --')
                print ("Name: " + iField.fieldName())
                print ("External Name: " + iField.fieldExternalName())
                print ("Type: " + iField.fieldType())
                print ("Length: " + repr(iField.fieldLength()))
                print ("Priority: " + repr(iField.fieldPriority()))
                print ('--')
        else:
            print (repr(len(lFields)) + " fields")


    
            
if __name__ == "__main__":
    # Test 1&2 - Make an empty manager
     lFieldManager = XLSToSWFieldManager()
     print ("Test 1:" + repr(lFieldManager.fieldsInSet()==[]))
     print ("Test 2:" + repr(lFieldManager.numberofFields()==0))

     # Test 3 - Add a single field
     lCfield1=XLSToSWField.XLSToSWField('sheath_with_loc', 'length', 'ds_float')
     lFieldManager.addField(lCfield1)
     print ("Test 3:" + repr(lFieldManager.numberofFields()==1))

     # Test 4 - Add another field with the same name, different external name
     # check for a name clash
     lCfield2=XLSToSWField.XLSToSWField('sheath_with_loc', 'length', 'ds_float')
     lCfield2.s_field_external_name='Length'
     lHaveException=False
     try:
         lFieldManager.addField(lCfield2)
     except XLSToSWExceptions.InequalityInFields:
         lHaveException=True
     print ("Test 4:" + repr(lHaveException))

     # Test 5 - check the no of classes managed = 1
     lClassnames = lFieldManager.classesManaged()
     print ("Test 5:" + repr(len(lClassnames)==1))

     # Test 6&7 - add a new field.
     # check no of total records is 2, no. of classes is 2
     lCfield3=XLSToSWField.XLSToSWField('sheath_annotation', 'text', 'ds_uint')
     lFieldManager.addField(lCfield3)
     print ("Test 6:" + repr(lFieldManager.numberofFields()==2))
     print ("Test 7:" + repr(len(lFieldManager.classesManaged())==2))
     
     
     # Test 8&9 - add 2 more fields to sheath_with loc
     # check total no of records is 4, no of fields defined for sheath_with_loc is 3
     lCfield4=XLSToSWField.XLSToSWField('sheath_with_loc', 'pins', 'ds_uint')
     lFieldManager.addField(lCfield4)
     lCfield5=XLSToSWField.XLSToSWField('sheath_with_loc', 'locs', 'ds_uint')
     lFieldManager.addField(lCfield5)
     print ("Test 8:" + repr(lFieldManager.numberofFields()==4))
     print ("Test 9:" + repr(len(lFieldManager.findFieldsForClass('sheath_with_loc'))==3))
                                

     # Test 10, see if it picks up a priority of 0 field
     lCfield10=XLSToSWField.XLSToSWField('sheath_with_loc', 'priorityzero', 'text')
     lCfield10.s_field_priority=0.0
     try:
         lFieldManager.addField(lCfield10)
     except XLSToSWExceptions.PriorityZero:
         lHaveException=True     
     
     lFieldManager.writeCaseDescription ('sheath_with_loc')
                                      
     
     

     
         
        
    

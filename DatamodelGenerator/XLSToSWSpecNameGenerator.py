import XLSToSWExceptions  ##GNGN need a common one of these
import xlrd
import operator


class XLSToSWSpecNameGenerator():

    s_filename='not set'
    s_workbook='not set'
    s_base_folder='C:/CustomerGISs/Cogeco/custom_code/tools/'

     
    def __init__(self, pSpecFilename):
        self.s_filename=self.s_base_folder + pSpecFilename
        self.s_workbook=xlrd.open_workbook(self.s_filename)

    def generateSpecNamesForType(self, pType):

        lsheet = self.s_workbook.sheet_by_index(0)
        if pType=='sheath':
            for irow in range (1, 287):
                lmanu = repr(lsheet.cell_value(irow, 0))
                lname = repr(lsheet.cell_value(irow, 2))
                ltype  = repr(lsheet.cell_value(irow, 3))
                lqty  = repr(int(lsheet.cell_value(irow, 4)))
                larmor= repr(lsheet.cell_value(irow, 6))
                ldiameter= repr(lsheet.cell_value(irow, 7))

                lmyname = lmanu + '/' + lqty + 'F' + '/' + ltype + '/'  + larmor
                if len(lname) > 2:
                    print (lname)
                else:
                    print (lmyname)
        


if __name__== "__main__":

    print ('######### CogecoSpecNameGenerator')
    lSpecNameGenerator = XLSToSWSpecNameGenerator('sheath_specs_v1pt0.xls')
    lSpecNameGenerator.generateSpecNamesForType ('sheath')


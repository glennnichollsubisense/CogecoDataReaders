import CogecoExceptions  ##GNGN need a common one of these
import xlrd
import operator


class CogecoSpecNameGenerator():

    s_filename='not set'
    s_workbook='not set'
    s_base_folder='D:/Documents and Settings/501906310/My Documents/GitHub/CogecoDataReaders/data/'

     
    def __init__(self, pSpecFilename):
        self.s_filename=self.s_base_folder + pSpecFilename
        self.s_workbook=xlrd.open_workbook(self.s_filename)

    def generateSpecNamesForType(self, pType):

        lsheet = self.s_workbook.sheet_by_index(0)
        if pType=='sheath':
            for irow in range (1, 287):
                lmanu = repr(lsheet.cell_value(irow, 0))
                ltype = repr(lsheet.cell_value(irow, 2))
                lqty  = repr(int(lsheet.cell_value(irow, 3)))
                larmor= repr(lsheet.cell_value(irow, 5))
                ldiameter= repr(lsheet.cell_value(irow, 6))

                lname = lmanu + '/' + lqty + 'F' + '/' + ltype + '/'  + larmor
                print (lname)
        


if __name__== "__main__":

    print ('######### CogecoSpecNameGenerator')
    lSpecNameGenerator = CogecoSpecNameGenerator('sheath_specs_v1pt0.xls')
    lSpecNameGenerator.generateSpecNamesForType ('sheath')


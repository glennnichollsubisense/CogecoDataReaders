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
                lmanu = lsheet.cell_value(irow, 0)
                ltype = lsheet.cell_value(irow, 2)
                lqty  = lsheet.cell_value(irow, 3)
                larmor= lsheet.cell_value(irow, 5)
                ldiameter= lsheet.cell_value(irow, 6)

                lname = lmanu + '/' + ltype + '/' + lqty + '/' + larmor + '/' + ldiameter
                print (lname)
        


if __name__== "__main__":

    print ('######### CogecoSpecNameGenerator')
    lSpecNameGenerator = CogecoSpecNameGenerator('sheath_specs_v1pt0.xlsx')
    lSpecNameGenerator.generateSpecNamesForType ('sheath')


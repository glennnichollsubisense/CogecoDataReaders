import CogecoReader

## Provides methods for reading items from the ngf filename defined when the class is instantiated


class CogecoConverter():


    s_reader='not set'

    def __init__(self, pFileName):
        self.s_reader=CogecoReader.CogecoReader(pFileName)

    def findQCFOSCS(self):
        return self.s_reader.findQCFOSCS()

    def findCABLES(self):
        return self.s_reader.findCABLES()

if  __name__=="__main__":

    print ("##########  CogecoConverter")
    lconverter=CogecoConverter("C:/Users/Glenn Nicholls/Documents/Cogeco/mauri.export.ngf")
    for ispec in lconverter.s_reader.findFOSCSpecs('QC'):
        print(ispec)

    lconverter=CogecoConverter("C:/Users/Glenn Nicholls/Documents/Cogeco/3rivieres.export.ngf")
    for ispec in lconverter.s_reader.findFOSCSpecs('QC'):
        print(ispec)


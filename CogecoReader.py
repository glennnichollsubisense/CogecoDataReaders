import mmap

QC_FO_FOSC_IDENTIFIER='38;FO_FOSC'
QC_FO_FOSC_NO_OF_FIELDS=63

QC_FOSC_IDENTIFIER='82;FOSC'
QC_FOSC_NO_OF_FIELDS=21

QC_NODE_IDENTIFIER='48;FO_NODE'
QC_NODE_NO_OF_FIELDS=22

ON_FOSC_NO_OF_FIELDS=1  # to be completed

ON_NODE_IDENTIFIER='12;OPTICAL_BRIDGER'
ON_NODE_NO_OF_FIELDS=107

CABLE_IDENTIFIER='39;FO_CABLE'
CABLE_NO_OF_FIELDS=52

BASE_DATA_FOLDER='C:/Users/Glenn Nicholls/Documents/GitHub/testingangua/data'

class CogecoReader():


    s_filename='not set'
    s_mmap=0
    s_qc_foscs=[]
    s_on_foscs=[]
    s_qc_fo_foscs=[]
    s_qc_nodes=[]
    s_on_nodes=[]
    s_sheaths=[]
    


    def __init__(self, pFileName):
        lfile=open(pFileName)
        self.s_mmap=mmap.mmap(lfile.fileno(), 0, access=mmap.ACCESS_READ)
        s_filename=pFileName

    def __findElements__(self, pElementString, pNoofItems, pCollection):
        lindex=0
        self.s_mmap.seek(lindex)
        while lindex<>-1:
            lindex=self.s_mmap.find(pElementString)
            if lindex==-1:
                break
            self.s_mmap.seek(lindex)
            litem=[]
            for i in range(1,pNoofItems):
                litem.append(self.s_mmap.readline())

            pCollection.append(litem)

        return pCollection  


    def findCABLES(self):
        return self.__findElements__(CABLE_IDENTIFIER, CABLE_NO_OF_FIELDS, self.s_sheaths)
        
    def findONFOSCS(self):
        return self.__findElements__(ON_FOSC_IDENTIFIER, ON_FOSC_NO_OF_FIELDS, self.s_on_foscs)
    def findQCFOSCS(self):
        return self.__findElements__(QC_FOSC_IDENTIFIER, QC_FOSC_NO_OF_FIELDS, self.s_qc_foscs)
    def findQCFOFOSCS(self):
        return self.__findElements__(QC_FO_FOSC_IDENTIFIER, QC_FO_FOSC_NO_OF_FIELDS, self.s_qc_fo_foscs)
    def findQCNODES(self):
        return self.__findElements__(QC_NODE_IDENTIFIER, QC_NODE_NO_OF_FIELDS, self.s_qc_nodes)
    def findONNODES(self):
        return self.__findElements__(ON_NODE_IDENTIFIER, ON_NODE_NO_OF_FIELDS, self.s_on_nodes)


    def resetCollections(self):
        s_qc_foscs=[]
        s_on_foscs=[]
        s_qc_fo_foscs=[]
        s_sheaths=[]
        
    def findFOSCModels(self):
        lFOFOSCS = self.findQCFOFOSCS()
        lFOSCS   = self.findQCFOSCS()

        lmodels=[]
        for ifosc in lFOFOSCS:
            lmodelstr=ifosc[6]
            lfirstsemi=lmodelstr.find(';')
            lmodelstr=lmodelstr[lfirstsemi+1:]
            lsecondsemi=lmodelstr.find(';')
            lmodelstr=lmodelstr[:lsecondsemi]
            lmodels.append (lmodelstr)

        for ifosc in lFOSCS:
            lmodelstr=ifosc[6]
            lfirstsemi=lmodelstr.find(';')
            lmodelstr=lmodelstr[lfirstsemi+1:]
            lmodelstr=lmodelstr[:(len(lmodelstr)-2)]
            lmodels.append (lmodelstr)
            
        return set(lmodels)


    def close(self):
        self.s_mmap.close()

    def findFOSCSpecs(self, pProvince):
        if pProvince=='ON':
            return self.findONFOSCSpecs()
        else:
            return self.findQCFOSCSpecs()
        
    def showFOSCSpecs(self, pFOSCSpecs):
        for ispec in pFOSCSpecs:
            print (ispec)
        

    def findNodeSpecs(self, pProvince):
        if pProvince=='ON':
            return self.findONNodeSpecs()
        else:
            return self.findQCNodeSpecs()

    def showNodeSpecs(self, pNodeSpecs):
        for ispec in pNodeSpecs:
            print (ispec)

    def findONFOSCSpecs(self):
        return 'not yet implemented'

    def findONNodeSpecs(self):
        self.findONNODES()
        
        lspecs=[]
        lspecs.append ('Name,Legacy Model,No. of Fibre Ports, Station Model No.,Manufacturer,Type')
        for inode in self.s_on_nodes:
            lnooffibreports=self.parseEntryWithTwoSemiColons(inode[8])
            lstationnumber=self.parseEntryWithTwoSemiColons(inode[17])            
            lspecs.append (',' + '' + ',' + lnooffibreports + ',' + lstationnumber + ',' + '' + ',Single')    
        
        return set(lspecs)

    def parseEntryWithTwoSemiColons(self, pStr):
        lfirstsemi=pStr.find(';')
        lstr=pStr[lfirstsemi+1:]
        lsecondsemi=lstr.find(';')
        lstr=lstr[:lsecondsemi]
        return lstr
    
    def parseEntryWithOneSemiColon(self, pStr):
        lfirstsemi=pStr.find(';')
        lstr=pStr[lfirstsemi+1:]
        lstr=lstr[:len(lstr)-2]
        return lstr
        

    def findQCNodeSpecs(self):
        self.findQCNODES()
        
        lspecs=[]
        lspecs.append ('Name,Legacy Model,No. of Fibre Ports, Station Model No.,Manufacturer,Type')
        for inode in self.s_qc_nodes:
            lmodelstr=self.parseEntryWithTwoSemiColons(inode[5])
            lmanufacturer=self.parseEntryWithTwoSemiColons(inode[4])            
            lspecs.append (',' + lmodelstr + ',,,' + lmanufacturer + ',Single')    
        
        return set(lspecs)


    def findQCFOSCSpecs(self):
        lFOFOSCS = self.findQCFOFOSCS()
        lFOSCS   = self.findQCFOSCS()

        lspecs=[]
        lspecs.append ('Name,Model,Port Capacity,Tray Capacity,Number of Mounting Sides,Maximum No. of Trays,No. of Trays Included,Maximum No. of Cables,Maximum No. of Fusions,Manufacturer')
        for ifosc in lFOFOSCS:
            lmodelstr=self.parseEntryWithTwoSemiColons(ifosc[6])
            lnb_cable_max=self.parseEntryWithTwoSemiColons(ifosc[15])
            lnb_fusion_max=self.parseEntryWithTwoSemiColons(ifosc[16])
            lmanufacturer=self.parseEntryWithTwoSemiColons(ifosc[4])
            
            lspecs.append (',' + lmodelstr + ',,,,,,' + lnb_cable_max + ',' + lnb_fusion_max + ',' + lmanufacturer)
    

        for ifosc in lFOSCS:
            lmodelstr=self.parseEntryWithOneSemiColon(ifosc[6])
            lmaxtrays=self.parseEntryWithOneSemiColon(ifosc[7])
            lnbtraysincluded=self.parseEntryWithOneSemiColon(ifosc[11])
            lmanufacturer=self.parseEntryWithOneSemiColon(ifosc[5])
            lspecs.append (',' + lmodelstr + ',,,,' + lmaxtrays + ',' + lnbtraysincluded + ',,,' + lmanufacturer)

        return set(lspecs)
        
        
            
if __name__=="__main__":

    print ("#################   CogecoReader")
    lReader=CogecoReader(BASE_DATA_FOLDER + '/test_foscs_nodes_and_cables.ngf')
    lReader.resetCollections()
    lReader.findQCFOFOSCS()
    lReader.findCABLES()        
    ltestctr=1
    print ('Test ' + repr(ltestctr) + ' ' + repr(len(lReader.s_qc_fo_foscs)==3))
    ltestctr+=1
    print ('Test ' + repr(ltestctr) + ' ' + repr(len(lReader.s_sheaths)==2))
    ltestctr+=1
    print ('Test ' + repr(ltestctr) + ' ' + repr(len(lReader.findFOSCModels())==3))
    ltestctr+=1

    lsetfoscspecs=lReader.findFOSCSpecs('QC')
    print ('Test ' + repr(ltestctr) + ' ' + repr(len(lReader.findFOSCSpecs('QC'))==3+1))
    # lReader.showFOSCSpecs(lsetfoscspecs)
    ltestctr+=1

    lsetnodespecs=lReader.findNodeSpecs('QC')
    # lReader.showNodeSpecs(lsetnodespecs)
    
    print ('Test ' + repr(ltestctr) + ' ' + repr(len(lReader.findNodeSpecs('QC'))==3+1))
    ltestctr+=1
    lReader.close()

    lReader=CogecoReader(BASE_DATA_FOLDER + '/test_on_nodes.ngf')
    lsetnodespecs=lReader.findNodeSpecs('ON')
    print ('Test ' + repr(ltestctr) + ' ' + repr(len(lReader.findNodeSpecs('ON'))==2+1))    
    lReader.close()
    

    

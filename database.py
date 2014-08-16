import pickledb
import os


#associates filename with db , can find signature with db better !:) but
class database():
    def __init__(self,homepath='/home/poochi/Desktop/micrecorder/recording'):
        self.DB_NAME = 'record.db'        
        self.homepath = homepath
        #self.homepath = 'C:\\Users\\100555\\Desktop\\micrec\\'
        self.db = pickledb.load(os.path.join(self.homepath,self.DB_NAME),False);
        self.filespresent  = []
        self._load()
        return;

    def _load(self):
        #only one level load
        for eachname in os.listdir(self.homepath):
            eachname = eachname.strip().split('.')[0]
            self.filespresent.append(eachname);

    def getlist(self):
        filesinfo= []
        for eachname in self.filespresent:            
            result = self.db.get(eachname);
            if result == None:
                continue;
            
            files = [];
            files.append(result['Date'])
            files.append(eachname)
            files.append(result['Rating'])
            filesinfo.append(files);

        #we need to add only these files into db
            
        
        return filesinfo;

    def getvalue(self,key):
        res = self.db.get(key)
        #assert(res !=None)
        return res;
            

    def addvalue(self,key,dictionary):
        #returns if appended 
        res = self.db.get(key);
        if res == None:
           self.addfile(key,dictionary);
           
           return True;
        res.update(dictionary);
        self.db.set(key,res);
        print 'adding value'
        self.db.dump();
        return False;
        

    def addfile(self,key,dictionary):
        print type(dictionary)
        #assert(type(dictionary) == type(dict))
        self.db.set(key,dictionary);
        print 'adding file'
        self.db.dump();
        return;

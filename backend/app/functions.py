 #!/usr/bin/python3


#################################################################################################################################################
#                                                    CLASSES CONTAINING ALL THE APP FUNCTIONS                                                                                                    #
#################################################################################################################################################


class DB:

    def __init__(self,Config):

        from math import floor
        from os import getcwd
        from os.path import join
        from json import loads, dumps, dump
        from datetime import timedelta, datetime, timezone 
        from pymongo import MongoClient , errors, ReturnDocument
        from urllib import parse
        from urllib.request import  urlopen 
        from bson.objectid import ObjectId  
       
      
        self.Config                         = Config
        self.getcwd                         = getcwd
        self.join                           = join 
        self.floor                      	= floor 
        self.loads                      	= loads
        self.dumps                      	= dumps
        self.dump                       	= dump  
        self.datetime                       = datetime
        self.ObjectId                       = ObjectId 
        self.server			                = Config.DB_SERVER
        self.port			                = Config.DB_PORT
        self.username                   	= parse.quote_plus(Config.DB_USERNAME)
        self.password                   	= parse.quote_plus(Config.DB_PASSWORD)
        self.remoteMongo                	= MongoClient
        self.ReturnDocument                 = ReturnDocument
        self.PyMongoError               	= errors.PyMongoError
        self.BulkWriteError             	= errors.BulkWriteError  
        self.tls                            = False # MUST SET TO TRUE IN PRODUCTION


    def __del__(self):
            # Delete class instance to free resources
            pass
 


    ####################
    # LAB 4 FUNCTIONS  #
    ####################
    
    # 1. CREATE FUNCTION TO INSERT DATA IN TO THE RADAR COLLECTION
    def insertRadar(self,data):
        try:
            remotedb = self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result = remotedb.ELET2415.radar.insert_one(data)
            
        except Exception as e:
            msg = str(e)
            if "duplicate" not in msg:
                print("insertRadar error ",msg)
                return False
        else:                  
            return True


    
    # 2. CREATE FUNCTION TO RETRIEVE ALL DOCUMENTS FROM RADAR COLLECT BETWEEN SPECIFIED DATE RANGE. MUST RETURN A LIST OF DOCUMENTS
    def objectRetrieve(self,start, end):
        '''RETURNS A LIST OF OBJECTS. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        try:
            start = int(start)
            end = int(end)
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.radar.find({'timestamp': {'$gte': start, '$lte': end}},{"_id":0} ).sort('timestamp', 1))
        except Exception as e:
            msg = str(e)
            print("obejectRetrieve error, ",msg)            
        else:                  
            return result


    # 3. CREATE A FUNCTION TO COMPUTE THE ARITHMETIC AVERAGE ON THE 'reserve' FEILED/VARIABLE, USING ALL DOCUMENTS FOUND BETWEEN SPECIFIED START AND END TIMESTAMPS. RETURNS A LIST WITH A SINGLE OBJECT INSIDE
    def getAverage(self,start,end):
        try:
            start = int(start)
            end = int(end)
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.radar.aggregate([ 
                { '$match': 
                    { 'timestamp': { '$gte': start, '$lte': end } } },

                { '$group': 
                    { '_id': None, 'avg': { '$avg': '$reserve' } } }, 
                
                { '$project': 
                    { '_id': 0 } } 
            ]))

        except Exception as e:
            msg = str(e)
            print("getAverage error ",msg)            
        else:                  
            return result
    
    # 4. CREATE A FUNCTION THAT INSERT/UPDATE A SINGLE DOCUMENT IN THE 'codef create_or_update_passcode(passcode):    
    def create_or_update_passcode(self,passcode):
        try:
            if len(passcode)== 4 and type(passcode)== "int":
                remotedb = self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
                result = remotedb.ELET2415.code.find_one_and_update(
                            {'type': "passcode"},
                            {'$set': {"type":"passcode","code":passcode}},
                            {'_id': 0},
                            upsert=True)
        except Exception as e:
            msg = str(e)
            if "duplicate" not in msg:
                print("create_or_update error ",msg)
                return False
        else:                  
            return result
    
    # 5. CREATE A FUNCTION THAT RETURNS A COUNT, OF THE NUMBER OF DOCUMENTS FOUND IN THE 'code' COLLECTION WHERE THE 'code' FEILD EQUALS TO THE PROVIDED PASSCODE.
    #    REMEMBER, THE SCHEMA FOR THE SINGLE DOCUMENT IN THE 'code' COLLECTION IS {"type":"passcode","code":"0070"}
    def check_passcode(self,passcode):
    # Check if the 'code' field equals the provided passcode
        try:
            passcode= int(passcode)
            remotedb = self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            count = remotedb.ELET2415.code.count_documents({"type": "passcode", "code": passcode})
            if count > 0:
                return True
            else:
                return False
            
        except Exception as e:
            msg = str(e)
            print("check_passcode error ",msg)  


   



def main():
    from config import Config
    from time import time, ctime, sleep
    from math import floor
    from datetime import datetime, timedelta
    one = DB(Config)
 
 
    start = time() 
    end = time()
    print(f"completed in: {end - start} seconds")
    
if __name__ == '__main__':
    main()


    

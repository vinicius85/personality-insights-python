import ibm_db
import json
import os

class SqlDBService:

    def __init__(self, vcapServices):  

        db = "SQLDB"
        hostname="75.126.155.153"
        port = "50000"
        username="user10417"
        password="OthtJGpiqa8E"

        if vcapServices is not None: 
            db2info = json.loads(os.environ['VCAP_SERVICES'])['sqldb'][0]  
            db2cred = db2info["credentials"]
            self.sqlConn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
        else:
            self.sqlConn = ibm_db.connect("DATABASE="+db+";HOSTNAME="+hostname+";PORT="+port+";UID="+username+";PWD="+password+";","","")  
            
    
    def listInsights(self):
        if self.sqlConn:
            stmt = ibm_db.exec_immediate(self.sqlConn,"select * from insights order by id desc")    
            print stmt
            result = ibm_db.fetch_assoc(stmt)    
            print result
            return result
        else:
            print("ERROR: Connection not found")


    def saveInsight(self, snippet, insightJson):

        insight = json.loads(insightJson)
        print(type(insight))
        bigFive = insight['tree']['children'][0]['children'][0]['children'][0]['name']
        bigFivePerc = insight['tree']['children'][0]['children'][0]['children'][0]['percentage']
        snippet = snippet.replace(",", "") 
        snippet = snippet.replace(".", "")    
        
        if self.sqlConn:
          result = ibm_db.exec_immediate(self.sqlConn,"insert into insights (TEXT_SNIPPET, BIG_FIVE, BIG_FIVE_PERCENTAGE) values('"+str(snippet)+"' , '"+str(bigFive)+"' , '"+str(bigFivePerc)+"' )")
          if result:
            rows = ibm_db.num_rows(result)
            print "affected row:", rows
            return rows

        else:
            print("ERROR: Connection not found")
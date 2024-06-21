import sqlalchemy as db 
from datetime import datetime 
from sqlalchemy.dialects import postgresql

class PriceWatchDB:

    def __init__(self):
        try:
            self.engine = db.create_engine("postgresql+psycopg2://localhost:5432/pricewatchdb")
            self.connection = self.engine.connect()
            self.metadata = db.MetaData()
            print("Database Connection Successful")
        except Exception as e:
            print("Error Occured Connection Database\n")
            print(e)
            return -2 
    
    # Functions for Bearings 
    def getBearingSizes(self):
        try:
            ResultSet = []
            bearings_sizes = db.Table('bearing_sizes',self.metadata,autoload_with=self.engine)
            query = db.Select(bearings_sizes)
            result = self.connection.execute(query)
            for i in result:
                ResultSet.append(i._asdict()["sizes"])
            return ResultSet
        except Exception as e:
            print("Internal Server Error Detected:\n")
            print(e)
            return {"message": "Internal Server Error", "Exception Message":str(e)}
    
    def addBearings(self,size,vendor_id,rate,bill_rate):
        # skipping check if vendor and size exists (need to add later)
        try:
            bearings = db.Table('bearings',self.metadata,autoload_with=self.engine)
            timestamp = datetime.now()
            query = db.insert(bearings).values(size=size,vendor_id=vendor_id,rate=rate,bill_rate=bill_rate,date_added=timestamp)
            self.connection.execute(query)
            self.connection.commit()
            return {"message":"Row Added Successfully"}
        
        except Exception as e:
            print("Internal Server Error Detected:\n")
            print(e)
            return {"message": "Internal Server Error", "Exception Message":str(e)}
            

    def getBearings(self,size,vendor_id):
        try:
            ResultSet = []
            bearings = db.Table('bearings',self.metadata,autoload_with=self.engine)
            query = db.Select(bearings).where((bearings.c.size==size) & (bearings.c.vendor_id==vendor_id))
            result = self.connection.execute(query)
            for i in result:
                ResultSet.append(i._asdict())
            return ResultSet
    
        except Exception as e:
            print("Internal Server Error Detected:\n")
            print(e)
            return {"message": "Internal Server Error", "Exception Message":str(e)}  
        
    # Get Vendors
    def getVendors(self,vendor_type):
        try:
            ResultSet = []
            vendors = db.Table('vendors',self.metadata,autoload_with=self.engine)
            query = db.Select(vendors).where(vendors.c.vendor_type == vendor_type)
            result = self.connection.execute(query)
            for i in result:
                ResultSet.append(i._asdict()["vendor_name"])
            return ResultSet 
        
        except Exception as e:
            print("Internal Server Error Detected:\n")
            print(e)
            return {"message": "Internal Server Error", "Exception Message":str(e)}
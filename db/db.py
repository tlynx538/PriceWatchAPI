import sqlalchemy as db 
from datetime import datetime 
from sqlalchemy.dialects import postgresql
from fastapi import HTTPException
class PriceWatchDB:
    def __init__(self):
        try:
            self.engine = db.create_engine("postgresql+psycopg2://localhost:5432/pricewatchdb")
            self.connection = self.engine.connect()
            self.metadata = db.MetaData()
            print("Database Connection Successful")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
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
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    def addBearings(self,size,vendor_name,rate,bill_rate):
        # skipping check if vendor and size exists (need to add later)
        try:
            bearings = db.Table('bearings',self.metadata,autoload_with=self.engine)
            vendor_id = self.getVendorID(vendor_type='Bearings',vendor_name=vendor_name)
            timestamp = datetime.now()
            query = db.insert(bearings).values(size=size,vendor_id=vendor_id,rate=rate,bill_rate=bill_rate,date_added=timestamp)
            self.connection.execute(query)
            self.connection.commit()
            return {"message":"Row Added Successfully"}
        
        except Exception as e:
            self.connection.rollback() # rollback in case of error
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
            

    def getBearings(self,size,vendor_name):
        try:
            ResultSet = []
            bearings = db.Table('bearings',self.metadata,autoload_with=self.engine)
            vendors = db.Table('vendors',self.metadata,autoload_with=self.engine)

            # Get Vendor ID
            query = db.Select(vendors).where((vendors.c.vendor_type == "Bearings")&(vendors.c.vendor_name == vendor_name))
            result = self.connection.execute(query)
            vendor_id = 0

            for i in result:
                vendor_id = i._asdict()["vendor_id"]
                break
            query = db.Select(bearings).where((bearings.c.size==size) & (bearings.c.vendor_id==vendor_id))
            result = self.connection.execute(query)
            for i in result:
                ResultSet.append(i._asdict())
            ResultSet = ResultSet[::-1]
            return ResultSet
    
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
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
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    # Get Vendor ID
    def getVendorID(self, vendor_type, vendor_name):
        try:
            ResultSet =[]
            vendors = db.Table('vendors',self.metadata,autoload_with=self.engine)
            query = db.Select(vendors).where((vendors.c.vendor_type == vendor_type) & (vendors.c.vendor_name == vendor_name))
            result = self.connection.execute(query)
            for i in result:
                ResultSet.append(i._asdict()["vendor_id"])
            return ResultSet[0]
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    

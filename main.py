from fastapi import FastAPI
from db.db import PriceWatchDB
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime 

origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = PriceWatchDB()

class Bearings(BaseModel):
    size: str
    vendor_id: int
    rate: float 
    bill_rate: float 

class GetBearings(BaseModel):
    size: str
    vendor_id: int

@app.get('/')
def home():
    return {"PriceWatch API v0.1"}

@app.get('/bearings/sizes')
def bearingSizes():
    return db.getBearingSizes()
 
@app.post('/bearings')
def addBearings(br: Bearings):
    return db.addBearings(size=br.size,vendor_id=br.vendor_id,rate=br.rate,bill_rate=br.bill_rate)

@app.get('/bearings')
def getBearings(br: GetBearings):
    return db.getBearings(size=br.size,vendor_id=br.vendor_id)

@app.get('/vendors/'+'{vendor_type}')
def vendors(vendor_type):
    return db.getVendors(vendor_type=vendor_type)
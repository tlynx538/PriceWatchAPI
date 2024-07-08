from fastapi import FastAPI
from db.db import PriceWatchDB
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime 

origins = [
    "http://localhost:3000",
    "*",
    "http://192.168.0.131:3000"

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
    vendor_name: str
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
    return db.addBearings(size=br.size,vendor_name=br.vendor_name,rate=br.rate,bill_rate=br.bill_rate)

@app.get('/bearings/'+'{size}'+'/'+'{vendor_name}')
def getBearings(size,vendor_name):
    return db.getBearings(size=size,vendor_name=vendor_name)

@app.get('/vendors/'+'{vendor_type}')
def vendors(vendor_type):
    return db.getVendors(vendor_type=vendor_type)
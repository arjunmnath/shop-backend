from __future__ import annotations
from typing import List
from pydantic import EmailStr, Field, BaseModel 
from datetime import datetime
from bson import ObjectId


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        try:
            ObjectId(v)
        except Exception as e:
            raise ValueError(f'Invalid ObjectId: {e}')
        return v


class Customer(BaseModel):
    name: str = Field(default="")
    phone: str = Field(default="")
    email: EmailStr | None = Field(default=None)
    balance: float = Field(default=0)
    addresses: List[Address]


class Address(BaseModel):
    line1: str = Field(default="")
    line2: str = Field(default="")
    city: str = Field(default="")
    pincode: int = Field(default=0)
        
    
class Products(BaseModel):
    name: str = Field(default="")
    costPrice: float = Field(default=0.0)
    sellingPrice: float = Field(default=0.0)
    stock: int = Field(default=0)
    stockUpdate: datetime = Field(default=datetime.now())
    

class Sales(BaseModel): 
    customerId: ObjectIdStr = Field(default="")
    productId: ObjectIdStr = Field(default="")
    site: int = Field(default=0)
    quantity: int = Field(default=0)
    isCredit: bool = Field(default=False)
    hasLoadingFee: bool = Field(default=False)
    date: datetime = Field(default=datetime.now())
    terms: str = Field(default='')
    transactionId: str = Field(default='', optional=True)
    

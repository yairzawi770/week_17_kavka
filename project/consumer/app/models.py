from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional


class Customer(BaseModel):
    type: Optional[str]
    customerNumber: int
    customerName: Optional[str]
    contactLastName: Optional[str]
    contactFirstName: Optional[str]
    phone: Optional[str] = Field(None, min_length=9, max_length=15)
    addressLine1: Optional[str]
    addressLine2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postalCode: Optional[str]
    country:Optional[str] = Field(None, min_length=2)
    salesRepEmployeeNumber: int
    creditLimit: Optional[str]

class Order(BaseModel):
    type: Optional[str]
    orderNumber: int
    orderDate:  Optional[str]
    requiredDate: Optional[str]
    shippedDate: Optional[str]
    status: Optional[str]
    comments: Optional[str]
    customerNumber: Optional[str]

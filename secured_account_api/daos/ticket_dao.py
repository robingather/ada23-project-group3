from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, TIMESTAMP

from db import Base


class TicketDAO(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True) # Auto generated primary key
    start_date = Column(DateTime)
    purchase_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    price = Column(Float)
    code = Column(String)
    account_email = Column(Integer, ForeignKey('accounts.email_address'))

    def __init__(self, start_date, purchase_date, end_date, status, price, code, account_email):
        self.start_date = start_date
        self.purchase_date = purchase_date
        self.end_date = end_date
        self.status = status
        self.price = price
        self.code = code
        self.account_email = account_email

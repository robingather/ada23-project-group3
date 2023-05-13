from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from db import Base


class AccountDAO(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto generated primary key
    first_name = Column(String)
    last_name = Column(String)
    email_address = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(String)
    automatic_topup = Column(Boolean)
    amount_topup = Column(Integer)

    # reference to status as foreign key relationship. This will be automatically assigned.
    # status_id = Column(Integer, ForeignKey('status.id'))
    # https: // docs.sqlalchemy.org / en / 14 / orm / basic_relationships.html
    # https: // docs.sqlalchemy.org / en / 14 / orm / backref.html
    # status = relationship(StatusDAO.__name__, backref=backref("account", uselist=False))

    def __init__(self, first_name, last_name, email_address, password, user_type, automatic_topup, amount_topup):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password
        self.user_type = user_type
        self.automatic_topup = automatic_topup
        self.amount_topup = amount_topup

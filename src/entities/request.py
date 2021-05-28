from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer
from .entity import Base

class Request(Base):
    __tablename__ = 'requests'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    path = Column(String)
    host = Column(String)
    requested_at = Column(String)

    def __init__(self, ip, path, host, requested_at):
        self.ip = ip
        self.path = path
        self.host = host
        self.requested_at = requested_at


class RequestSchema(Schema):

    id = fields.Number()

    ip = fields.Str()

    path = fields.Str()

    host = fields.Str()

    requested_at = fields.Str()
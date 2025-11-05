import sqlalchemy as sa
from sqlalchemy import create_engine
from decimal import Decimal
from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, String, Text, DECIMAL, Date, Time, Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.base import state_attribute_str
from sqlalchemy.sql import operators
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import UniqueConstraint, Index
from sqlalchemy.sql.sqltypes import Float
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
from sqlalchemy.sql import func

DbBase = declarative_base()


#设备表
class Device(DbBase):
    """用户资金表每日备份"""
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    
    device_id = Column(String(), comment="设备id")
    gatewayname = Column(String(), comment="gatewayname")
    mac = Column(String(), comment="mac")
    
    hostname = Column(String(), comment="hostname")
    dhcp_server = Column(String(), comment="dhcp_server")
    disk_serial = Column(String(), comment="disk_serial")
    board_serial = Column(String(), comment="board_serial")
    cpu_cores = Column(Integer(), comment="cpu_cores")
    cpu_model = Column(String(), comment="cpu_model")
    disk_total  = Column(String(), comment="disk_total")
    disk_used = Column(String(), comment="disk_used")
    disk_avail = Column(String(), comment="disk_avail")
    disk_usage_percent = Column(String(), comment="disk_usage_percent")
    mem_total = Column(String(), comment="mem_total")
    mem_used = Column(String(), comment="mem_used")
    mem_free = Column(String(), comment="mem_free")
    mem_usage_percent = Column(String(), comment="mem_usage_percent")
    ip = Column(String(), comment="ip")
    status = Column(String(), comment="status")
    create_time = Column(DateTime(timezone=True), comment="创建时间")
    update_time = Column(DateTime(timezone=True), comment="更新时间")
    
    __table_args__ = (
        Index('device_idx1', 'gatewayname'),
        Index('device_idx2', 'mac'),
        UniqueConstraint('gatewayname', name='device_uq1'),
    )
        


#用户行为表
class UserBehavior(DbBase):
    """用户行为表"""
    __tablename__ = 'user_behavior'

    id = Column(Integer, primary_key=True)
    
    session_id = Column(String(), comment="session_id")
    gatewayname = Column(String(), comment="gatewayname")
    browser = Column(String(), comment="browser")
    os = Column(String(), comment="os")
    device = Column(String(), comment="device")
    
    action = Column(String(), comment="action")
    action_data = Column(String(), comment="action_data")
    create_time = Column(DateTime(timezone=True), comment="创建时间")
    
    __table_args__ = (
        Index('user_behavior_idx1', 'gatewayname'),
        Index('user_behavior_idx2', 'session_id'),
    )
        

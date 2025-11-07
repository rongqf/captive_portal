

from fastapi import APIRouter, Request, Depends, BackgroundTasks
import os
from loguru import logger
from datetime import datetime
from dependencies.user_agent import get_user_agent_info
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models.base import Device, UserBehavior, DbBase
import json
import pandas as pd 
import numpy as np
from utils.pd import df_to_sql

router = APIRouter(prefix='/device/data')


def process_device_data(data: dict):
    gatename = data['gate_name']
    msgtype = data['type']
    time = pd.to_datetime(data['timestamp'])
    
    logger.info(f"处理设备数据: {data['data']}")
    df = pd.DataFrame([data['data']])
    logger.info(f"处理设备数据: {df}")
    df['gatewayname'] = gatename
    del df['time']
    del df['os']
    del df['dhcp_lease_time']
    del df['cpu_usage']
    df = df.replace('N/A', np.nan).infer_objects(copy=False)
    
    df_to_sql(df, 'device', elements=['gatewayname'])


@router.post("/upload")
def upload(request: Request, data: dict, background_tasks: BackgroundTasks):
    """接收设备数据并放入后台任务队列"""
    try:
        logger.info(f"接收到设备数据: {data}")
        # 将数据放入后台任务队列
        background_tasks.add_task(process_device_data, data)
        return {'ok': True, 'data': {}}
        
    except Exception as e:
        logger.error(f"设备数据接收失败: {str(e)}")
        return  {'ok': False, 'data': {}}




from fastapi import APIRouter, Request, Depends, BackgroundTasks
import os
from loguru import logger
from datetime import datetime
from dependencies.user_agent import get_user_agent_info
import pandas as pd 
import numpy as np
from utils.pd import df_to_sql

router = APIRouter(prefix='/userbehavior/data')


def process_user_data(session_id, gate_name, user_agent_info, data):
    data = {}
    data['session_id'] = session_id
    data['gatewayname'] = gate_name
    data['create_time'] = datetime.now()
    data['action'] = data.get('action')
    data['action_data'] = data.get('actionData')

    df = pd.DataFrame([data])
    df_to_sql(df, 'user_behavior')

    pass

@router.post("/upload")
async def upload(
    request: Request, 
    data: dict,
    background_tasks: BackgroundTasks,
    user_agent_info: dict = Depends(get_user_agent_info),
    ):
    
    session_id = request.cookies.get("session_id")
    gate_name = request.cookies.get("gate_name")
    logger.info(f"session_id: {session_id}")
    logger.info(data)
    #logger.info(user_agent_info)
    
    background_tasks.add_task(process_user_data, session_id, gate_name, user_agent_info, data)
        
    return {'ok': True, 'data': {}}

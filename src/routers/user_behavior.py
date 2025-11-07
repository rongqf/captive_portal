

from fastapi import APIRouter, Request, Depends, BackgroundTasks
import os
from loguru import logger
from datetime import datetime
from dependencies.user_agent import get_user_agent_info

router = APIRouter(prefix='/userbehavior/data')


def process_user_data(session_id, user_agent_info, data):
    pass

@router.post("/upload")
async def upload(
    request: Request, 
    data: dict,
    background_tasks: BackgroundTasks,
    user_agent_info: dict = Depends(get_user_agent_info),
    ):
    
    session_id = request.cookies.get("session_id")
    logger.info(f"session_id: {session_id}")
    logger.info(data)
    logger.info(user_agent_info)
    
    background_tasks.add_task(process_user_data, session_id, user_agent_info, data)
        
    return {'ok': True, 'data': {}}

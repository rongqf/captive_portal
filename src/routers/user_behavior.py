

from fastapi import APIRouter, Request, Depends
import os
from loguru import logger
from datetime import datetime
from dependencies.user_agent import get_user_agent_info

router = APIRouter(prefix='/userbehavior/data')


@router.post("/upload")
async def upload(
    request: Request, 
    data: dict,
    user_agent_info: dict = Depends(get_user_agent_info)
    ):
    session_id = request.cookies.get("session_id")
    logger.info(f"session_id: {session_id}")
    logger.info(data)
    
    logger.info(user_agent_info)
    
    return {'ok': True, 'data': {}}

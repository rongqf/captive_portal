

from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
import os, random
from datetime import datetime
from loguru import logger
from dependencies.user_agent import get_basic_user_agent_info
import uuid

router = APIRouter(
    prefix='/auth/wifidogx',
    tags=['wifidogx']  
)
templates = Jinja2Templates(directory=os.path.join("templates"))


@router.get("/login/")
async def login(
    request: Request,
    response: Response,
    user_agent_info: dict = Depends(get_basic_user_agent_info)
):
    # 解析GET请求的查询参数
    input = dict(request.query_params)
    
    
    # 记录用户访问信息
    logger.info(f"登录页面访问 - 查询参数: {input}")
    logger.info(f"用户设备信息: {user_agent_info}")
    
    gw_address = input.get('gw_address')
    gw_port = input.get('gw_port')
    gw_id = input.get('gw_id')
    token = datetime.now().strftime('%Y%m%d%H%M%S-') + str(random.randint(1000, 9999))
    redirect_url = 'http://%s:%s/wifidog/auth?token=%s&gw_id=%s' % (gw_address, gw_port, token, gw_id)
    
    logger.info(f"重定向URL: {redirect_url}")
    
    response = templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={"redirect_url": redirect_url}
    )
    session_token = f"session_{uuid.uuid4()}"
    response.set_cookie(
        key="session_id", 
        value=session_token,
        path="/",  # 对整个站点有效
        httponly=True,  # 防止XSS攻击
        secure=False,  # 开发环境设为False，生产环境设为True
        samesite="lax"  # 防止CSRF攻击
    )
    return response


@router.get("/auth/")
@router.post("/auth/")
async def auth(
    request: Request,
    user_agent_info: dict = Depends(get_basic_user_agent_info)
):
    # 解析查询参数
    input = dict(request.query_params)
    
    # 检查cookie
    session_cookie = request.cookies.get("session_id")
    all_cookies = request.cookies
    
    logger.info(f"认证请求 - 查询参数: {input}")
    logger.info(f"认证用户设备信息: {user_agent_info}")
    logger.info(f"接收到的Session Cookie: {session_cookie}")
    logger.info(f"所有Cookies: {all_cookies}")
    logger.info(f"请求头中的Cookie: {request.headers.get('cookie', 'None')}")
    
    if input.get('stage') == 'counters_v2':
        return {}
    
    # 根据cookie存在与否返回不同的认证结果
    if session_cookie:
        return f'Auth: 1 (Session: {session_cookie})'
    else:
        return 'Auth: 1 (No Session)'


@router.get("/portal/")
async def ok(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="ok.html"
    )
    
@router.get("/ping/")
async def ping(request: Request):
    # 解析查询参数，而不是表单数据
    input_dict = dict(request.query_params)
    logger.info(f"Ping request: {input_dict}")
    return 'Pong'


from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os
from loguru import logger
import uuid

router = APIRouter(
    prefix='/auth/opennds',
    tags=['opennds']  
)
templates = Jinja2Templates(directory=os.path.join("templates"))


#/?authaction=http://192.168.9.1:2050/opennds_auth/?clientip=192.168.9.135&gatewayname=OpenWrt%20openNDS&tok=aeb0a0b3&redir=http%3a%2f%2fcaptive.apple.com%2fhotspot-detect.html
@router.get("/")
async def login(
    request: Request
    ):
    # 解析GET请求的查询参数
    input = dict(request.query_params)
    # 记录日志
    logger.info(input)
        
    if input.get('authaction'):
        redir = 'http://192.168.50.242:8000/auth/opennds/ok'
        redirect_url = '%s&tok=%s&redir=%s' % (
            input.get('authaction'), 
            input.get('tok'), 
            redir, #input.get('redir')
        )
        logger.info(redirect_url)
        response =  templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"redirect_url": redirect_url}
        )
        # 在返回响应对象之前设置cookie
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
    else:
        return '已经登录'
        

@router.get("/ok")
async def ok(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="ok.html"
    )
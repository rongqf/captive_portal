import os
import sys
from fastapi import FastAPI, Request, Response

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
#from configs import settings
from fastapi import applications
from loguru import logger
import uuid
from fastapi.templating import Jinja2Templates
 
from routers import auth_opennds
from routers import device_data
from routers import auth_wifidogx
from routers import user_behavior

app = FastAPI(
    # docs_url=None,
    debug=True,#settings.DEBUG,
    title="captive portal",
    description="Session Restful API",
    version="0.1.0",
)

origins = [
    "http://192.168.50.242:8000",  # 假设前端运行在 3000 端口
    "http://127.0.0.1:8001",  # 假设前端运行在 3000 端口
    "http://106.53.56.43:8001",  # 假设前端运行在 3000 端口
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 明确指定来源，而非 ["*"]
    allow_credentials=True,  # 关键：允许携带凭据（Cookie）
    allow_methods=["*"],     # 允许的 HTTP 方法
    allow_headers=["*"],      # 允许的 HTTP 头
)

# logger.add(
#     "app.log",
#     format="{time} [{extra[request_id]}] {level} - {message}",
#     rotation="1 day",  # 每天轮换一个日志文件
#     retention="7 days",  # 保留7天的日志
#     encoding="utf-8",
#     backtrace=True,  # 记录异常回溯
#     diagnose=True,
# )
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}:{function}</cyan> |  <cyan>{extra[request_id]}</cyan> | <level>{message}</level>",
    level="INFO",
    colorize=True,  # 启用颜色，使输出更清晰
)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    # 为每个请求生成唯一 ID
    request_id = str(uuid.uuid4())
    # 获取cookie中的session_id
    session_id = request.cookies.get("session_id", "None")
    # 将 request_id 注入到 Loguru 的上下文
    with logger.contextualize(request_id=request_id):
        logger.info("Request started - Session ID: %s" % session_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info("Request ended - Session ID: %s" % session_id)
    return response


@app.get("/")
def index():
    logger.info("index")
    return {"message": "Hello World"}

@app.get("/test")
def test(request: Request):
    # 检查cookie
    all_cookies = request.cookies
    logger.info(f"所有Cookies: {all_cookies}")
    
    session_token = f"session_{uuid.uuid4()}"
    
    logger.info("test")
    templates = Jinja2Templates(directory=os.path.join("templates"))
    
    # 创建响应对象并设置cookie
    response = templates.TemplateResponse(
        request=request, 
        name="test_cookie.html",
    )
    
    # 在返回响应对象之前设置cookie
    response.set_cookie(
        key="session_id", 
        value=session_token,
        max_age=3600,  # 1小时过期
        path="/",  # 对整个站点有效
        httponly=True,  # 防止XSS攻击
        secure=False,  # 开发环境设为False，生产环境设为True
        samesite="lax"  # 防止CSRF攻击
    )
    
    return response




app.mount("/static", StaticFiles(directory='./static'))
app.include_router(auth_opennds.router)
app.include_router(device_data.router)
app.include_router(auth_wifidogx.router)
app.include_router(user_behavior.router)





from fastapi import APIRouter, Request, Depends
import os
from loguru import logger
from datetime import datetime
from dependencies.user_agent import get_user_agent_info

router = APIRouter(prefix='/device/data')


@router.post("/upload")
async def upload(request: Request, data: dict):
    
    logger.info(data)
    return {'ok': True, 'data': {}}


@router.post("/info/")
async def receive_device_info(
    request: Request,
    user_agent_info: dict = Depends(get_user_agent_info)
):
    """接收前端上报的navigator数据并解析"""
    try:
        # 获取请求体数据
        navigator_data = await request.json()
        
        # 添加时间戳和IP地址
        navigator_data['timestamp'] = datetime.now().isoformat()
        navigator_data['client_ip'] = request.client.host if request.client else 'Unknown'
        
        # 使用依赖注入的user-agent信息
        navigator_data['server_user_agent_parsed'] = user_agent_info
        navigator_data['server_user_agent_raw'] = request.headers.get('user-agent', 'Unknown')
        
        # 解析navigator数据
        parsed_info = parse_navigator_data(navigator_data)
        
        # 合并user-agent解析结果
        parsed_info['server_user_agent'] = user_agent_info
        
        # 记录解析后的信息
        logger.info(f"设备信息上报 - 解析结果: {parsed_info}")
        
        # 这里可以添加数据库存储逻辑
        # 例如：save_to_database(parsed_info)
        
        return {
            'ok': True, 
            'message': '设备信息接收成功',
            'parsed_info': parsed_info,
            'raw_data': navigator_data,
            'user_agent_analysis': user_agent_info
        }
        
    except Exception as e:
        logger.error(f"接收设备信息错误: {str(e)}")
        return {
            'ok': False, 
            'message': f'设备信息接收失败: {str(e)}'
        }


def parse_navigator_data(navigator_data: dict) -> dict:
    """解析navigator数据，提取有用的设备信息"""
    parsed = {}
    
    # 从userAgent解析操作系统和浏览器
    user_agent = navigator_data.get('userAgent', '')
    
    # 操作系统检测
    if 'Windows' in user_agent:
        parsed['operating_system'] = 'Windows'
    elif 'Mac' in user_agent:
        parsed['operating_system'] = 'Mac OS'
    elif 'Linux' in user_agent:
        parsed['operating_system'] = 'Linux'
    elif 'Android' in user_agent:
        parsed['operating_system'] = 'Android'
    elif 'iOS' in user_agent or 'iPhone' in user_agent or 'iPad' in user_agent:
        parsed['operating_system'] = 'iOS'
    else:
        parsed['operating_system'] = 'Unknown'
    
    # 设备类型检测
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        parsed['device_type'] = 'Mobile'
    elif 'Tablet' in user_agent or 'iPad' in user_agent:
        parsed['device_type'] = 'Tablet'
    else:
        parsed['device_type'] = 'Desktop'
    
    # 浏览器检测
    if 'Chrome' in user_agent and 'Edg' not in user_agent:
        parsed['browser'] = 'Chrome'
    elif 'Firefox' in user_agent:
        parsed['browser'] = 'Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        parsed['browser'] = 'Safari'
    elif 'Edg' in user_agent:
        parsed['browser'] = 'Edge'
    elif 'Opera' in user_agent:
        parsed['browser'] = 'Opera'
    else:
        parsed['browser'] = 'Unknown'
    
    # 直接可用的信息
    parsed['language'] = navigator_data.get('language', 'Unknown')
    parsed['platform'] = navigator_data.get('platform', 'Unknown')
    parsed['vendor'] = navigator_data.get('vendor', 'Unknown')
    parsed['cookie_enabled'] = navigator_data.get('cookieEnabled', False)
    parsed['java_enabled'] = navigator_data.get('javaEnabled', False)
    parsed['hardware_concurrency'] = navigator_data.get('hardwareConcurrency', 'Unknown')
    parsed['max_touch_points'] = navigator_data.get('maxTouchPoints', 0)
    parsed['online'] = navigator_data.get('onLine', False)
    
    # 屏幕信息
    screen_info = navigator_data.get('screen', {})
    parsed['screen_resolution'] = f"{screen_info.get('width', 0)}x{screen_info.get('height', 0)}"
    parsed['screen_avail_resolution'] = f"{screen_info.get('availWidth', 0)}x{screen_info.get('availHeight', 0)}"
    parsed['color_depth'] = screen_info.get('colorDepth', 0)
    parsed['pixel_depth'] = screen_info.get('pixelDepth', 0)
    
    # 页面信息
    page_info = navigator_data.get('pageInfo', {})
    parsed['page_url'] = page_info.get('url', 'Unknown')
    parsed['referrer'] = page_info.get('referrer', 'Direct')
    parsed['page_title'] = page_info.get('title', 'Unknown')
    
    # 时区
    parsed['timezone'] = navigator_data.get('timezone', 'Unknown')
    
    # 事件类型
    parsed['event_type'] = navigator_data.get('event_type', 'unknown')
    
    # 客户端信息
    parsed['client_ip'] = navigator_data.get('client_ip', 'Unknown')
    parsed['timestamp'] = navigator_data.get('timestamp', 'Unknown')
    
    return parsed
        

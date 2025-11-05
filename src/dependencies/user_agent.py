"""
User-Agent解析依赖注入模块
"""
from typing import Dict, Any
from user_agents import parse
from fastapi import Request, Depends
from loguru import logger


class UserAgentParser:
    """User-Agent解析器"""
    
    def __init__(self, user_agent_string: str):
        self.user_agent_string = user_agent_string
        self.parsed_ua = parse(user_agent_string)
    
    def get_basic_info(self) -> Dict[str, Any]:
        """获取基础信息"""
        return {
            "browser": {
                "family": self.parsed_ua.browser.family,
                "version": self.parsed_ua.browser.version_string,
                "is_bot": self.parsed_ua.is_bot
            },
            "os": {
                "family": self.parsed_ua.os.family,
                "version": self.parsed_ua.os.version_string
            },
            "device": {
                "family": self.parsed_ua.device.family,
                "brand": self.parsed_ua.device.brand,
                "model": self.parsed_ua.device.model,
                "is_mobile": self.parsed_ua.is_mobile,
                "is_tablet": self.parsed_ua.is_tablet,
                "is_pc": self.parsed_ua.is_pc,
                "is_touch_capable": self.parsed_ua.is_touch_capable
            }
        }
    
    def get_detailed_info(self) -> Dict[str, Any]:
        """获取详细信息"""
        basic_info = self.get_basic_info()
        
        # 添加额外信息
        detailed_info = {
            **basic_info,
            "raw_user_agent": self.user_agent_string,
            "is_email_client": self.parsed_ua.is_email_client,
            "device_type": self._get_device_type(),
            "platform_summary": self._get_platform_summary()
        }
        
        return detailed_info
    
    def _get_device_type(self) -> str:
        """获取设备类型摘要"""
        if self.parsed_ua.is_mobile:
            return "mobile"
        elif self.parsed_ua.is_tablet:
            return "tablet"
        elif self.parsed_ua.is_pc:
            return "desktop"
        else:
            return "other"
    
    def _get_platform_summary(self) -> str:
        """获取平台摘要"""
        device = self.parsed_ua.device
        os = self.parsed_ua.os
        
        if device.family != "Other":
            return f"{device.brand or device.family} {device.model or ''}".strip()
        else:
            return f"{os.family} {os.version_string or ''}".strip()


def get_user_agent_parser(request: Request) -> UserAgentParser:
    """获取User-Agent解析器依赖"""
    user_agent_string = request.headers.get("user-agent", "Unknown")
    return UserAgentParser(user_agent_string)


def get_user_agent_info(
    user_agent_parser: UserAgentParser = Depends(get_user_agent_parser)
) -> Dict[str, Any]:
    """获取User-Agent信息依赖"""
    return user_agent_parser.get_detailed_info()


def get_basic_user_agent_info(
    user_agent_parser: UserAgentParser = Depends(get_user_agent_parser)
) -> Dict[str, Any]:
    """获取基础User-Agent信息依赖"""
    return user_agent_parser.get_basic_info()
import time
from datetime import datetime
from uuid import uuid4
import json
import logging

from typing import Callable, Any, Coroutine
from fastapi.routing import APIRoute
from fastapi import Request, Response


logger = logging.getLogger("common")


SKIP_PATH_SET = {}

def skip_log_path(request_body) -> bool:
    request_body_str = str(request_body)
    for skip_path in SKIP_PATH_SET:
        if skip_path in request_body_str:
            return True
    return False

class CustomAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            # TODO: 添加trace_id
            # trace_id = request.headers.get("uber-trace-id", f"GTID:{uuid4().hex}")
            # request.state.trace_id = trace_id
            # GhLogging.bind(
            #     trace_id=trace_id,
            # )

            start = time.perf_counter()
            start_time = str(datetime.now())[:-3]
            try:
                response: Response = await original_route_handler(request)
            except Exception as e:
                # 计算耗时
                exception_duration = time.perf_counter() - start
                end_time = str(datetime.now())[:-3]
                # 获取request请求
                request_data = await self._custom_get_request_data(request)
                # 记录请求异常日志
                logger.error(
                    dict(
                        name="RecordRouteRequestException",
                        # request_headers=request.headers.items(),
                        # request_ip=request.client.host,
                        request_start_time=start_time,
                        request_end_time=end_time,
                        request_method=request.method,
                        request_path=str(request.url.path),
                        request_path_params=request.path_params,
                        request_query_params=dict(request.query_params),
                        request_body=request_data,
                        exception=str(e),
                        route_exception_duration=f"{exception_duration} s",
                    )
                )
                raise e
            else:
                # 计算耗时
                duration = time.perf_counter() - start
                end_time = str(datetime.now())[:-3]
                # 获取request请求
                request_data = await self._custom_get_request_data(request)
                # 获取response内容
                response_body = response.body.decode()
                # if response_body:
                #     response_data = json.loads(response_body)
                # else:
                #     response_data = None

                # 过滤部分返回值过大的请求日志打印
                # if skip_log_path(request_body=request_data):
                #     response_data = "skip response log"
                # 记录请求过程
                logger.info(
                    dict(
                        name="RecordRouteRequestAndResponse",
                        # request_headers=request.headers.items(),
                        # request_ip=request.client.host,
                        request_start_time=start_time,
                        request_end_time=end_time,
                        request_method=request.method,
                        request_path=str(request.url.path),
                        request_path_params=request.path_params,
                        request_query_params=dict(request.query_params),
                        request_body=request_data,
                        response=response_body,
                        route_duration=f"{duration} s",
                    )
                )
                return response
        return custom_route_handler

    async def _custom_get_request_data(self, request: Request):
        """
        获取request请求内容
        """
        if request._stream_consumed:
            info_list = [
                getattr(request, "_form", dict()),
                getattr(request, "_body", b'{}').decode()
            ]
            request_body = next((i for i in info_list if i))
        else:
            # 当post请求体为空或get请求时, request._stream_consumed为False
            request_body = ""
        
        if hasattr(request_body, "_dict"):
            request_data = getattr(request_body, "_dict", dict()) if request_body else dict()
        elif isinstance(request_body, str):
            request_data = json.loads(request_body) if request_body else dict()
        else:
            request_data = None
        return request_data

        # try:
        #     request_body = (await request.body()).decode()
        #     request_data = json.loads(request_body) if request_body else dict()
        # except RuntimeError:
        #     # 处理request form请求
        #     request_data = (await request.form())._dict
        # except Exception as e:
        #     request_data = {}
        #     logger.error("获取request body出现异常", path=str(request.url.path), exception=str(e))
        # return request_data

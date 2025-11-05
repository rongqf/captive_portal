import sys
import logging
import traceback  # 新增
logger = logging.getLogger("common")

def exception_hook(exctype, value, tb):
    logger.warning([exctype, value, tb])  # 打印异常
    logger.warning(traceback.format_exc())
    logger.exception([exctype, value, tb])

    sys.__excepthook__(exctype, value, tb)  # 调用原始异常方法

sys.excepthook = exception_hook
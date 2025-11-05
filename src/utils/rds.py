

import functools
from datetime import datetime, timezone
from redis import Redis
import redis_lock
from configs import settings
import logging
logger = logging.getLogger("common")


from utils import except_handle

redis = Redis.from_url('%s%s' % (settings.RDS_URI_OTC, settings.RDS_DB_OTC), 
                       decode_responses=True)

def set_reload_info(tag='all'):
    tm = datetime.now(tz=timezone.utc).isoformat()
    return redis.set('otcbook:reload_info:%s' % tag, tm)

def get_reload_info(tag='all'):
    tm = redis.get('otcbook:reload_info:%s' % tag)
    if tm:
        return datetime.fromisoformat(tm)
    else:
        return None
    

#只针对同步函数
def lock(key):
    def func_decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            #先检查funcs中的f是否满足，再调用func
            lock = redis_lock.Lock(redis, key)
            isok = False
            is_get_lock = False
            if lock.acquire(blocking=False):
                is_get_lock = True
                try:
                    res = func(*args, **kwargs)
                    isok = True
                except Exception as e:
                    logger.exception(e)
                    res = {
                        'ok': False,
                        'reason': {
                            'err': str(e),
                            'desc': str(e),
                        },
                    }
                lock.release()
            
            print(is_get_lock, isok, lock)
            if is_get_lock:
                return res
            else:
                return {
                    'ok': False,
                    'reason': {
                        'err': 'lock failed',
                        'desc': 'lock failed',
                    },
                }
        return wrapper
    return func_decorate



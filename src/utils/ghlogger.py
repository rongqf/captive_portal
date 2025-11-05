import logging
import pandas as pd

class GHLogger(logging.Logger):
    def info(self, msg, *args, **kwargs):
        argsnew = args
        if args:
            x = [a.to_dict() if isinstance(a, pd.DataFrame) else a for a in args]
            argsnew = tuple(x)
        if isinstance(msg, pd.DataFrame):
            msg = msg.to_dict('split')
        #logging.Logger.info(self, msg, *argsnew, stacklevel=2, **kwargs)
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, argsnew, **kwargs)

#logging.setLoggerClass(GHLogger)
logger = logging.getLogger('common')

def pd_to_dict(msg):
    if isinstance(msg, pd.DataFrame):
        return msg.to_dict('split')
    elif isinstance(msg, list):
        return [pd_to_dict(x) for x in msg]
    elif isinstance(msg, dict):
        return {k: pd_to_dict(v) for k, v in msg.items()}
    else:
        return msg

def pd_info(msg, *args, **kwargs):
    logger.info(pd_to_dict(msg), *args, stacklevel=2, **kwargs)
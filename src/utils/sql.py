from utils.common import engine
import pandas as pd
from datetime import date, datetime, timedelta, timezone

def sql_journal_can(ids):
    sql = '''update journal set is_valid = false where id in (%s) returning id'''
    sql = sql % ','.join([str(x) for x in ids])
    with engine.connect() as conn:
        res = conn.execute(sql)
        return [x for x in res]
    
#小于当前日期的最后一天的数据
def sql_get_pos_date_prv(the_date: date):
    sql = '''select * from positions where "date" = (select max("date") from positions WHERE "date" < '%s')'''
    sql = sql % the_date.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)

def sql_get_pos_max_date(the_date: date):
    sql = '''select max("date") as prvdate from positions WHERE "date" < '%s' '''
    sql = sql % the_date.strftime('%Y-%m-%d')
    df = pd.read_sql(sql, engine)
    if df.empty:
        return date(2020, 1, 1)
    else:
        return df.iloc[0]['prvdate']

def sql_get_pos_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from positions where '%s' <= "date" and "date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from positions where "date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)


def sql_get_client_pos_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from client_pos where '%s' <= "date" and "date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from client_pos where "date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)

def sql_get_pos_pl_max_date(the_date: date):
    sql = '''select max("date") as prvdate from position_pl WHERE "date" < '%s' '''
    sql = sql % the_date.strftime('%Y-%m-%d')
    df = pd.read_sql(sql, engine)
    if df.empty:
        return date(2020, 1, 1)
    else:
        return df.iloc[0]['prvdate']
    

def sql_get_pos_pl_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from position_pl where '%s' <= "date" and "date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from position_pl where "date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)

def sql_get_client_pos_max_date(the_date: date):
    sql = '''select max("date") as prvdate from client_pos WHERE "date" < '%s' '''
    sql = sql % the_date.strftime('%Y-%m-%d')
    df = pd.read_sql(sql, engine)
    if df.empty:
        return date(2020, 1, 1)
    else:
        return df.iloc[0]['prvdate']

def sql_get_client_margin_max_date(the_date: date):
    sql = '''select max("date") as prvdate from client_margin WHERE "date" < '%s' '''
    sql = sql % the_date.strftime('%Y-%m-%d')
    df = pd.read_sql(sql, engine)
    if df.empty:
        return date(2020, 1, 1)
    else:
        return df.iloc[0]['prvdate']
    
def sql_get_client_margin_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from client_margin where '%s' <= "date" and "date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from client_margin where "date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)

#获取
def sql_get_pos_date(the_date):
    sql = ''' select * from positions where "date" = '%s' '''
    sql = sql % the_date.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)




def sql_get_evt_summary_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from events_summary where '%s' <= "date" and "date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from events_summary where "date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)


def sql_get_evt_aqdq_max_date(the_date: date):
    sql = '''select max("sch_date") as prvdate from event_aq_dq WHERE "sch_date" < '%s' '''
    sql = sql % the_date.strftime('%Y-%m-%d')
    df = pd.read_sql(sql, engine)
    if df.empty:
        return date(2020, 1, 1)
    else:
        return df.iloc[0]['prvdate']
    

def sql_get_evt_aqdq_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from event_aq_dq where '%s' <= "sch_date" and "sch_date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from event_aq_dq where "sch_date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)


def sql_get_journal_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from journal where '%s' <= "date" and "date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from journal where "date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)


def sql_get_booking_input_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from booking_input where '%s' <= "trade_date" and "trade_date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from booking_input where "trade_date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)


def sql_get_risk_sub_group_max_date(the_date: date):
    sql = '''select max("date") as date from risk_sub_group WHERE "date" < '%s' '''
    sql = sql % the_date.strftime('%Y-%m-%d')
    df = pd.read_sql(sql, engine)
    if df.empty:
        return None
    else:
        return df.iloc[0]['date']
    
    
def sql_get_risk_sub_group_range(d1: date, d2: date):
    if d1 != d2:
        sql = '''select * from risk_sub_group where '%s' <= "date" and "date" <= '%s' '''
        sql = sql % (d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    else:
        sql = ''' select * from risk_sub_group where "date" = '%s' '''
        sql = sql % d1.strftime('%Y-%m-%d')
    return pd.read_sql(sql, engine)

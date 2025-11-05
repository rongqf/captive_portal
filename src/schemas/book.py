from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class SettleTradeInput(BaseModel):
    input_date: str
    nums: list
    dates: list


class CancelTradeInput(BaseModel):
    nums: list
    dates: list


class RateItem(BaseModel):
    inst_code: str
    valuation_date: date
    value: str

class StocksItem(RateItem):
    open: str
    high: str
    low: str
    pre_eod_price: str
    volume: str

class FXItem(RateItem):
    bid: Optional[str]
    ask: Optional[str]

class DoValueInput(RateItem):...


class UpdatePriceInput(BaseModel):
    value_date: Optional[date]
    rate: Optional[List[RateItem]]
    fx: Optional[List[FXItem]]
    stocks: Optional[List[StocksItem]]
    aqdq: Optional[List[DoValueInput]]


class UpdatePriceNewItem(BaseModel):
    inst_code: str
    ticker: str
    date: date
    bid: float
    ask: float
    open: float
    high: float
    low: float
    value: float
    volume: float
    
class UpdatePriceInputNew(BaseModel):
    update_vdate: date
    items: List[UpdatePriceNewItem]



class BookItem(BaseModel):
    booking_number : Optional[str]
    to_book : Optional[str]
    type : Optional[str]
    order_group : Optional[str]
    party_1 : Optional[str]
    party_2 : Optional[str]
    settlement_counterparty : Optional[str]
    product_1 : Optional[str]
    product_2 : Optional[str]
    related_prod : Optional[str]
    direction_1 : Optional[str]
    quantity_1 : Optional[float]
    quantity_2 : Optional[float]
    price : Optional[float]
    currency : Optional[str]
    
    net_price_strike: Optional[float]
    maturity: Optional[str]
    trs_fund_ccy: Optional[str]
    
    trade_date : Optional[date]
    settlement_date : Optional[date]
    remark : Optional[str]
    settled_cash : Optional[float]
    pending_cash : Optional[float]
    ir_rate : Optional[float]
    bench_mark : Optional[str]
    bm_rate : Optional[float]
    bid_rate : Optional[float]
    ask_rate : Optional[float]
    neg_allow : Optional[bool]
    uuid : Optional[str]

class BookInput(BaseModel):
    books: List[BookItem]


class Inst_Cash(BaseModel):
    inst_code: str
    name: Optional[str]
    currency: Optional[str]

class Inst_FX(BaseModel):
    inst_code: str
    bbg_ticker: Optional[str]
    foreign: Optional[str]
    base: Optional[str]
    reverse: Optional[str]

class Inst_Rate(BaseModel):
    inst_code: str
    bbg_ticker: Optional[str]
    currency: Optional[str]
    name: Optional[str]
    series: Optional[str]

class Inst_Stock(BaseModel):
    inst_code: str
    valid_from: date
    valid_to: Optional[date]
    bbg_ticker: Optional[str]
    name: Optional[str]
    exchange: Optional[str]
    currency: Optional[str]
    dvd_PayPct: Optional[str]
    yahoo_ticker: Optional[str]
    

class Inst_Lists(BaseModel):
    inst_cash: Optional[List[Inst_Cash]]
    inst_fx: Optional[List[Inst_FX]]
    inst_rates: Optional[List[Inst_Rate]]
    inst_stocks: Optional[List[Inst_Stock]]


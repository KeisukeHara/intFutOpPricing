from fastapi import FastAPI
from typing import Optional,List
from pydantic import BaseModel
import QuantLib as ql
import pricing_logic as pl

class IntFutOpTrade(BaseModel):
    trade_id:str
    ccy:str
    strike:float
    expiration_date:str
    call_put:str
    buy_sell:str
    amount:float



class MarketInputData(BaseModel):
    evaluation_date:str
    spot_date:str
    interest_rate:float
    volatility:float
    underlying_price:float

class CalcPvRequest(BaseModel):
    trade_data:IntFutOpTrade
    market_data:MarketInputData

class CalcPvResponse(BaseModel):
    trade_id:str
    premium:float
    pv: float



app = FastAPI()

@app.get("/")
async def top():
    return {  "trade_data": {
    "trade_id": "string",
    "ccy": "string",
    "strike": 100,
    "expiration_date": "20230914",
    "call_put": "C",
    "buy_sell": "string",
    "amount": 0
  },
  "market_data": {
    "evaluation_date": "20230712",
    "spot_date": "20230714",
    "interest_rate": 0.01,
    "volatility": 0.2,
    "underlying_price": 105.0
  }}
#    return {"message": "calc pv of interest future option trade."}


@app.post("/calc/calc_pv/")
async def calc_pv(req: CalcPvRequest) -> CalcPvResponse:
    #取引データとマーケットデータの設定
    evaluation_date = pl.convert_date_string(req.market_data.evaluation_date)  # 評価日
    spot_date = pl.convert_date_string(req.market_data.spot_date)  # 金利カーブの基準日
    strike_price = req.trade_data.strike  # ストライク価格
    expiration_date = pl.convert_date_string(req.trade_data.expiration_date)  # オプションの満期日

    if req.trade_data.call_put == "C":
        option_type = ql.Option.Call
    else:
        option_type = ql.Option.Put  # オプションのタイプ (Call or Put)

    interest_rate = req.market_data.interest_rate  # 金利
    volatility = req.market_data.volatility  # ボラティリティ
    underlying_price = req.market_data.underlying_price  # 基礎資産の価格

    trade_data = pl.TradeData(strike_price, expiration_date, option_type)
    market_data = pl.MarketData(evaluation_date, spot_date, interest_rate, volatility, underlying_price)

    #計算実行
    premium = pl.calculate_option_price(trade_data, market_data)
    pv = premium / 100 / 4 * req.trade_data.amount
    if req.trade_data.buy_sell == "S":
        premium *= -1

    result = CalcPvResponse(trade_id=req.trade_data.trade_id, premium=premium, pv=pv)

    return result

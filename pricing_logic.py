import QuantLib as ql

class TradeData:
    def __init__(self, strike_price, expiration_date, option_type):
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.option_type = option_type

class MarketData:
    def __init__(self, evaluation_date, spot_date, interest_rate, volatility, underlying_price):
        self.evaluation_date = evaluation_date
        self.spot_date = spot_date
        self.interest_rate = interest_rate
        self.volatility = volatility
        self.underlying_price = underlying_price

def calculate_option_price(trade_data, market_data):
    # 日付設定
    ql.Settings.instance().evaluationDate = market_data.evaluation_date

    # 金利カーブ設定
    curve = ql.FlatForward(market_data.spot_date, market_data.interest_rate, ql.Actual360())
    discount_curve = ql.YieldTermStructureHandle(curve)

    # ボラティリティカーブ設定
    volatility_curve = ql.BlackConstantVol(market_data.spot_date, ql.NullCalendar(), market_data.volatility, ql.Actual360())
    volatility_curve_handle = ql.BlackVolTermStructureHandle(volatility_curve)

    # オプションの作成
    option = ql.EuropeanOption(ql.PlainVanillaPayoff(trade_data.option_type, trade_data.strike_price), ql.EuropeanExercise(trade_data.expiration_date))

    # 基礎資産の設定
    underlying_price = market_data.underlying_price
    option.setPricingEngine(ql.AnalyticEuropeanEngine(ql.BlackScholesProcess(ql.QuoteHandle(ql.SimpleQuote(underlying_price)), discount_curve, volatility_curve_handle)))

    # オプションの価格計算
    option_price = option.NPV()
    return option_price


def convert_date_string(date_string):
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return ql.Date(day, month, year)
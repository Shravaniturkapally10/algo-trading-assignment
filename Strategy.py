import backtrader as bt
import yfinance as yf


# Stock settings
SYMBOL = "AAPL"
START = "2019-01-01"
END = "2025-01-01"

STARTING_CASH = 100000


class SMARSI_Strategy(bt.Strategy):

    params = (
        ("fast_ma", 20),
        ("slow_ma", 50),
        ("rsi_period", 14),
        ("rsi_buy", 55),
        ("stop_loss", 0.05),
        ("take_profit", 0.10),
    )

    def __init__(self):

        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.fast_ma
        )

        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.slow_ma
        )

        self.rsi = bt.indicators.RSI(
            self.data.close,
            period=self.params.rsi_period
        )

        self.crossover = bt.indicators.CrossOver(
            self.fast_ma,
            self.slow_ma
        )

        self.buy_price = 0

    def next(self):

        if not self.position:

            if self.crossover[0] > 0 and self.rsi[0] > self.params.rsi_buy:

                self.buy()

                self.buy_price = self.data.close[0]

                print(f"BUY at {self.buy_price}")

        else:

            current_price = self.data.close[0]

            if current_price <= self.buy_price * (
                1 - self.params.stop_loss
            ):

                self.close()

                print(f"STOP LOSS SELL at {current_price}")

            elif current_price >= self.buy_price * (
                1 + self.params.take_profit
            ):

                self.close()

                print(f"TAKE PROFIT SELL at {current_price}")

            elif self.crossover[0] < 0:

                self.close()

                print(f"CROSSOVER SELL at {current_price}")


def run_backtest():


    cerebro = bt.Cerebro()

    cerebro.addstrategy(SMARSI_Strategy)

    # Download stock data
    data = yf.download(
        SYMBOL,
        start=START,
        end=END,
        auto_adjust=False
    )

    # Flatten multi-index columns
    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    # Convert all column names to lowercase
    data.columns = [str(col).lower() for col in data.columns]

    print(data.columns)


    datafeed = bt.feeds.PandasData(
        dataname=data,
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )

    cerebro.adddata(datafeed)
    cerebro.broker.setcash(STARTING_CASH)
    print("Starting Portfolio Value: {cerebro.broker.getvalue()")
    cerebro.run()
    print("Final Portfolio Value: {cerebro.broker.getvalue()")
    cerebro.plot()

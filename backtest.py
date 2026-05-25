import backtrader as bt
import yfinance as yf

# Import Strategy Class
from Strategy import SMARSI_Strategy


# Stock Details
SYMBOL = "AAPL"
START = "2019-01-01"
END = "2025-01-01"

# Starting Capital
STARTING_CASH = 100000


def run_backtest():

    # Create Cerebro Engine
    cerebro = bt.Cerebro()

    # Download Historical Data
    data = yf.download(
        SYMBOL,
        start=START,
        end=END,
        auto_adjust=False
    )

    # Fix Multi-Index Columns
    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    # Convert Column Names to Lowercase
    data.columns = [
        str(col).lower()
        for col in data.columns
    ]

    print(data.columns)

    # Convert Pandas Data to Backtrader Feed
    data_feed = bt.feeds.PandasData(
        dataname=data,
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )

    # Add Data Feed
    cerebro.adddata(data_feed)

    # Add Strategy
    cerebro.addstrategy(SMARSI_Strategy)

    # Set Initial Cash
    cerebro.broker.setcash(
        STARTING_CASH
    )

    # Set Broker Commission
    cerebro.broker.setcommission(
        commission=0.001
    )

    # Add Drawdown Analyzer
    cerebro.addanalyzer(
        bt.analyzers.DrawDown,
        _name="drawdown"
    )

    print(
        f"Starting Portfolio Value: "
        f"{cerebro.broker.getvalue():.2f}"
    )

    # Run Backtest
    results = cerebro.run()

    # Get Strategy Instance
    strategy = results[0]

    # Final Portfolio Value
    final_value = cerebro.broker.getvalue()

    # Calculate Total Return
    total_return = (
        (final_value - STARTING_CASH)
        / STARTING_CASH
    ) * 100

    # Maximum Drawdown
    max_drawdown = strategy.analyzers.drawdown.get_analysis()[
        "max"
    ]["drawdown"]

    print(
        f"Final Portfolio Value: "
        f"{final_value:.2f}"
    )

    print(
        f"Total Return: "
        f"{total_return:.2f}%"
    )

    print(
        f"Maximum Drawdown: "
        f"{max_drawdown:.2f}%"
    )

    # Plot Graph
    cerebro.plot()


# Main Function
if __name__ == "__main__":
    run_backtest()
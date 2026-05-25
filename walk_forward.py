import numpy as np
import yfinance as yf
import backtrader as bt

# Import Strategy Class
from Strategy import SMARSI_Strategy


# Stock Symbol
SYMBOL = "AAPL"

# Starting Cash
STARTING_CASH = 100000


def prepare_data(data):

    # Fix Multi-Index Columns
    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    # Convert Columns to Lowercase
    data.columns = [
        str(col).lower()
        for col in data.columns
    ]

    return data


def run_segment(
    train_start,
    train_end,
    test_start,
    test_end
):

    # Download Training Data
    train_data = yf.download(
        SYMBOL,
        start=train_start,
        end=train_end,
        auto_adjust=False
    )

    train_data = prepare_data(
        train_data
    )

    # Download Testing Data
    test_data = yf.download(
        SYMBOL,
        start=test_start,
        end=test_end,
        auto_adjust=False
    )

    test_data = prepare_data(
        test_data
    )

    best_return = -999
    best_params = None

    # Parameter Optimization
    for fast in [10, 20, 30]:

        for slow in [50, 100]:

            cerebro = bt.Cerebro()

            feed = bt.feeds.PandasData(
                dataname=train_data,
                open='open',
                high='high',
                low='low',
                close='close',
                volume='volume',
                openinterest=-1
            )

            cerebro.adddata(feed)

            cerebro.addstrategy(
                SMARSI_Strategy,
                fast_ma=fast,
                slow_ma=slow
            )

            cerebro.broker.setcash(
                STARTING_CASH
            )

            cerebro.run()

            final_value = (
                cerebro.broker.getvalue()
            )

            total_return = (
                (final_value - STARTING_CASH)
                / STARTING_CASH
            ) * 100

            # Find Best Parameters
            if total_return > best_return:

                best_return = total_return

                best_params = (
                    fast,
                    slow
                )

    # Out-of-Sample Testing
    cerebro = bt.Cerebro()

    feed = bt.feeds.PandasData(
        dataname=test_data,
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )

    cerebro.adddata(feed)

    cerebro.addstrategy(
        SMARSI_Strategy,
        fast_ma=best_params[0],
        slow_ma=best_params[1]
    )

    cerebro.broker.setcash(
        STARTING_CASH
    )

    cerebro.run()

    final_value = (
        cerebro.broker.getvalue()
    )

    out_sample_return = (
        (final_value - STARTING_CASH)
        / STARTING_CASH
    ) * 100

    # Walk Forward Efficiency
    efficiency = (
        out_sample_return / best_return
    ) * 100 if best_return != 0 else 0

    return {
        "best_in_sample_return":
            best_return,

        "out_sample_return":
            out_sample_return,

        "efficiency":
            efficiency,

        "best_parameters":
            best_params
    }


if __name__ == "__main__":

    windows = [

        (
            "2019-01-01",
            "2021-01-01",
            "2021-01-01",
            "2021-07-01"
        ),

        (
            "2020-01-01",
            "2022-01-01",
            "2022-01-01",
            "2022-07-01"
        ),

        (
            "2021-01-01",
            "2023-01-01",
            "2023-01-01",
            "2023-07-01"
        )
    ]

    efficiencies = []

    for window in windows:

        result = run_segment(
            *window
        )

        efficiencies.append(
            result["efficiency"]
        )

        print("\n======================")
        print(
            f"Best Parameters: "
            f"{result['best_parameters']}"
        )

        print(
            f"In-Sample Return: "
            f"{result['best_in_sample_return']:.2f}%"
        )

        print(
            f"Out-of-Sample Return: "
            f"{result['out_sample_return']:.2f}%"
        )

        print(
            f"Efficiency: "
            f"{result['efficiency']:.2f}%"
        )

    average_efficiency = np.mean(
        efficiencies
    )

    print("\n======================")

    print(
        f"Average Walk Forward "
        f"Efficiency: "
        f"{average_efficiency:.2f}%"
    )
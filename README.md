<<<<<<< HEAD
# Algorithmic Trading Strategy Assignment

## Project Overview

This project implements an algorithmic trading strategy using Python and the Backtrader framework.

The strategy uses:

- Simple Moving Average (SMA) Crossover
- Relative Strength Index (RSI)
- Stop Loss
- Take Profit

The project also includes:

- Backtesting
- Walk-Forward Analysis
- Robustness Score Calculation

---

# Technologies Used

- Python
- Backtrader
- yFinance
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

---

# Project Structure

algo-trading-assignment/

├── strategy.py  
├── backtest.py  
├── walk_forward.py  
├── robustness.py  
├── requirements.txt  
└── README.md  

---

# Strategy Explanation

## Buy Conditions

The strategy enters a BUY trade when:

1. Fast SMA crosses above Slow SMA
2. RSI is greater than 55

---

## Sell Conditions

The strategy exits a trade when:

1. Fast SMA crosses below Slow SMA
2. Stop-loss is triggered
3. Take-profit target is reached

---

# Installation

Install all required libraries using:

```bash id="v10mxv"
pip install -r requirements.txt
=======
# algo-trading-assignment
Algorithmic Trading Strategy Project
>>>>>>> 9d544de3f3671d09d39dcc07f913ef693aecb497

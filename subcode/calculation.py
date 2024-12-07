# ---------------------------------------------------------
# RSI Backtesting Tool - Calculation Functions
#
# Language:         Python
#
# Project Members:  Arthur, Samuel, Leo
#
# Final Review:     December 8, 2024
#
# Description:      This script provides essential functions for performing
#                   calculations and simulations in the RSI Backtesting Tool.
#                   It includes fetching historical stock data, calculating RSI,
#                   generating trading signals, backtesting a trading strategy, 
#                   and calculating performance metrics.
#
# Assistance:       The structure, code design, and modularization of this project were 
#                   influenced by multiple resources, including ChatGPT, an AI language 
#                   model developed by OpenAI. Additional guidance and references were 
#                   drawn from YouTube tutorials, Stack Overflow discussions, and other 
#                   publicly available educational materials during the development process.
# ---------------------------------------------------------

import yfinance as yf   # Import yfinance for fetching historical stock data.
import pandas as pd     # Import pandas for data manipulation and analysis.
import numpy as np      # Import numpy for numerical operations.

# ------------------ Fetch Historical Data ------------------
# Fetches daily historical price data for a given stock ticker using yfinance.
def get_historical_data(ticker, start_date, end_date):
    """
    Fetches historical price data for a given ticker between specified start and end dates.
    Cleans the data by removing NaN values and flattening multi-index columns if present.
    """
    data = yf.download(tickers=ticker, start=start_date, end=end_date, interval='1d', progress=False)   # Download data for the given ticker and date range.
    data.dropna(inplace=True)                                                                           # Remove rows with missing data.
    if isinstance(data.columns, pd.MultiIndex):                                                         # Check if the columns are multi-indexed.
        data.columns = data.columns.get_level_values(0)                                                 # Flatten the multi-indexed columns.
    return data                                                                                         # Return the cleaned data.

# ------------------ Calculate RSI ------------------
# Function that calculates the Relative Strength Index (RSI) over a specified period.

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()                                    # Calculate the daily change in closing price.
    gain = (delta.where(delta > 0, 0)).fillna(0)                    # Keep positive changes (gains) and set others to 0.
    loss = (-delta.where(delta < 0, 0)).fillna(0)                   # Keep negative changes (losses) as positive values.
    avg_gain = gain.rolling(window=period, min_periods=1).mean()    # Calculate the rolling average gain over the specified period.
    avg_loss = loss.rolling(window=period, min_periods=1).mean()    # Calculate the rolling average loss over the specified period.
    rs = avg_gain / avg_loss                                        # Calculate the relative strength (RS) as the ratio of average gain to average loss.
    data['RSI'] = 100 - (100 / (1 + rs))                            # Convert RS to RSI using the RSI formula.
    data['RSI'] = data['RSI'].fillna(50)                            # Set RSI to a neutral value (50) for initial periods with insufficient data.
    return data                                                     # Return the data with the RSI column added.

# ------------------ Generate Trading Signals ------------------
# Function that generates buy/sell trading signals based on RSI thresholds.

def generate_signals(data, rsi_overbought, rsi_oversold):
    data['Signal'] = 0                                                                          # Initialize a new column for trading signals with default value 0 (hold).
    buy_signals = (data['RSI'] > rsi_oversold) & (data['RSI'].shift(1) <= rsi_oversold)         # Identify buy signals when RSI crosses above the oversold level.
    data.loc[buy_signals, 'Signal'] = 1                                                         # Assign a buy signal (1) to rows where the condition is met.
    sell_signals = (data['RSI'] < rsi_overbought) & (data['RSI'].shift(1) >= rsi_overbought)    # Identify sell signals when RSI crosses below the overbought level.
    data.loc[sell_signals, 'Signal'] = -1                                                       # Assign a sell signal (-1) to rows where the condition is met.
    return data                                                                                 # Return the data with the Signal column added.

# ------------------ Backtest Strategy ------------------
# Function that simulates the trading strategy using the generated signals and calculates portfolio performance. 
    # Backtests a trading strategy using generated buy/sell signals, starting capital, and trade fees.
    # Simulates trades and calculates portfolio value, fees paid, and strategy returns over time.

def backtest_strategy(data, initial_capital, fee_percentage):

    data = data.copy()                                      # Create a copy of the data to avoid modifying the original.
    cash = initial_capital                                  # Initialize cash with the starting capital.
    holdings = 0                                            # Track the number of shares held.
    total_fees = 0                                          # Track the total fees paid during the backtest.
    portfolio_values = []                                   # List to store daily portfolio values.
    positions = []                                          # List to track position status (1 for holding, 0 for no position).
    trades = []                                             # List to track trades executed (1 for buy, -1 for sell, 0 for hold).
    daily_returns = []                                      # List to store daily returns.
    prev_portfolio_value = initial_capital                  # Store the previous day's portfolio value for return calculation.

    for i in range(len(data)):                                  # Iterate through each row of the data (daily data points).
        price = data['Close'].iloc[i]                           # Get the closing price for the current day.
        signal = data['Signal'].iloc[i]                         # Get the trading signal for the current day.
        trade = 0                                               # Initialize trade as 0 (no trade).

        if signal == 1 and holdings == 0:                           # Execute a buy trade if the signal is 1 and no holdings exist.
            shares = int(cash // price)                             # Calculate the number of shares that can be purchased.
            if shares > 0:                                          # Ensure that at least one share can be purchased.
                fee = shares * price * fee_percentage               # Calculate the trade fee.
                cash -= shares * price + fee                        # Deduct the cost of shares and fee from cash.
                holdings += shares                                  # Update holdings with the number of shares purchased.
                total_fees += fee                                   # Add the fee to the total fees paid.
                positions.append(1)                                 # Update position status to 1 (holding shares).
                trade = 1                                           # Record the trade as a buy.

        elif signal == -1 and holdings > 0:                         # Execute a sell trade if the signal is -1 and holdings exist.
            fee = holdings * price * fee_percentage                 # Calculate the trade fee for selling.
            cash += holdings * price - fee                          # Add the proceeds from selling shares (minus fee) to cash.
            holdings = 0                                            # Reset holdings to 0 after selling all shares.
            total_fees += fee                                       # Add the fee to the total fees paid.
            positions.append(0)                                     # Update position status to 0 (no holdings).
            trade = -1                                              # Record the trade as a sell.

        else:                                                       # If no trade occurs, maintain the current position.
            positions.append(positions[-1] if positions else 0)     # Keep the last position status.

        portfolio_value = cash + holdings * price   # Calculate the total portfolio value (cash + value of holdings).
        portfolio_values.append(portfolio_value)    # Append the portfolio value to the list.
        trades.append(trade)                        # Append the trade status to the trades list.

        daily_return = (portfolio_value - prev_portfolio_value) / prev_portfolio_value if prev_portfolio_value != 0 else 0  # Calculate the daily return as the change in portfolio value compared to the previous day.
        daily_returns.append(daily_return)                                                                                  # Append the daily return to the list.
        prev_portfolio_value = portfolio_value                                                                              # Update the previous day's portfolio value.

    # Add results to the data for further analysis.
    data['Portfolio Value'] = portfolio_values          # Add the daily portfolio values to the data.
    data['Total Fees'] = total_fees                     # Add the total fees paid to the data.
    data['Positions'] = positions                       # Add the position statuses to the data.
    data['Trades'] = trades                             # Add the trades executed to the data.
    data['Strategy Daily Return'] = daily_returns       # Add the daily returns to the data.
    return data                                         # Return the data with the added backtesting results.

# ------------------ Calculate Performance Metrics ------------------
# Function that computes various performance metrics for the strategy and Buy-and-Hold. 
    # Calculates key performance metrics for the trading strategy and Buy-and-Hold approach.
    # Metrics include portfolio value, returns, drawdowns, volatility, and Sharpe ratio.

def calculate_performance_metrics(data, initial_capital):

    data = data.copy()  # Create a copy of the data to avoid modifying the original.

    # Calculate total return for the strategy
    total_return = (data['Portfolio Value'].iloc[-1] / initial_capital) - 1     # Final portfolio value divided by initial capital minus 1.

    # Calculate drawdowns for the strategy
    cumulative_max = data['Portfolio Value'].expanding(min_periods=1).max()     # Track the highest portfolio value seen up to each day.
    drawdown = (data['Portfolio Value'] - cumulative_max) / cumulative_max      # Calculate drawdown as the percentage drop from the cumulative max.
    max_drawdown = drawdown.min()                                               # Get the maximum drawdown (largest drop from the peak).

    # Retrieve total fees paid and final portfolio value
    total_fees = data['Total Fees'].iloc[-1]                                    # Get the total fees paid during the backtest.
    final_portfolio_value = data['Portfolio Value'].iloc[-1]                    # Get the final portfolio value after the last trading day.

    # Calculate strategy volatility and Sharpe Ratio
    strategy_daily_returns = data['Strategy Daily Return']                      # Extract daily returns for the strategy.
    strategy_volatility = strategy_daily_returns.std() * np.sqrt(252)           # Annualize volatility based on daily returns.
    risk_free_rate = 0.01                                                       # Set the assumed annual risk-free rate (e.g., 1%).
    strategy_sharpe_ratio = (strategy_daily_returns.mean() * 252 - risk_free_rate) / strategy_volatility if strategy_volatility != 0 else 0  # Calculate Sharpe Ratio.

    # Count the total number of trades executed
    num_trades = data['Trades'].abs().sum()  # Count buy (1) and sell (-1) trades as positive values.

    # ------------------ Buy-and-Hold Metrics ------------------
    # These metrics evaluate a simple buy-and-hold strategy for comparison with the RSI strategy.

    data['Buy and Hold Position'] = 1                                                                   # Assume always holding the stock throughout the period.
    data['Buy and Hold Portfolio Value'] = initial_capital * (data['Close'] / data['Close'].iloc[0])    # Scale portfolio value with stock price relative to the first day.

    # Calculate total return for buy-and-hold
    bh_total_return = (data['Buy and Hold Portfolio Value'].iloc[-1] / initial_capital) - 1             # Final value divided by initial capital minus 1.

    # Calculate drawdowns for buy-and-hold
    bh_cumulative_max = data['Buy and Hold Portfolio Value'].expanding(min_periods=1).max()             # Track the highest value up to each day.
    bh_drawdown = (data['Buy and Hold Portfolio Value'] - bh_cumulative_max) / bh_cumulative_max        # Calculate drawdown as a percentage drop from the cumulative max.
    bh_max_drawdown = bh_drawdown.min()                                                                 # Get the maximum drawdown.

    # Calculate daily returns, volatility, and Sharpe Ratio for buy-and-hold
    data['Buy and Hold Daily Return'] = data['Close'].pct_change().fillna(0)                            # Calculate daily returns for buy-and-hold.
    bh_volatility = data['Buy and Hold Daily Return'].std() * np.sqrt(252)                              # Annualize volatility for buy-and-hold daily returns.
    bh_sharpe_ratio = (data['Buy and Hold Daily Return'].mean() * 252 - risk_free_rate) / bh_volatility if bh_volatility != 0 else 0  # Calculate Sharpe Ratio.

    # Retrieve final portfolio value for buy-and-hold
    bh_final_portfolio_value = data['Buy and Hold Portfolio Value'].iloc[-1]                            # Get the final portfolio value.

    # ------------------ Prepare Metrics Dictionary ------------------
    # Create a dictionary to store all performance metrics for both strategies.
    metrics = {
        'portfolio_value': f"${final_portfolio_value:,.2f}",            # Final portfolio value for the RSI strategy.
        'total_return': f"{total_return:.2%}",                          # Total return percentage for the RSI strategy.
        'max_drawdown': f"{max_drawdown:.2%}",                          # Maximum drawdown percentage for the RSI strategy.
        'volatility': f"{strategy_volatility:.2%}",                     # Annualized volatility for the RSI strategy.
        'sharpe_ratio': f"{strategy_sharpe_ratio:.2f}",                 # Sharpe Ratio for the RSI strategy.
        'fees_paid': f"${total_fees:,.2f}",                             # Total fees paid during the RSI strategy.
        'number_of_trades': int(num_trades),                            # Total number of trades executed in the RSI strategy.
        'bh_portfolio_value': f"${bh_final_portfolio_value:,.2f}",      # Final portfolio value for buy-and-hold.
        'bh_total_return': f"{bh_total_return:.2%}",                    # Total return percentage for buy-and-hold.
        'bh_max_drawdown': f"{bh_max_drawdown:.2%}",                    # Maximum drawdown percentage for buy-and-hold.
        'bh_volatility': f"{bh_volatility:.2%}",                        # Annualized volatility for buy-and-hold.
        'bh_sharpe_ratio': f"{bh_sharpe_ratio:.2f}",                    # Sharpe Ratio for buy-and-hold.
        'bh_number_of_trades': "N/A",                                   # Number of trades is not applicable for buy-and-hold.
        'bh_fees_paid': "N/A",                                          # Fees are not applicable for buy-and-hold.
    }

    return data, metrics                                                # Return the data with added metrics and the dictionary of performance metrics.

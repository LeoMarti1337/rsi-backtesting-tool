# RSI Backtesting Tool

## Project Information

**Assignment:** Coding Group Project

**Group ID:** 3360

**Creators:** Arthur, Samuel, Leo  

## Project Description
**RSI Backtesting Tool** is a Python application that enables traders to evaluate RSI (Relative Strength Index) trading strategies using historical stock data. It provides a user-friendly GUI to configure strategy parameters, execute backtests, and visualize performance metrics compared to buy-and-hold strategies.

#### How does the program calculate the returns of a strategy?

1. Retrieve Historical Market Data
2. Calculate RSI (Relative Strength Index) 
3. Generate Trading Signals  
4. Backtest and Visualize Strategy Outcomes
5. Summarize Performance Metrics



## Example Backtest of a Strategy
Below is an excerpt from the Interface showing the backtest of the RSI-Strategy with given set of parameters.

![image](https://github.com/user-attachments/assets/9d384534-ff61-485d-9198-4a999ea7067e)<br>

While the strategy achieved higher historical returns than a buy-and-hold approach for JPMorgan, it underperformed compared to buy-and-hold for all other companies in the list. However, it is noteworthy that volatility decreased and the sharpe ratio increased in nearly all company backtests, resulting in a more stable portfolio over time. Additionally, maximum drawdowns were significantly lower in most backtests.

## Directory Structure
```
.
├─ main.py
├─ README.md
├─ requirements.txt
└─ subcode
   ├─ app.py
   ├─ calculation.py
   └─ configuration.py
```

- **main.py**: The entry point of the application that initializes and runs the backtesting GUI.
- **subcode/**: A directory containing all the supporting modules for calculations, configuration, and the GUI.
  - **app.py**: Defines the `BacktestApp` GUI class, manages user input, and displays results.
  - **calculation.py**: Handles data retrieval, RSI calculation, signal generation, strategy backtesting, and performance metric calculations.
  - **configuration.py**: Provides configurations such as company listings and default start/end dates for data retrieval.

## Installation & Requirements
**Requirements:**
- Python 3.8+
- Packages listed in `requirements.txt`

**Installation Steps:**
1. Clone the repository:
   ```bash
   git clone https://github.com/LeoMarti1337/rsi-backtesting-tool
   cd rsi-backtesting-tool
   ```
   *(If a you have problems with git, download the contents manually and open cmd in the correct repository.)*

2. Install required packages (if needed):
   ```bash
   pip install -r requirements.txt
   ```
   *(If that fails, install needed libraries like `yfinance`, `pandas`, `numpy`, `matplotlib` manually.)*

## Usage Instructions
1. Run the main application:
   ```bash
   python main.py #for Windows
   ```
   ```bash
   python3 main.py #for Mac
   ```
1. The RSI Backtesting Tool’s GUI will appear.  
2. Choose a company from the dropdown, set initial capital, fee percentage, and RSI thresholds.
3. Click on **"Run Backtest"** to generate the analysis and view the performance metrics and charts.

## Configuration Details
- The `subcode/configuration.py` file defines:
  - **COMPANIES**: A dictionary of company names and their corresponding ticker symbols. You can add or remove entries as needed.
  - **START_DATE** and **END_DATE**: Default date range for historical data retrieval.

Adjust these settings to analyze different companies or time periods.


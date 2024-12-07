# RSI Backtesting Tool

## Project Information
-**Assignment:** Coding Group Project
-**Group ID:** 3360
-**Creators:** Arthur, Samuel, Leo  

## Program Summary
**RSI Backtesting Tool** is a Python application that enables traders to evaluate RSI (Relative Strength Index) trading strategies using historical stock data. It provides a user-friendly GUI to configure strategy parameters, execute backtests, and visualize performance metrics compared to buy-and-hold strategies.

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
- Packages listed in `calculation.py` imports (e.g., `yfinance`, `pandas`, `numpy`, `matplotlib`, `tkinter` (included with standard Python), `ttk`).

**Installation Steps:**
1. Clone the repository:
   ```bash
   git clone [your_repository_url_here]
   cd [your_repository_directory]
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install required packages (if needed):
   ```bash
   pip install -r requirements.txt
   ```
   *(If a `requirements.txt` file is not provided, install needed libraries like `yfinance`, `pandas`, `numpy`, `matplotlib` manually.)*

## Usage Instructions
1. Run the main application:
   ```bash
   python main.py
   ```
2. The RSI Backtesting Tool’s GUI will appear.  
3. Choose a company from the dropdown, set initial capital, fee percentage, and RSI thresholds.
4. Click on **"Run Backtest"** to generate the analysis and view the performance metrics and charts.

## Configuration Details
- The `subcode/configuration.py` file defines:
  - **COMPANIES**: A dictionary of company names and their corresponding ticker symbols. You can add or remove entries as needed.
  - **START_DATE** and **END_DATE**: Default date range for historical data retrieval.

Adjust these settings to analyze different companies or time periods.

## Example (Screenshot/Code Snippet)
Below is an excerpt from `app.py` showing the initial default parameters for the RSI strategy:

```python
self.company_var.set('JPMorgan Chase & Co. (JPM)')
self.capital_entry.insert(0, "10000")       # Starting capital: $10,000
self.fee_entry.insert(0, "0.1")             # Fee per Trade: 0.1%
self.overbought_entry.insert(0, "70")       # RSI Overbought Level: 70
self.oversold_entry.insert(0, "30")         # RSI Oversold Level: 30
```
```

# ---------------------------------------------------------
# RSI Backtesting Tool - Configuration File
#
# Language:         Python
#
# Project Members:  Arthur, Samuel, Leo
#
# Final Review:     December 8, 2024
#
# Description:      This configuration file allows customization of key parameters 
#                   for the RSI Backtesting Tool. Users can modify the list of 
#                   companies to analyze and set the default start and end dates 
#                   for historical data retrieval.
#
# Assistance:       The structure, code design, and modularization of this project were 
#                   influenced by multiple resources, including ChatGPT, an AI language 
#                   model developed by OpenAI. Additional guidance and references were 
#                   drawn from YouTube tutorials, Stack Overflow discussions, and other 
#                   publicly available educational materials during the development process.
# ---------------------------------------------------------

# ------------------ Companies Configuration ------------------
# This dictionary contains the names of popular companies and their respective stock tickers.
# Users can add or remove entries to customize the list of companies available for analysis.

COMPANIES = {
    'Apple Inc. (AAPL)': 'AAPL',                # Apple Inc., ticker: AAPL
    'Microsoft Corporation (MSFT)': 'MSFT',     # Microsoft Corporation, ticker: MSFT
    'Amazon.com, Inc. (AMZN)': 'AMZN',          # Amazon.com Inc., ticker: AMZN
    'Alphabet Inc. Class A (GOOGL)': 'GOOGL',   # Alphabet Inc. Class A (Google), ticker: GOOGL
    'Alphabet Inc. Class C (GOOG)': 'GOOG',     # Alphabet Inc. Class C (Google), ticker: GOOG
    'Meta Platforms, Inc. (META)': 'META',      # Meta Platforms (formerly Facebook), ticker: META
    'Tesla, Inc. (TSLA)': 'TSLA',               # Tesla Inc., ticker: TSLA
    'NVIDIA Corporation (NVDA)': 'NVDA',        # NVIDIA Corporation, ticker: NVDA
    'JPMorgan Chase & Co. (JPM)': 'JPM'         # JPMorgan Chase, ticker: JPM
}

# ------------------ Default Date Range ------------------
# These variables define the default date range for fetching historical stock data.
# Users can modify these values to set the desired analysis period.

START_DATE = '2020-01-01'   # Start date for historical data (YYYY-MM-DD format).
END_DATE = '2023-12-31'     # End date for historical data (YYYY-MM-DD format).

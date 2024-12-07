# ---------------------------------------------------------
# RSI Backtesting Tool - Main Application
#
# Language:         Python
#
# Project Members:  Arthur, Samuel, Leo
#
# Final Review:     December 8, 2024
#
# Description:      This is the entry point of the RSI Backtesting Tool. It
#                   initializes and launches the application by creating
#                   an instance of the `BacktestApp` class from `app.py`.
#                   This script is responsible for starting the GUI-based 
#                   tool and ensuring it runs within the event loop.
#
# Assistance:       The structure, code design, and modularization of this project were 
#                   influenced by multiple resources, including ChatGPT, an AI language 
#                   model developed by OpenAI. Additional guidance and references were 
#                   drawn from YouTube tutorials, Stack Overflow discussions, and other 
#                   publicly available educational materials during the development process.
# ---------------------------------------------------------

# Import the BacktestApp class from the `subcode.app` module.
# The `BacktestApp` class contains the main logic and GUI setup 
# for the RSI Backtesting Tool.
from subcode.app import BacktestApp

# The standard Python entry point. This ensures that the following
# code runs only when this script is executed directly and not when 
# it is imported as a module in another script.

if __name__ == '__main__':
    # Create an instance of the BacktestApp class, which initializes
    # the application and its GUI components.
    app = BacktestApp()
    
    # Start the application's event loop. This ensures that the GUI
    # remains responsive to user interactions and continuously runs
    # until the user closes the application.
    app.mainloop()
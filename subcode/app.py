# ---------------------------------------------------------
# RSI Backtesting Tool - Backtest Application (GUI)
#
# Language:         Python
#
# Project Members:  Arthur, Samuel, Leo
#
# Final Review:     December 8, 2024
#
# Description:      This script defines the main graphical user interface (GUI) 
#                   for the RSI Backtesting Tool. The application allows users 
#                   to test RSI-based trading strategies on historical stock data. 
#                   It provides interactive components for user input, displays 
#                   metrics, and visualizes results.
# 
# Assistance:       The structure, code design, and modularization of this project were 
#                   influenced by multiple resources, including ChatGPT, an AI language 
#                   model developed by OpenAI. Additional guidance and references were 
#                   drawn from YouTube tutorials, Stack Overflow discussions, and other 
#                   publicly available educational materials during the development process.
# ---------------------------------------------------------

# ------------------ Library and Module Imports ------------------
# Import required libraries for GUI, plotting, and data calculations.

import tkinter as tk                                                # Import tkinter for GUI creation.
from tkinter import ttk                                             # Import ttk for modern GUI widgets.
from tkinter import messagebox                                      # Import messagebox for displaying pop-up messages.
import matplotlib.pyplot as plt                                     # Import matplotlib for plotting data.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Import for embedding matplotlib plots into tkinter.

import subcode.configuration                                                                                                            # Import project-specific configurations.
from subcode.calculation import get_historical_data, calculate_rsi, generate_signals, backtest_strategy, calculate_performance_metrics  # Import core functions for RSI calculations and backtesting.

# ------------------ Main Application Class ------------------
# This class defines the main GUI application for the RSI Backtesting Tool.
# It includes methods for creating widgets, handling user inputs, and displaying results.

class BacktestApp(tk.Tk):  # Define the main application class inheriting from tkinter's root class.
    def __init__(self):
        super().__init__()                  # Initialize the tkinter parent class.
        self.title("RSI Backtesting Tool")  # Set the application window title.
        self.geometry("1200x680")           # Set the initial size of the application window (width=1200, height=680).
        self.create_widgets()               # Call the method to create and arrange all widgets in the GUI.
        self.canvas = None                  # Initialize a placeholder for the canvas (for matplotlib plots).
        self.metrics_frame = None           # Initialize a placeholder for the metrics display frame.

    # ------------------ Widget Creation ------------------
    # This method sets up the main layout of the GUI, including frames for input, information, metrics, and results.

    def create_widgets(self):
        self.main_frame = tk.Frame(self)                    # Create the main frame that contains all subframes.
        self.main_frame.pack(fill=tk.BOTH, expand=True)     # Pack the main frame to fill the window and allow resizing.


        # ------------------ Input Section ------------------
        # The input section allows users to provide backtesting parameters like the company name, starting capital, fees, and RSI levels.
        self.input_frame = tk.Frame(self.main_frame)                            # Create the input frame for user inputs.
        self.input_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)   # Place the input frame in the grid (top-left).


        # ------------------ Info Section ------------------
        # The info section provides a textual explanation of the application's purpose and RSI functionality.

        self.info_frame = tk.Frame(self.main_frame)                             # Create the info frame for explanatory text about the app and RSI.
        self.info_frame.grid(row=0, column=1, sticky='nsw', padx=10, pady=10)   # Place the info frame to the right of the input frame.

        # Add a bold title label to the info frame.
        info_title = tk.Label(self.info_frame, text="RSI Backtesting Tool", font=("Helvetica", 10, "bold"), anchor="w")
        info_title.pack(fill=tk.X, pady=(0, 10))                                # Pack the title with horizontal fill and spacing below it.

        # Add a descriptive text label to explain RSI and the tool's purpose.
        info_label = tk.Label(self.info_frame, text=(
                "This application allows you to test a Relative Strength Index (RSI) "
                "trading strategy on historical stock data. The RSI is a momentum indicator "
                "that measures the speed and change of price movements. It ranges from 0 to 100 "
                "and is often used to identify overbought (above 70) and oversold (below 30) conditions.\n\n"
                "Use the input panel on the left to configure the backtest parameters, "
                "and view the plots in the section below and the metrics on the right."
            ), justify="left", wraplength=400, font=("Helvetica", 9), anchor="w")
        info_label.pack(fill=tk.BOTH, expand=True)                              # Pack the descriptive text.


        # ------------------ Summary Section ------------------
        # The summary section displays the backtesting performance metrics for RSI-based and buy-and-hold strategies.

        self.summary_frame = tk.Frame(self.main_frame)                          # Create the summary frame for displaying performance metrics.
        self.summary_frame.grid(row=0, column=2, sticky='ne', padx=10, pady=10) # Place the summary frame in the top-right corner.


        # ------------------ Results Section ------------------
        # The results section displays graphical outputs, including stock prices, RSI plots, and portfolio value charts.

        self.results_frame = tk.Frame(self.main_frame, padx=10, pady=10)        # Create the results frame for plots and charts.
        self.results_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')   # Place the results frame in the second row, spanning all columns.


        # ------------------ Layout Configuration ------------------
        # Configure the grid layout to make the results and input/summary frames resizable.

        self.main_frame.rowconfigure(1, weight=1)       # Make the results frame expandable vertically.
        self.main_frame.columnconfigure(0, weight=1)    # Make the input frame expandable horizontally.
        self.main_frame.columnconfigure(1, weight=1)    # Make the info frame expandable horizontally.
        self.main_frame.columnconfigure(2, weight=1)    # Make the summary frame expandable horizontally.


        # ------------------ Input Widgets ------------------
        # Define and place input widgets for setting backtesting parameters.

        input_font = ("Helvetica", 8)                                                               # Define a consistent font style for input widgets.

        self.company_label = ttk.Label(self.input_frame, text="Select Company:", font=input_font)   # Label for company selection.
        self.company_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)                       # Position the label in the input frame.

        self.company_var = tk.StringVar()                                                           # Variable to hold the selected company name.
        self.company_var.set('JPMorgan Chase & Co. (JPM)')                                          # Set the default company in the dropdown.
        self.ticker_map = subcode.configuration.COMPANIES                                           # Load the mapping of company names to tickers from configuration.

        self.company_dropdown = ttk.OptionMenu(self.input_frame, self.company_var, self.company_var.get(), *subcode.configuration.COMPANIES.keys())  # Create the dropdown for selecting a company.
        self.company_dropdown.config(width=25)                                                      # Set the width of the dropdown.
        self.company_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)                    # Position the dropdown next to the label.

        self.capital_label = ttk.Label(self.input_frame, text="Starting Capital ($):", font=input_font)     # Label for starting capital.
        self.capital_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)                               # Position the label below the company selection.

        self.capital_entry = ttk.Entry(self.input_frame, font=input_font)                                   # Entry widget for starting capital input.
        self.capital_entry.insert(0, "10000")                                                               # Set a default value of $10,000.
        self.capital_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)                               # Position the entry next to the label.

        self.fee_label = ttk.Label(self.input_frame, text="Fee per Trade (%):", font=input_font)            # Label for trade fees.
        self.fee_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)                                   # Position the label below the capital input.

        self.fee_entry = ttk.Entry(self.input_frame, font=input_font)                                       # Entry widget for trade fees input.
        self.fee_entry.insert(0, "0.1")                                                                     # Set a default value of 0.1%.
        self.fee_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)                                   # Position the entry next to the label.

        self.overbought_label = ttk.Label(self.input_frame, text="RSI Overbought Level:", font=input_font)  # Label for RSI overbought level.
        self.overbought_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)                            # Position the label below the fee input.

        self.overbought_entry = ttk.Entry(self.input_frame, font=input_font)                                # Entry widget for overbought level input.
        self.overbought_entry.insert(0, "70")                                                               # Set a default value of 70.
        self.overbought_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)                            # Position the entry next to the label.

        self.oversold_label = ttk.Label(self.input_frame, text="RSI Oversold Level:", font=input_font)      # Label for RSI oversold level.
        self.oversold_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)                              # Position the label below the overbought level.

        self.oversold_entry = ttk.Entry(self.input_frame, font=input_font)                                  # Entry widget for oversold level input.
        self.oversold_entry.insert(0, "30")                                                                 # Set a default value of 30.
        self.oversold_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)                              # Position the entry next to the label.

        self.run_button = ttk.Button(self.input_frame, text="Run Backtest", command=self.run_backtest)      # Button to execute the backtest.
        self.run_button.grid(row=5, column=0, columnspan=2, pady=10)                                        # Position the button below all inputs.

    # ------------------ Exit Application ------------------
    # This method gracefully exits the application by closing the GUI and destroying all widgets.

    def exit_application(self):
        self.quit()                 # Stop the tkinter main event loop.
        self.destroy()              # Destroy all widgets and close the application window.

    # ------------------ Run Backtest ------------------
    # This method handles the main backtesting process. It validates user inputs, retrieves historical data,
    # performs calculations, generates trading signals, and displays results in the GUI.

    def run_backtest(self):
        try:
            company_name = self.company_var.get()                           # Retrieve the selected company name from the dropdown.
            ticker = self.ticker_map[company_name]                          # Map the company name to its ticker symbol.
            initial_capital = float(self.capital_entry.get())               # Get the initial capital input and convert to float.
            if initial_capital <= 0:                                                            # Check if the initial capital is positive.
                raise ValueError("Starting capital must be positive.")                          # Raise an error if invalid.

            fee_percentage = float(self.fee_entry.get()) / 100                                  # Get the trade fee percentage and convert to decimal.
            if fee_percentage < 0:                                                              # Check if the fee percentage is non-negative.
                raise ValueError("Fee percentage cannot be negative.")                          # Raise an error if invalid.

            rsi_overbought = float(self.overbought_entry.get())                                 # Get the RSI overbought level and convert to float.
            if not (0 < rsi_overbought < 100):                                                  # Ensure the overbought level is between 0 and 100.
                raise ValueError("RSI Overbought level must be between 0 and 100.")             # Raise an error if invalid.

            rsi_oversold = float(self.oversold_entry.get())                                     # Get the RSI oversold level and convert to float.
            if not (0 < rsi_oversold < 100):                                                    # Ensure the oversold level is between 0 and 100.
                raise ValueError("RSI Oversold level must be between 0 and 100.")               # Raise an error if invalid.

            if rsi_oversold >= rsi_overbought:                                                  # Ensure oversold level is less than overbought level.
                raise ValueError("RSI Oversold level must be less than RSI Overbought level.")  # Raise an error if invalid.

        except ValueError as e:                                             # Catch input validation errors.
            messagebox.showerror("Input Error", str(e))                     # Display an error dialog with the message.
            return                                                          # Exit the method if inputs are invalid.

        # Retrieve configuration values for the start and end dates of the backtest.
        start_date = subcode.configuration.START_DATE       # Get the start date from the configuration module.
        end_date = subcode.configuration.END_DATE           # Get the end date from the configuration module.

        # Fetch historical stock data for the selected company and specified date range.
        data = get_historical_data(ticker, start_date, end_date)  
        if data.empty:                                                                          # Check if no data is returned.
            messagebox.showinfo("No Data", "No data available for the selected parameters.")    # Inform the user.
            return                                                                              # Exit the method if no data is available.

        data = calculate_rsi(data)                                          # Calculate the RSI values for the historical data.
        data = generate_signals(data, rsi_overbought, rsi_oversold)         # Generate buy/sell signals based on RSI thresholds.
        data = backtest_strategy(data, initial_capital, fee_percentage)     # Perform backtesting with the given parameters.

        # Calculate additional performance metrics for the strategy and add Buy-and-Hold results.
        data, metrics = calculate_performance_metrics(data, initial_capital)

        self.display_metrics(metrics)                                       # Display the calculated performance metrics in the summary frame.
        self.plot_results(data, company_name, rsi_overbought, rsi_oversold) # Plot the backtest results.

    # ------------------ Display Metrics ------------------
    # This method displays performance metrics (e.g., portfolio value, Sharpe ratio) in the summary frame.

    def display_metrics(self, metrics):
        if self.metrics_frame:              # Check if a previous metrics frame exists.
            self.metrics_frame.destroy()    # Destroy the previous metrics frame to clear old data.

        self.metrics_frame = tk.Frame(self.summary_frame)   # Create a new frame for the metrics.
        self.metrics_frame.pack(anchor='ne')                # Pack the frame into the top-right corner of the summary frame.

        label_font = ("Helvetica", 8)                       # Define the font style for the metrics text.

        # Define the table headers and the metrics labels to be displayed.
        headers = ["", "RSI-Strategy", "Buy-n-Hold"]                        # Column headers for the metrics table.
        metrics_labels = [                                                  # List of metrics to display in rows.
            "Portfolio Value", "Total Return", "Max. Drawdown", 
            "Volatility", "Sharpe Ratio", "Fees Paid", "Number of Trades"
        ]

        # Create the header row in the metrics table.
        for col, header in enumerate(headers):  # Loop through each header and its column index.
            header_label = tk.Label(self.metrics_frame, text=header, font=("Helvetica", 8, "bold"))     # Create a label for the header.
            header_label.grid(row=0, column=col, padx=5, pady=2)                                        # Position the header in the table.

        # Fill the table with metrics data.
        for row, metric in enumerate(metrics_labels, start=1):                                          # Loop through each metric and its row index.
            metric_label = tk.Label(self.metrics_frame, text=metric + ":", font=label_font)             # Label for the metric name.
            metric_label.grid(row=row, column=0, sticky='w', padx=5, pady=2)                            # Position the metric name in the first column.

            key = metric.lower().replace(" ", "_").replace(".", "")                                     # Generate the dictionary key for the metric.

            rsi_value = metrics.get(key, "")                                                            # Get the value of the metric for the RSI strategy.
            rsi_label = tk.Label(self.metrics_frame, text=rsi_value, font=label_font)                   # Create a label for the RSI value.
            rsi_label.grid(row=row, column=1, sticky='e', padx=5, pady=2)                               # Position the RSI value in the second column.

            bh_value = metrics.get("bh_" + key, "")                                                     # Get the value of the metric for the Buy-and-Hold strategy.
            bh_label = tk.Label(self.metrics_frame, text=bh_value, font=label_font)                     # Create a label for the Buy-and-Hold value.
            bh_label.grid(row=row, column=2, sticky='e', padx=5, pady=2)                                # Position the Buy-and-Hold value in the third column.

    # ------------------ Plot Results ------------------
    # This method visualizes the backtesting results, including stock price, RSI, and portfolio value.

    def plot_results(self, data, company_name, rsi_overbought, rsi_oversold):
        if self.canvas:                                                            # Check if a previous plot canvas exists.
            self.canvas.get_tk_widget().destroy()                                  # Destroy the previous canvas to clear old plots.

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True)   # Create a figure with 3 subplots.

        ax1.plot(data.index, data['Close'], label=f"{company_name} Price")              # Plot the stock price.
        trades = data[data['Trades'] != 0]                                              # Filter the data for executed trades.
        ax1.plot(trades.loc[trades['Trades'] == 1].index, trades['Close'][trades['Trades'] == 1], '^', markersize=10, color='g', label='Buy')       # Mark buy points.
        ax1.plot(trades.loc[trades['Trades'] == -1].index, trades['Close'][trades['Trades'] == -1], 'v', markersize=10, color='r', label='Sell')    # Mark sell points.
        ax1.set_title(f"{company_name} Price with Buy/Sell Signals")                    # Set the title for the stock price plot.
        ax1.set_ylabel('Price ($)')                                                     # Set the y-axis label for the stock price plot.
        ax1.legend(loc='lower left', fontsize=8)                                        # Add a legend to the stock price plot.
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)                     # Add a grid to the stock price plot.

        ax2.plot(data.index, data['RSI'], label='RSI')  # Plot the RSI values.
        ax2.axhline(y=rsi_overbought, color='r', linestyle='--', label=f'Overbought ({rsi_overbought})')    # Mark the overbought level.
        ax2.axhline(y=rsi_oversold, color='g', linestyle='--', label=f'Oversold ({rsi_oversold})')          # Mark the oversold level.
        ax2.set_title('Relative Strength Index (RSI)')                                                      # Set the title for the RSI plot.
        ax2.set_ylabel('RSI')                                                                               # Set the y-axis label for the RSI plot.
        ax2.legend(loc='lower left', fontsize=8)                                                            # Add a legend to the RSI plot.
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)                                         # Add a grid to the RSI plot.

        ax3.plot(data.index, data['Portfolio Value'], label='RSI-Strategy Portfolio Value')                                     # Plot the RSI strategy portfolio value.
        ax3.plot(data.index, data['Buy and Hold Portfolio Value'], label='Buy-n-Hold Portfolio Value', linestyle='--')          # Plot the Buy-and-Hold portfolio value.
        ax3.set_title('Portfolio Value Over Time')                                                                              # Set the title for the portfolio value plot.
        ax3.set_xlabel('Date')                                                                                                  # Set the x-axis label for all plots.
        ax3.set_ylabel('Portfolio Value ($)')                                                                                   # Set the y-axis label for the portfolio value plot.
        ax3.legend(loc='lower left', fontsize=8)                                                                                # Add a legend to the portfolio value plot.
        ax3.grid(True, which='both', linestyle='--', linewidth=0.5)                                                             # Add a grid to the portfolio value plot.

        plt.tight_layout()                                                          # Automatically adjust subplot spacing to prevent overlap.
        fig.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.12)           # Adjust figure margins.
        fig.subplots_adjust(hspace=0.5)                                             # Adjust vertical spacing between subplots.

        self.canvas = FigureCanvasTkAgg(fig, master=self.results_frame)             # Embed the figure into the tkinter GUI.
        self.canvas.draw()  # Render the canvas.
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)    # Pack the canvas into the results frame.

# ------------------ Run the Application ------------------
# This code ensures the application runs only when executed directly, not when imported as a module.

if __name__ == '__main__':
    app = BacktestApp()     # Create an instance of the BacktestApp class.
    app.mainloop()          # Start the tkinter event loop to display the GUI.

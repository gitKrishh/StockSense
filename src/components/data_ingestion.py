import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# --- 1. Define the Tickers and Date Range ---

# List of Indian stock tickers.
# .NS suffix is for the National Stock Exchange (NSE).
# ^NSEI is the ticker for the NIFTY 50 index.
tickers_list = ["RELIANCE.NS", "TCS.NS", "^NSEI"]

# Set the end date to today
end_date = datetime.today()

# Set the start date to 10 years ago from today
start_date = end_date - timedelta(days=10*365)

# Format dates into 'YYYY-MM-DD' string format, which yfinance expects
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

print(f"Fetching data for: {', '.join(tickers_list)}")
print(f"From {start_date_str} to {end_date_str}\n")


# --- 2. Download the Historical Data ---

# Use yf.download() to get the data for all tickers at once.
# The data is returned as a pandas DataFrame with multi-level columns.
# 'group_by="ticker"' is False by default, which groups data by OHLCV columns.
try:
    data = yf.download(tickers_list,
                       start=start_date_str,
                       end=end_date_str,
                       progress=True) # Shows a progress bar

    # Check if the downloaded data is empty
    if data.empty:
        print("No data downloaded. Check the ticker symbols and date range.")
    else:
        # --- 3. Display and Save the Data ---

        # Display the last 5 rows of the downloaded data
        print("\n--- Sample of Downloaded Data ---")
        print(data.tail())

        # The columns are multi-level. For example, to access the 'Close' price for Reliance:
        # print(data['Close']['RELIANCE.NS'].tail())

        # Save the entire DataFrame to a CSV file
        output_filename = "indian_stocks_10_years.csv"
        data.to_csv(output_filename)

        print(f"\n✅ Data successfully downloaded and saved to '{output_filename}'")

except Exception as e:
    print(f"An error occurred: {e}")


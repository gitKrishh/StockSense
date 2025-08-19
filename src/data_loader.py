import pandas as pd
import glob
import os

def load_all_data(data_dir: str) -> pd.DataFrame:
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    all_df_list = []

    print(f"Found {len(csv_files)} CSV files to load.")

    for file in csv_files:
        df = pd.read_csv(file)

        ticker = os.path.splitext(os.path.basename(file))[0]
        df['Ticker'] = ticker

        all_df_list.append(df)


    combined_df = pd.concat(all_df_list, ignore_index=True)

    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    combined_df.set_index(['Date', 'Ticker'], inplace=True)
    combined_df.sort_index(inplace=True) 

    print("Successfully created multi-index DataFrame.")
    
#checking the missing values

    missing_values = combined_df.isnull().sum()
    if missing_values.sum() > 0:
        print("\nMissing values found. Forward-filling them...")
        print(missing_values[missing_values > 0])

        combined_df.fillna(method='ffill', inplace=True)

        combined_df.fillna(method='bfill', inplace=True)
    else:
        print("\nNo missing values found.")

    return combined_df

if __name__ == '__main__':

    RAW_DATA_PATH = '../data/raw' 
    
    master_df = load_all_data(RAW_DATA_PATH)
    
    print("\n--- DataFrame Head ---")
    print(master_df.head())
    
    print("\n--- DataFrame Info ---")
    master_df.info()
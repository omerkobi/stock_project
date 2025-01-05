import pandas as pd
import requests as re
import json



####################
def get_matching_series(search_term, api_key):
    url_search = f'https://api.stlouisfed.org/fred/series/search?search_text={search_term}&api_key={api_key}&file_type=json'
    response = re.get(url_search)

    if response.status_code == 200:
        series = response.json()
        series_dict = series.get('seriess', [])
        # Extract (id, notes) for matching series
        matching_series = [(dic['id'], dic['notes'].split(".")[0]) for dic in series_dict if 'id' in dic and 'notes' in dic and
                           search_term.lower() in dic['notes'].split(".")[0].lower()]
        return matching_series
    else:
        st.error("Failed to fetch series. Check your API key or network connection.")
        return []

# Function to fetch data for a specific series ID
def get_series_data(series_id, start_date, api_key):
    url_data = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}'
    response = re.get(url_data)

    if response.status_code == 200:
        data = response.json()
        observations = data.get('observations', [])
        df = pd.DataFrame(observations)
        #df = df[['date', 'value']]  # Keep only date and value columns
        df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Convert value to numeric
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        #df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['change_from_last'] = df['value'].pct_change() * 100 # creating a collumn with the presentage change from the last value
        df['change_from_last'] = df['change_from_last'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else None)
        df['change_from_last'] = df['change_from_last'].str.rstrip('%').astype(float)  # Convert percentage strings to numeric
        df['yearly_change'] = None # creat new collumn for the yearly presentage change
        df['date'] = df['date'].dt.strftime('%Y-%m-%d') # removes the 00:00:00
        # iterate over the rows to match the year before data
        for index, row in df.iterrows():
            #find the matching row from the year before
            mask = (df['year'] == row['year'] -1 ) & (df['month'] == row['month'])
            previous_row = df.loc[mask] # locking the year before data
             #if matching row as found calculate the presentage change
            if not previous_row.empty:
                df.at[index, 'yearly_change'] = round((row['value'] / previous_row['value'].values[0] -1) *100,1) # specific value from the index and the column

        df = df.dropna(subset=['change_from_last','yearly_change'], inplace=False) #df = df.dropna(subset=['change_from_last','yearly_change'], inplace=True)
        return df   #df[['date', 'value','change_from_last']] # returning only the intresting collumn
    else:
        st.error("Failed to fetch data for the selected series.")
        return None


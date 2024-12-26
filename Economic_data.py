import pandas as pd
import requests as re
import json





fred_key = '25af470e22d07300c84e19895ed91600'
data_type = "CPIAUCSL"
start_data_date = '2000-01-01'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={data_type}&api_key={fred_key}&file_type=json&observation_start={start_data_date}'
##########
serach_code = 'nonfarm' # what data i would like to find
url2 = f'https://api.stlouisfed.org/fred/series/search?search_text={serach_code}&api_key={fred_key}&file_type=json' # in order to find the series id
fred_series = re.get(url2)
if fred_series.status_code == 200:
    # Print the JSON response
    print('ok')
    #print(fred2.text)
    #print(fred2.json())
    print(type(fred_series.json()))
else:
    print(f"Error: {fred_series.status_code}")

series = fred_series.json()
series_dict = series.get('seriess',[])
full_lst =  [(dic['id'],dic['notes']) for dic in series_dict if 'id' in dic and 'notes' in dic]
tup_lst_id_note = [(dic['id'],dic['units_short'], dic['notes'].split(".")[0]) for dic in series_dict if 'id' in dic and 'notes' in dic] # list of tuples containing the data id and explanation
#serach_code = 'GDP' # what data i would like to find
data_codes = [dic['id'] for dic in series_dict if 'notes' in dic and f'{serach_code}' in dic['notes'].split(".")[0]] # list of series code that muches my search_code
#print(data_codes)
#['CPIAUCSL', 'CPILFESL', 'CPILFENS'] - consumers A191RL1Q225SBEA -GDP PAYEMS- nonfarm
for l in full_lst:
    if 'PAYEMS' in l:
        print(l)

for i in tup_lst_id_note:
    for id_ in data_codes:
        if id_ in i:
            print(i)
#for i in tup_lst:
    #if 'GEPUCURRENT' in i:
        #print(i)

#### gettind the data
#fred = re.get(url)
#df = pd.DataFrame()
#if fred.status_code == 200:
#    data = fred.json() # getting a dict object
#    observations = data.get("observations", []) # extracting the data which is under the observation key
#    df = pd.DataFrame(observations) # put the data in a data frame
#    df['date'] = pd.to_datetime(df['date'])
#    df['value'] = df['value'].astype(float) # value is str convert to float in order to calculate the % change
#print(df.tail(20))
#    df['change_from_last'] = df['value'].pct_change() * 100
#    df['change_from_last'] = df['change_from_last'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "NaN")
#    df['yearly_change'] = (df['value'] / df['value'].shift(12) - 1) * 100 # calculate the yearly change
#    df['yearly_change'] = df['yearly_change'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "NaN")
#print(df.tail(20))
#else :
#    print('error type: ', fred.status_code)

#print(df.tail(10))
g = "KJbb(GDP)55"
print(g.lower())

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
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['change_from_last'] = df['value'].pct_change() * 100 # creating a collumn with the presentage change from the last value
        df['change_from_last'] = df['change_from_last'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else None)
        df['change_from_last'] = df['change_from_last'].str.rstrip('%').astype(float)  # Convert percentage strings to numeric
        df = df.dropna(subset=['change_from_last'])
        return df #df[['date', 'value','change_from_last']] # returning only the intresting collumn
    else:
        st.error("Failed to fetch data for the selected series.")
        return None


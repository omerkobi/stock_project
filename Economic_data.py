import pandas as pd
import requests as re
import json





fred_key = '25af470e22d07300c84e19895ed91600'
data_type = "CPIAUCSL"
start_data_date = '2000-01-01'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={data_type}&api_key={fred_key}&file_type=json&observation_start={start_data_date}'
##########
url2 = f'https://api.stlouisfed.org/fred/series/search?search_text=index+monetary&api_key={fred_key}&file_type=json' # in order to find the series id
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
tup_lst_id_note = [(dic['id'], dic['notes'].split(".")[0]) for dic in series_dict if 'id' in dic and 'notes' in dic] # list of tuples containing the data id and explanation
serach_code = 'GDP' # what data i would like to find
data_codes = [dic['id'] for dic in val if 'notes' in dic and f'{serach_code}' in dic['notes'].split(".")[0]] # list of series code that muches my search_code
#for i in tup_lst:
    #if 'GEPUCURRENT' in i:
        #print(i)

#### gettind the data
fred = re.get(url)
df = pd.DataFrame()
if fred.status_code == 200:
    data = fred.json() # getting a dict object
    observations = data.get("observations", []) # extracting the data which is under the observation key
    df = pd.DataFrame(observations) # put the data in a data frame
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = df['value'].astype(float) # valu is str convert to float in order to calculate the % change
#print(df.tail(20))
    df['monthly_change'] = df['value'].pct_change() * 100
    df['monthly_change'] = df['monthly_change'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "NaN")
    df['yearly_change'] = (df['value'] / df['value'].shift(12) - 1) * 100 # calculate the yearly change
    df['yearly_change'] = df['yearly_change'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "NaN")
#print(df.tail(20))
else :
    print('error type: ', fred.status_code)

print(df.tail(10))



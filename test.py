#import streamlit as st
import requests as re
import pandas as pd
print('I was here')
print('hello')
print('say hello my friend')
######### streamlit ###########
st.markdown("""

# Title



## Subtitle

- bullet1
- bullet2
- bullet3


> Amazing Quote
""")
st.radio("what kind of data would ypu like to see",['economic date','stock data'])

df=sns.load_dataset("penguins")
plot_choice = st.radio("choose what would you like to see",['economic data','stock data']) # telling the user to pick
fig, axe = plt.subplots() # creat a new figure, get the axes object
sns.scatterplot(data=df,x= "flipper_length_mm", y= "bill_length_mm", hue="species", ax = axe)
st.pyplot(fig)

#st.markdown('''
#Title
##subtitle

#-bullet1
#-bullet2
#bullet3

#> Amazingv quote :
#''')

#st.radio("Which desert is better?", ["cake","ice cream","Pie"])

################## API ##################
categories_url = 'https://api.chucknorris.io/jokes/categories'
response = re.get(categories_url)
response.raise_for_status() # 200 ok
print(response.text)

########## Using jason ##########
import  json
categories = json.loads(response.text)
print(type(categories))

#### Shorter way using json ######
print(response.json())
print(response.json()[1])


def get_chuck_norris_joke_by_category(category):
    url = f"https://api.chucknorris.io/jokes/random?category={category}"
    response = re.get(url)
    response.raise_for_status()
    return response.json()


# Try categories like 'animal', 'career', 'celebrity'
joke_dict = get_chuck_norris_joke_by_category('animal')
# print(joke_dict)
print(joke_dict['value'])

obj = [{}, 1,2,3, ["abc"], {"name": "moshe"}]
type(obj)  # list
result = json.dumps(obj)
print(type(result), repr(result))


### requasting wether

url = "https://catfact.ninja/fact"
response = re.get(url)
print(response.json().keys())
print(response.json()['fact'])

key_words = ['Consumers','GDP','Payroll','PPI']
fred_key = '25af470e22d07300c84e19895ed91600'
data_type = 'PAYEMS'#"A191RL1Q225SBEA"#"GDP"#"CPIAUCSL"
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={data_type}&api_key={fred_key}&file_type=json&observation_start=2000-01-01'
url2 = f'https://api.stlouisfed.org/fred/series/search?search_text=A191RL1Q225SBEA&api_key={fred_key}&file_type=json'#&search_type=series_id'
fred2 = re.get(url2)
if fred2.status_code == 200:
    # Print the JSON response
    print('ok')
    #print(fred2.text)
    #print(fred2.json())
    print(type(fred2.json()))
else:
    print(f"Error: {fred2.status_code}")
#series_id = fred2.text
series = fred2.json()
val = series.get('seriess',[])
#print(val)
#units_short
full_lst =  [(dic['id'],dic['notes']) for dic in val if 'id' in dic and 'notes' in dic]
tup_lst = [(dic['id'],  dic['units_short'] ,dic['notes'].split(".")[0]) for dic in val if 'id' in dic and 'notes' in dic] # list of tuples containing the data id and explanation
#data_codes = [dic['id'] for dic in val if 'Consumer' in dic['notes'].split(".")[0]]
#data_codes = [dic['id'] for dic in val if 'Consumer' in dic['notes'].split(".")[0] and 'notes' in dic ]
serach_code = 'GDP'
data_codes = [dic['id'] for dic in val if 'notes' in dic and f'{serach_code}' in dic['notes'].split(".")[0]]
print(data_codes)
#['CPIAUCSL', 'CPILFESL', 'CPILFENS'] - consumers A191RL1Q225SBEA -GDP PAYEMS- nonfarm
for i in tup_lst:
    for id_ in data_codes:
        if id_ in i:
            print(i)

#print(tup_lst)
#print(type(val[1]))
#print(val)
#print(fred2.json())
fred = re.get(url)
print(fred.text)
print(type(fred.text))
print(type(fred.json()))
#print(fred.json())


data = fred.json()
observations = data.get("observations", [])
df = pd.DataFrame(observations)
df['date'] = pd.to_datetime(df['date'])
df['value'] = df['value'].astype(float)
print(df.tail(20))
value_2024 = df.loc[df['date'] == '2024-11-01', 'value'].values
value_2023 = df.loc[df['date'] == '2023-11-01', 'value'].values
#val = (df.loc[df['date'] =='2024-04-01','value'] - df.loc[df['date'] =='2023-04-01','value' ] ) / df.loc[df['date'] =='2023-04-01','value' ]
print('the value is : ',type(df.loc[df['date'] =='2024-04-01','value']))
#print(val)
print(value_2024,value_2023)
cpi = (value_2024 -value_2023) / value_2023
print(cpi)
cpi = str(cpi *100) +"%"
print(cpi)


#############  Draft of the project #############


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
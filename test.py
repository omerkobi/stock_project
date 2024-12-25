#import streamlit as st
import requests as re
import pandas as pd
print('I was here')
print('hello')
print('say hello my friend')
######### streamlit ###########
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

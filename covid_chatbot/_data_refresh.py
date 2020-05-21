import pandas as pd
import requests
import json

url1 = f'https://api.covid19india.org/data.json'
url2 = f'https://api.covid19india.org/v2/state_district_wise.json'

response1 = requests.get(url1)
response1_dict = json.loads(response1.text)

response2 = requests.get(url2)
response2_dict = json.loads(response2.text)

final_state_list = []
final_district_list = []
valid_distrcit_key = ['district','confirmed']
valid_state_key = ['active','recovered','state','deaths','confirmed']

for state_dict in con_dic['statewise']:
    temp = (list(map(lambda key,value :  key+"#"+value if key in valid_state_key else None , state_dict.keys(),state_dict.values() )))
    final_state_list.append(" ".join(list(filter(None, temp))) )

for response in response2_dict:
    state = response['state']
    for district in response['districtData']:
        temp = (list(map(lambda key,value :  key+"#"+str(value) if key in valid_distrcit_key else None  , district.keys(),district.values())))
        final_district_list.append(" ".join(list(filter(None, temp))))

state_dataframe = pd.DataFrame({'Question' : final_state_list, 'Answer' : final_state_list})
district_dataframe = pd.DataFrame({'Question':final_district_list,'Answer':final_district_list})
final_dataframe = pd.concat([d1,d2])
final_dataframe.to_excel('Data.xlsx',index=False);
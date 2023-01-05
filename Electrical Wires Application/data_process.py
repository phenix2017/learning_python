import pandas as pd
import os.path

file_name = ".\google_test2.csv"
file_name_1 = ".\google_electrician_toronto.csv"
file_obs_path = os.path.realpath(file_name)
file_obs_path_1 = os.path.realpath(file_name_1)
df = pd.read_csv(file_obs_path)
df_1 = pd.read_csv(file_obs_path_1)
df_1.shape
df = pd.concat([df,df_1], axis='index',join='outer')
df.shape
df.columns
df1 = df.iloc[:,1:3].reset_index(drop=True)
company_info = [df1.iloc[i,0].split('\n') for i in range(df1.shape[0])]
# company_info format
# Name, Rate, Category, Location, Open Close Phone
company_info[0][0]
company_name = [company_info[i][0] for i in range(df1.shape[0])]
len(company_name)
import numpy as np
import re
phone_list = []
for index in range(df1.shape[0]):
    if len(company_info[index]) >=5: # 0, 1, 2, 3, 4
        potential_phone = company_info[index][4].split("\xb7")[-1]
        phone_number = re.sub("[^0-9]", "", potential_phone)
        if len(phone_number) >= 10:
            phone_list.append(phone_number)
        else:
            phone_list.append(np.nan)
    else:
        phone_list.append(np.nan)
len(phone_list)

df_ = pd.DataFrame({"Company":[], "Phone":[], "Web":[]})
df_['Company'] = company_name
df_['Phone'] = phone_list
df_['Web'] = df1['href']

# Remove replicats
new_df = df_.drop_duplicates(subset='Phone').dropna().reset_index(drop=True)
new_df.to_csv("electrician_GTA.csv",encoding='utf-8-sig')
import pandas as pd
import datetime
file_name = "allcontact.xlsx"
df = pd.read_excel(file_name)
# Find all the duplicates
duplicated_rows = df.duplicated(subset="First Name", keep=False)
# Get the duplicates rows timesheet
s = df[duplicated_rows]['Latest Source Timestamp']
# Get the index where the duplicates 
index = s[s.iloc[:] < datetime.datetime(2023,1,1)].index
df.drop(labels=index,inplace=True)
df[df.duplicated(subset="First Name",keep=False)].shape[0]
df[df.duplicated(subset="First Name",keep=False)].index
first_name_mobile_index = df[df.duplicated(subset=["First Name","Mobile Phone Number"],keep='first')].index
df.drop(labels=first_name_mobile_index,inplace=True)
df.to_excel("removed_duplicates.xlsx",encoding='utf_8_sig', index=False)
import pandas as pd
import os
# os.path.exists()
path = '.\google_test2.csv'
real_path = os.path.realpath(path)
real_path
df = pd.read_csv(real_path)
df.columns[0]
df.drop(columns=[df.columns[0]], inplace=True)
df.columns

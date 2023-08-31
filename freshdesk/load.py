import pandas as pd
import os
import freshdesk.config.local_vars as conf

# Get the file path of all the files
filepath = conf.DATA_FOLDER

os.chdir(filepath)

# Get the list of all the files from the path
file_list = (os.listdir())

for file in file_list:
    df = pd.read_csv(file)
    print(df)
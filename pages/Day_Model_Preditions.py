import streamlit as st
import s3fs
import os
from io import StringIO
import pandas as pd
from datetime import datetime

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

content = read_file("s3://pmpf-data/sagemaker-xgboost-prediction/data/test.csv")

COLUMNS = ['failure_comp2', 'datetime', 'machineID', 'volt', 'rotate', 'pressure',
       'vibration', 'age', 'anomaly', 'error1', 'error2', 'error3', 'error4',
       'error5', 'maint_comp1', 'maint_comp2', 'maint_comp3', 'maint_comp4',
       'model1', 'model2', 'model3', 'model4', 'error1_convolve_24',
       'error2_convolve_24', 'error3_convolve_24', 'error4_convolve_24',
       'error5_convolve_24', 'maint_comp1_convolve_24',
       'maint_comp2_convolve_24', 'maint_comp3_convolve_24',
       'maint_comp4_convolve_24']

df = pd.read_csv(StringIO(content), header=None)
df.iloc[:,1] = pd.to_datetime(df.iloc[:,1])

# Getting Machine, year, month, day, and hours available --
dates = df.iloc[:, 1]
max_date = dates.iloc[-1]
min_date = dates.iloc[0]
years = set([d.year for d in dates])
months = set([d.month for d in dates])
days = set([d.day for d in dates])
hours = set([d.hour for d in dates])

machine_ids = set(list(df.iloc[:,2]))

# Call Model ----------------------------------------------

import boto3
sagemaker = boto3.client('sagemaker-runtime')

def get_row(date):
    row = df.loc[df[1] == date]
    return row

def get_prediction(row):
    df_row = pd.DataFrame(row)
    res = sagemaker.invoke_endpoint(
                    EndpointName='sagemaker-xgboost-2023-02-12-00-09-14-542',
                    Body=df_row.iloc[:, 1:].to_csv(index=False, header=False),
                    ContentType='text/csv',
                    Accept='Accept'
                )
    prediction =  res['Body'].read().decode('UTF-8')
    return prediction

def update_cell(m_id, year, month, day, hour):
    message = ""
    date = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour))
    row = pd.DataFrame()
    if date < min_date:
        message = "Please select a date after " + str(min_date)
    elif date > max_date:
        message = "Please select an before date " + str(max_date)
    else:
        row = df.loc[(df.iloc[:,2] == m_id) & (df.iloc[:,1] == date)]
        row[1] = 0 # setting the date to zero
        p = get_prediction(row)
        message = f"Predicition: {p} Grouth Truth: {row.iloc[0, 0]}"
        row.columns = COLUMNS
    return message, row

# Actual Front-end -------------------------------

st.title("24-hour Prediction Model")

st.write("The DayModel will look at the data for a given time stamp and predict if component 2 will fail within 24 hours.")

st.write("Note: Predicted failures are rare, some examples include: machine 7 on 2015-10-20 07:00:00 or machine 97 on 2015-10-20 07:00:00.")

machine = st.selectbox("Machine ID:", tuple(list(machine_ids)))
year =    st.selectbox("Year:      ", tuple(list(years)))
month =   st.selectbox("Month:     ", tuple(list(months)))
day =     st.selectbox("Day:       ", tuple(list(days)))
hour =   st.selectbox("Hours:     ", tuple(list(hours)))

st.write(update_cell(machine, year, month, day, hour)[0])

col1, col2, col3 = st.columns(3)
with col1:
    st.write("Telemetric Information:")
    st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 2:8])

with col2:
    st.write("Error Codes:")
    st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 9:14])

with col3:
    st.write("Maintenance Codes:")
    st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 14:18])

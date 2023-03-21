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

content = read_file("s3://pmpf-data/sagemaker-xgboost-prediction/data/test_02_12_16.csv")

COLUMNS = ['failure_comp2', 'datetime', 'machineID', 'volt', 'rotate', 'pressure',
       'vibration', 'age', 'anomaly', 'error1', 'error2', 'error3', 'error4',
       'error5', 'maint_comp1', 'maint_comp2', 'maint_comp3', 'maint_comp4',
       'model1', 'model2', 'model3', 'model4', 'error1_in_past_48',
       'error2_in_past_48', 'error3_in_past_48', 'error4_in_past_48',
       'error5_in_past_48', 'maint_comp1_in_past_48',
       'maint_comp2_in_past_48', 'maint_comp3_in_past_48',
       'maint_comp4_in_past_48']

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
sagemaker = boto3.client('sagemaker-runtime', region_name="us-west-1")

def get_row(date):
    row = df.loc[df[1] == date]
    return row

def get_prediction(row):
    df_row = pd.DataFrame(row)
    res = sagemaker.invoke_endpoint(
                    EndpointName='sagemaker-xgboost-2023-03-21-05-02-43-436',
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
        message = f"Prediction: {p} Ground Truth: {row.iloc[0, 0]}"
        row.columns = COLUMNS
    return message, row

# Actual Front-end -------------------------------

st.title("48-hour Prediction Model")

st.write("The Two Day Model will look at the data for a given time stamp and predict if component 2 will fail within 48 hours.")

st.write("Note: Predicted failures are rare, some examples include: machine 7 on 2015-10-20 07:00:00 or machine 97 on 2015-10-20 07:00:00.")

machine = st.selectbox("Machine ID:", tuple(list(machine_ids)))
year =    st.selectbox("Year:      ", tuple(list(years)))
month =   st.selectbox("Month:     ", tuple(list(months)))
day =     st.selectbox("Day:       ", tuple(list(days)))
hour =   st.selectbox("Hours:     ", tuple(list(hours)))

st.write(update_cell(machine, year, month, day, hour)[0])

with st.expander("Model Inputs"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Telemetric Information:")
        try:
            st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 2:8])
        except IndexError:
            pass

    with col2:
        st.write("Errors in past 48 hrs:")
        try:
            st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 22:27])
        except IndexError:
            pass

    with col3:
        st.write("Maintenance in past 48 hrs:")
        try:
            st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 27:32])
        except IndexError:
            pass

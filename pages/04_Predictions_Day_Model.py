import streamlit as st
import os
import pandas as pd
from datetime import datetime

import src.data as data
COLUMNS = data.DayModelData.COLUMNS

model_data = data.DayModelData()
df = model_data.get_df()
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
sagemaker = boto3.client('sagemaker-runtime', region_name="us-west-1",
                        aws_access_key_id=os.environ["ACCESS_KEY"],
                        aws_secret_access_key=os.environ["SECRET_KEY"])

def get_row(date):
    row = df.loc[df[1] == date]
    return row

def get_prediction(row):
    df_row = pd.DataFrame(row)
    res = sagemaker.invoke_endpoint(
                    EndpointName='sagemaker-xgboost-2023-03-21-04-37-03-129',
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

st.title("24-hour Prediction Model")

st.write("The DayModel will look at the data for a given time stamp and predict if component 2 will fail within 24 hours.")

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
        st.write("Errors in past 24 hrs:")
        try:
            st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 22:27])
        except IndexError:
            pass

    with col3:
        st.write("Maintenance in past 24hr:")
        try:
            st.dataframe(update_cell(machine, year, month, day, hour)[1].iloc[0, 27:32])
        except IndexError:
            pass

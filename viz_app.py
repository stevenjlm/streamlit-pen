import streamlit as st
import s3fs
import os
from io import StringIO
import pandas as pd
from constants import APP_DIR

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False,
                        key=st.secrets["ACCESS_KEY"],
                        secret=st.secrets["SECRET_KEY"])

# Retrieve file contents.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

content = read_file("s3://pmpf-data/sagemaker-xgboost-prediction/data/test.csv",
                        aws_access_key_id=st.secrets["ACCESS_KEY"],
                        aws_secret_access_key=st.secrets["SECRET_KEY"])

df = pd.read_csv(StringIO(content), header=None)
df.iloc[:,1] = pd.to_datetime(df.iloc[:,1])

dates = df.iloc[:, 1]
first_n_dates = list(dates[:10])
options = [str(d) for d in first_n_dates]

""" Call Model """

import boto3
sagemaker = boto3.client('sagemaker-runtime')

def get_row(date):
    row = df.loc[df[1] == date]
    return row

def get_prediction(row):
    df_row = pd.DataFrame(row)
    res = sagemaker.invoke_endpoint(
                    EndpointName='sagemaker-xgboost-2023-02-10-04-30-05-328',
                    Body=df_row.iloc[:, 1:].to_csv(index=False, header=False),
                    ContentType='text/csv',
                    Accept='Accept'
                )
    prediction =  res['Body'].read().decode('UTF-8')
    return prediction

def update_cell(date):
    row = get_row(date)
    row[1] = 0
    ## hack to get first row
    p = get_prediction(row.iloc[[0]])
    return p

""" Actual App Front-end """

st.title("Azure Predictive Maintenance Challenge")

st.subheader("Test Data")

date = st.selectbox("Which Date would you like to test?", tuple(options))

st.write(update_cell(date))

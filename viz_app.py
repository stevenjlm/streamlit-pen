import streamlit as st
import s3fs
import os
from io import StringIO
import pandas as pd

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

content = read_file("pmpf-data/sagemaker-xgboost-prediction/data/test.csv")

df = pd.read_csv(StringIO(content), header=None)
df.iloc[:,1] = pd.to_datetime(df.iloc[:,1])

dates = df.iloc[:, 1]
first_n_dates = list(dates[:10])
options = [str(d) for d in first_n_dates]

""" Actual App Front-end """

st.title("Azure Predictive Maintenance Challenge")

st.subheader("Test Data")

date = st.selectbox("Which Date would you like to test?", tuple(options))

st.write(date)

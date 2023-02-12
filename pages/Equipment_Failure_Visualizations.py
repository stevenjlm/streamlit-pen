import streamlit as st
import s3fs
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
import matplotlib.pyplot as plt
# Using plotly.express
import plotly.express as px

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

failures = df.loc[df[0] == True]
machine_ids = list(failures[2].unique())

def get_dates_for_machine(m_id):
    dates = list(failures.loc[failures[2] == int(m_id)][1])
    return dates[::-1]

def make_plot(machine, date, column, hours):
    machine_signal = df.loc[df[2] == int(machine)]
    machine_signal.columns = COLUMNS
    end_date = date
    start_date = date - timedelta(hours=hours)

    time_window_signal = machine_signal[(machine_signal['datetime'] >= start_date) & (machine_signal['datetime'] <= end_date)]

    return px.line(time_window_signal, x='datetime', y=column, title=f"{column} vs Time for Machine {machine}")
    # plt.rcParams['figure.figsize'] = [10, 5]
    # plt.title(f"{column} vs Time for Machine {machine}")
    # plt.plot(t, y, "xb")
    # plt.xticks(rotation = 45)
    # return plt.gcf()



# Actual Front-end -------------------------------

st.title("Visualize Data Before a Component Failure")

col1, col2 = st.columns(2)

with col1:
    machine = st.selectbox("Machine ID:", tuple(machine_ids))
    date = st.selectbox("Dates:", tuple(get_dates_for_machine(machine)))

with col2:
    column = st.selectbox("Quantity:", tuple(COLUMNS[3:]))
    hours = st.selectbox("Hours:", tuple([12,24,42,72,161]))

st.plotly_chart(make_plot(machine, date, column, hours))

st.write("Note: If there are no data points in the plot, select a later date.")

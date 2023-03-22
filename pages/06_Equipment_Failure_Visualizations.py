import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
# Using plotly.express
import plotly.express as px

import src.data as data
COLUMNS = data.DayModelData.COLUMNS

df = data.DayModelData.get_df()

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

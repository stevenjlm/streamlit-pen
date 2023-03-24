import streamlit as st
import time

import src.plots as plots
import src.data as data
COLUMNS = data.DayModelData.COLUMNS

model_data = data.DayModelData()
df = model_data.get_df()
machine_ids = model_data.get_machine_ids()
plotter = plots.DayModelPlotter()


# Actual Front-end -------------------------------

st.title("Visualize Data Before a Component Failure")

col1, col2 = st.columns(2)

with col1:
    machine = st.selectbox("Machine ID:", tuple(machine_ids))
    date = st.selectbox("Dates:", tuple(model_data.failure_dates_for_machine(machine)))

with col2:
    column = st.selectbox("Quantity:", tuple(COLUMNS[3:]))
    hours = st.selectbox("Hours:", tuple([12,24,42,72,161]))

chart = st.plotly_chart(plotter.plot_animation(machine, date, column, 1))
for t in range(2, hours):
    chart.empty()
    chart = st.plotly_chart(plotter.plot_animation(machine, date, column, t))
    time.sleep(0.5)

st.write("Note: If there are no data points in the plot, select a later date.")

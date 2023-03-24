import streamlit as st

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
    hours = st.selectbox("Hours:", tuple([12,24,42,72,161]))

st.plotly_chart(plotter.plot_telem_animation(machine, date, hours))

column = st.selectbox("Indicator:", tuple(COLUMNS[7:]))

st.plotly_chart(plotter.plot_ts(machine, date, column, hours))

st.write("Note: If there are no data points in the plot, select a later date.")

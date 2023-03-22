import streamlit as st
from datetime import timedelta

import src.data as data


class DayModelPlotter:

    def __init__(self) -> None:
        self.columns = data.DayModelData.COLUMNS
        self.df = data.DayModelData.get_df()

    def plot_ts(self, machine, date, column, hours):
        machine_signal = self.df.loc[self.df[2] == int(machine)]
        machine_signal.columns = self.columns
        end_date = date
        start_date = date - timedelta(hours=hours)

        time_window_signal = machine_signal[(machine_signal['datetime'] >= start_date) & (machine_signal['datetime'] <= end_date)]

        return px.line(time_window_signal, x='datetime', y=column, title=f"{column} vs Time for Machine {machine}")
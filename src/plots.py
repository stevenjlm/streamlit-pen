import streamlit as st
from datetime import timedelta
import plotly.express as px

import src.data as data


class DayModelPlotter:

    def __init__(self) -> None:
        self.columns = data.DayModelData.COLUMNS
        self.model_data = data.DayModelData()
        self.df = self.model_data.get_df()

    def plot_ts(self, machine, date, column, hours):
        machine_signal = self.df.loc[self.df[2] == int(machine)]
        machine_signal.columns = self.columns
        end_date = date
        start_date = date - timedelta(hours=hours)

        time_window_signal = machine_signal[(machine_signal['datetime'] >= start_date) & (machine_signal['datetime'] <= end_date)]

        return px.line(time_window_signal, x='datetime', y=column, title=f"{column} vs Time for Machine {machine}")
    
    def plot_animation(self, machine, date, column, t):
        machine_signal = self.df.loc[self.df[2] == int(machine)]
        machine_signal.columns = self.columns
        end_date = date
        start_date = date - timedelta(hours=t)

        time_window_signal = machine_signal[(machine_signal['datetime'] >= start_date) & (machine_signal['datetime'] <= end_date)]

        return px.line(time_window_signal, x='datetime', y=column, title=f"{column} vs Time for Machine {machine}")
    
class HomePlotter:

    def __init__(self) -> None:
        self.df = data.read_home_page_data()

    def home_page_plot(self):
        pp_df = self.df
        fig = px.scatter(pp_df, x="x", y="y", color="status",
             # color_discrete_map=color_discrete_map,
             color_discrete_sequence=['#00FF00', '#FF0000'],
             animation_frame="day",
             title="Data Preview: Machine Status for December 2015")
             #range_y=[y_min, y_max])
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 0
        fig.update_xaxes(nticks=3, title="Machine ID 1s", zeroline=False)
        fig.update_yaxes(nticks=3, title="Machine ID 10s", zeroline=False)
        fig.update_traces(marker_size=10)
        return fig

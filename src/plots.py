import streamlit as st
from datetime import timedelta
import plotly.express as px
import numpy as np
import pandas as pd

import src.data as data


class DayModelPlotter:

    def __init__(self) -> None:
        self.columns = data.DayModelData.COLUMNS
        self.model_data = data.DayModelData()
        self.df = self.model_data.get_df()

    def plot_ts(self, machine, date, column, hours):
        time_window_signal = self.machine_time_signal(machine, date, hours)

        return px.line(time_window_signal, x='datetime', y=column, title=f"{column} vs Time for Machine {machine}")

    def machine_time_signal(self, machine, date, hours):
        machine_signal = self.df.loc[self.df[2] == int(machine)]
        machine_signal.columns = self.columns
        end_date = date
        start_date = date - timedelta(hours=hours)

        time_window_signal = machine_signal[(machine_signal['datetime'] >= start_date) & (machine_signal['datetime'] <= end_date)]
        return time_window_signal
    
    def plot_telem_animation(self, machine, date, hours):
        time_window_signal = self.machine_time_signal(machine, date, hours)

        telem_signal = time_window_signal.iloc[:, np.r_[1, 3:7]]

        telemetry_columns = ["Hours Before Failure", "Voltage (V)", "Rotation (degrees)", "Pressure (kPa)", "Vibration (No Unit)"]
        telem_signal.columns = telemetry_columns
        melted = pd.melt(telem_signal, id_vars="Hours Before Failure", var_name="Measure", value_name="Value")
        melted.iloc[:,0] = date - melted.iloc[:,0]
        melted.iloc[:,0] = melted.iloc[:,0].dt.components['hours'] + melted.iloc[:,0].dt.components['days']*24

        MARGIN = 10
        axes = ["yaxis", "yaxis2", "yaxis3", "yaxis4"]
        limits = {}
        for axis, col in zip(axes, telemetry_columns[1:]):
            column_df = melted.loc[melted["Measure"] == col]
            limits[axis] = [min(column_df.iloc[:, 2]) - MARGIN,
                            max(column_df.iloc[:, 2]) + MARGIN]
    
        fig = px.bar(melted, x="Measure", y="Value", color="Measure",
             # color_discrete_map=color_discrete_map,
             color_discrete_sequence=px.colors.qualitative.Plotly,
             animation_group="Measure",
             animation_frame="Hours Before Failure",
             facet_col="Measure",
             title="Telemetric Data")
             #range_y=[y_min, y_max])

        fig.update_yaxes(matches=None, showticklabels=True)
        for l in limits:
            fig.layout[l].update(range=limits[l])

        fig.for_each_annotation(lambda a: a.update(text=""))
        fig.update_xaxes(matches=None)
        return fig

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

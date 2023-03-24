import streamlit as st
import s3fs
from typing import List
from io import StringIO
import pandas as pd
from datetime import datetime

FAILURE_COL_IDX = 0
MACHINE_ID_COL_IDX = 2

# Retrieve S3 file contents.
# Uses st.cache_data to only rerun when the query changes or after 20 min.
@st.cache_data(ttl=1200)
def read_file(filename):
    # Create connection object.
    # `anon=False` means not anonymous, i.e. it uses access keys to pull data.
    fs = s3fs.S3FileSystem(anon=False)

    with fs.open(filename) as f:
        return f.read().decode("utf-8")

@st.cache_data(ttl=600)
def get_dataframe(filename: str) -> pd.DataFrame:
    content = read_file(filename)
    df = pd.read_csv(StringIO(content), header=None)
    return df


class APMData:

    def __init__(self) -> None:
        self.df = None
        self.failures = None
        self.machine_ids = None

    def get_machine_ids(self) -> List:
        self.failures = self.df.loc[self.df[FAILURE_COL_IDX] == True]
        self.machine_ids = list(self.failures[MACHINE_ID_COL_IDX].unique())
        return self.machine_ids

    def failure_dates_for_machine(self, m_id: str) -> List[str]:
        dates = list(self.failures.loc[self.failures[2] == int(m_id)][1])
        return dates[::-1]


class DayModelData(APMData):
    COLUMNS = ['failure_comp2', 'datetime', 'machineID', 'volt', 'rotate', 'pressure',
       'vibration', 'age', 'anomaly', 'error1', 'error2', 'error3', 'error4',
       'error5', 'maint_comp1', 'maint_comp2', 'maint_comp3', 'maint_comp4',
       'model1', 'model2', 'model3', 'model4', 'error1_in_past_24',
       'error2_in_past_24', 'error3_in_past_24', 'error4_in_past_24',
       'error5_in_past_24', 'maint_comp1_in_past_24',
       'maint_comp2_in_past_24', 'maint_comp3_in_past_24',
       'maint_comp4_in_past_24']
    FILENAME = "s3://pmpf-data/sagemaker-xgboost-prediction/data/test_02_12_12.csv"

    def __init__(self) -> None:
        super().__init__()

    def get_df(self) -> pd.DataFrame:
        if not self.df:
            self.df = get_dataframe(self.FILENAME)
            self.df.iloc[:,1] = pd.to_datetime(self.df.iloc[:,1])
        return self.df
    
class TwoDayModel(APMData):
    COLUMNS = ['failure_comp2', 'datetime', 'machineID', 'volt', 'rotate', 'pressure',
       'vibration', 'age', 'anomaly', 'error1', 'error2', 'error3', 'error4',
       'error5', 'maint_comp1', 'maint_comp2', 'maint_comp3', 'maint_comp4',
       'model1', 'model2', 'model3', 'model4', 'error1_in_past_48',
       'error2_in_past_48', 'error3_in_past_48', 'error4_in_past_48',
       'error5_in_past_48', 'maint_comp1_in_past_48',
       'maint_comp2_in_past_48', 'maint_comp3_in_past_48',
       'maint_comp4_in_past_48']
    FILENAME = "s3://pmpf-data/sagemaker-xgboost-prediction/data/test_02_12_16.csv"

    def __init__(self) -> None:
        super().__init__()

    def get_df(self) -> pd.DataFrame:
        if not self.df:
            self.df = get_dataframe(self.FILENAME)
            self.df.iloc[:,1] = pd.to_datetime(self.df.iloc[:,1])
        return self.df

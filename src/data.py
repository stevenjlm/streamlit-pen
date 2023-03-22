import streamlit as st
import s3fs
import os
from io import StringIO
import pandas as pd
from datetime import datetime

# Retrieve S3 file contents.
# Uses st.cache_data to only rerun when the query changes or after 20 min.
@st.cache_data(ttl=1200)
def read_file(filename):
    # Create connection object.
    # `anon=False` means not anonymous, i.e. it uses access keys to pull data.
    fs = s3fs.S3FileSystem(anon=False)

    with fs.open(filename) as f:
        return f.read().decode("utf-8")


class DayModelData:
    COLUMNS = ['failure_comp2', 'datetime', 'machineID', 'volt', 'rotate', 'pressure',
       'vibration', 'age', 'anomaly', 'error1', 'error2', 'error3', 'error4',
       'error5', 'maint_comp1', 'maint_comp2', 'maint_comp3', 'maint_comp4',
       'model1', 'model2', 'model3', 'model4', 'error1_in_past_24',
       'error2_in_past_24', 'error3_in_past_24', 'error4_in_past_24',
       'error5_in_past_24', 'maint_comp1_in_past_24',
       'maint_comp2_in_past_24', 'maint_comp3_in_past_24',
       'maint_comp4_in_past_24']
    FILENAME = "s3://pmpf-data/sagemaker-xgboost-prediction/data/test_02_12_12.csv"

    @classmethod
    @st.cache_data(ttl=600)
    def get_df(cls) -> pd.DataFrame:
        content = read_file(cls.FILENAME)
        df = pd.read_csv(StringIO(content), header=None)
        return df
    
class TwoDayModel:
    COLUMNS = ['failure_comp2', 'datetime', 'machineID', 'volt', 'rotate', 'pressure',
       'vibration', 'age', 'anomaly', 'error1', 'error2', 'error3', 'error4',
       'error5', 'maint_comp1', 'maint_comp2', 'maint_comp3', 'maint_comp4',
       'model1', 'model2', 'model3', 'model4', 'error1_in_past_48',
       'error2_in_past_48', 'error3_in_past_48', 'error4_in_past_48',
       'error5_in_past_48', 'maint_comp1_in_past_48',
       'maint_comp2_in_past_48', 'maint_comp3_in_past_48',
       'maint_comp4_in_past_48']
    FILENAME = "s3://pmpf-data/sagemaker-xgboost-prediction/data/test_02_12_16.csv"

    @classmethod
    @st.cache_data(ttl=600)
    def get_df(cls) -> pd.DataFrame:
        content = read_file(cls.FILENAME)
        df = pd.read_csv(StringIO(content), header=None)
        return df

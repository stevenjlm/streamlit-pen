import streamlit as st

from constants import APP_DIR
app_dir=APP_DIR

st.title("Input Data")

st.write("The APM challenge dataset consists of time-series data for machines in a cloud computing center. The goal of this web-app, after splitting data into \
         training, validation, and testing datasets, is to build a model to predict impending failures in the test data (data that it has never seen during learning).")
st.image(f"{app_dir}/img/task.png")

st.write("The Azure Predictive Maintenance Challenge dataset contains continuous-valued measurements for physical characteristics \
    of the equipment such as temperature, or pressure. It also tracks indicator variables specifying when errors, failures, and maintenance occur.")
st.image(f"{app_dir}/img/signals.png")

st.write("There are 100 machines labelled 1 to 100 in the data.")
st.image(f"{app_dir}/img/machines.png")

st.write("Each Machine has five components.")
st.image(f"{app_dir}/img/components.png")

st.write("In this project I focus on predicting failures for component 2.")
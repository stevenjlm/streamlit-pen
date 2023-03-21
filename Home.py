import streamlit as st
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
app_dir = config["DEFAULT"]["app_dir"]


st.title("Predictive Maintenance Tool for Azure Computing Data")

st.write("Steven Munn, March 20th 2023")

st.markdown(
"""
Tabs on the left allow you to:
- Infer likely failure time-intervals for components with the [Predictions Day Model](/Predictions_Day_Model) or [Predictions Two Day Model](/Predictions_Two_Day_Model).
- Visualize pre-failure data in the [Equipment Failure Visualizations](/Equipment_Failure_Visualizations) tab.
- Examine training reports in the [Reports](/Reports) tab.

The sections below give an overview of the predictive maintenance problem.
"""
)


with st.expander("Problem Description"):

    st.write("Using the Kaggle data-set for [Azure Predictive Maintenance Challenge](https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance) \
        this project explores ways to model and predict failures for component 2.")

with st.expander("Data Description"):

    st.image(f"{app_dir}/img/task.png")
    st.write("This project aims to train predictive models based on historical data from the APM challenge dataset.")

    st.image(f"{app_dir}/img/signals.png")
    st.write("The Azure Predictive Maintenance Challenge dataset contains continuous-valued measurements for physical characteristics \
        of the equipment such as temperature, or pressure. It also tracks indicator variables specifying when errors, failures, and maintenance occur.")

    st.image(f"{app_dir}/img/machines.png")
    st.write("Machines are labelled 1 to 100 in the data.")

    st.image(f"{app_dir}/img/components.png")
    st.write("Each Machine has five components.")

    st.write("In this project we focus on predicting failures for component 2.")


with st.expander("Predictive Models"):
    st.write("After splitting the data from the Kaggle dataset into training, validation, and testing data, the predictive models will use testing data (unseen by the models) to compare predictions to ground truth.")

with st.expander("Visualizations"):
    st.write("The visualization tab helps the user plot variables leading up to a certain time to see patterns in the failures.")

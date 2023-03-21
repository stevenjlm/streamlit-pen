import streamlit as st

st.title("Predictive Maintenance Tool")

st.write("Steven Munn, March 20th 2023")

st.write("Using the Kaggle data-set for \
[Azure Predictive Maintenance Challenge](https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance) \
        this project explores ways to model and predict failures for component 2.")

with st.expander("Problem Overview"):
    st.image("img/task.png")
    st.write("This project aims to train predictive models based on historical data from the APM challenge dataset.")

    st.image("img/signals.png")
    st.write("The Azure Predictive Maintenance Challenge dataset contains continuous-valued measurements for physical characteristics \
        of the equipment such as temperature, or pressure. It also tracks indicator variables specifying when errors, failures, and maintenance occur.")

    st.image("img/machines.png")
    st.write("Machines are labelled 1 to 100 in the data.")

    st.image("img/components.png")
    st.write("Each Machine has five components.")

    st.write("In this project we focus on predicting failures for component 2.")


with st.expander("Predictive Models"):
    st.write("See model predictions in the Day Model Predictions or Two Day Model Predictions tabs.")

with st.expander("Visualizations"):
    st.write("Inspect data before a failure in the Equipment Failure Visualizations tab.")

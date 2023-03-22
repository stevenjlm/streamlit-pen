import streamlit as st


st.title("Predictive Maintenance Web Application for Telemetry Data")

st.write("Steven Munn, March 20th 2023")

with st.expander("Introduction"):
    st.write("Cloud computing providers need to keep their machines up and running as much as possible. \
            Machines that shut down are not providing a service, so the provider's goal is keep uptime high \
            in a cost-effective manner.")

    st.write("    Predictive maintenance is a way of anticipating necessary maintenance needs without \
            performing unnecessary maintenance on healthy machines. To do this, the provider needs \
            a model for forecasting which machines in their compute center are likely to fail. The \
            [Azure Predictive Maintenance Challenge](https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance) \
            (APM) provides a data set of measurements in a cloud computing facility that can help build such a model.")

    st.write("    This web-app is a front-end for the predictive models I built based on the APM data set. \
            After splitting data into \
            training, validation, and testing datasets, the goal is to build a model to predict impending failures in the test data (data that it has never seen during learning).")
    
with st.expander("Usage"):
    st.markdown("""
    #### Background and Information
    The first three tabs on the left explain the data and model in more depth.

    #### Predictive Models
    Click on [Predictions Day Model](/Predictions_Day_Model) to see the 24-hour model in action. Or [Predictions Two Day Model](/Predictions_TWo_Day_Model) \
    for the 48-hour model.

    #### Equipment Failure Visualizations
    The [Equipment Failure Visualizations](/Equipment_Failure_Visualizations) tab presents the input data before a given time stamp.

    #### Reports
    The last tab shows all the jupyter notebooks and training reports for the ML models, as well as the github repositories for the training and front-end code.
    """)

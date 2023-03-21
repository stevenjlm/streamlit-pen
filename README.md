# streamlit-pen
Streamlit web app for the predictive maintenance tool (marching-penguins).

# Setup

This web-app uses the [Streamlit](https://streamlit.io/) package for the front-end. It calls AWS sagemaker and S3 buckets for inference and raw data respectively.

The `requirements.txt` file contains necessary python modules to run the web-app. After installing the requirements,

```
$ streamlit run home.py
```
 
will run the server which you can connect to via `http://localhost:8501/`.

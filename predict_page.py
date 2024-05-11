import streamlit as st
import pickle
import numpy as np
import pandas as pd

df = pd.read_csv("jobs_in_data.csv")


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

regressor_loaded = data["model"]
le_job_title = data["le_job_title"]
le_experience_level = data["le_experience_level"]
le_work_setting = data["le_work_setting"]
le_company_location = data["le_company_location"]

def show_predict_page():
    st.title("Data Jobs Salary Prediction")

    st.write("""### We need some information to predict the salary""")
    
    job_titles = (
        'Data Analyst',
        'Data Scientist',
        'Data Engineer',
        'Machine Learning Engineer',
        'Data Architect',
        'Analytics Engineer',
        'Applied Scientist',
        'Research Scientist',
        
    )
    experience_levels = (
        'Entry-level',
        'Mid-level',
        'Senior',
        'Executive',
    )
    work_settings = (
        'Office',
        'Hybrid',
        'Remote',
    )
    company_locations = (
        'United States',
        'United Kingdom',
        'Canada',
        'Spain',
        'Germany',
        'France',
        'Netherlands',
        'Portugal',
        'Australia',
        'Other',
    )

    job_title = st.selectbox("Job Title", job_titles)
    experience_level = st.selectbox("Experience Level", experience_levels)
    work_setting = st.selectbox("Work Type", work_settings)
    company_location = st.selectbox("Company Country", company_locations)

    if st.button("Calculate Salary"):
        x = np.array([[job_title, experience_level, work_setting, company_location]])
        x[:, 0] = le_job_title.transform(x[:, 0])
        x[:, 1] = le_experience_level.transform(x[:, 1])
        x[:, 2] = le_work_setting.transform(x[:, 2])
        x[:, 3] = le_company_location.transform(x[:, 3])
        x = x.astype(float)

        salary = regressor_loaded.predict(x)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

show_predict_page()

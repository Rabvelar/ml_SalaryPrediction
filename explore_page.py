import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Customize Matplotlib style
plt.style.use('dark_background')
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

@st.cache
def load_data():
    df = pd.read_csv("jobs_in_data.csv")

    # Check if the columns exist before attempting to drop them
    columns_to_drop = ['salary', 'salary_currency', 'job_category', 'work_year', 'company_size', 'employment_type', 'employee_residence']
    existing_columns = df.columns.tolist()
    columns_to_drop = [col for col in columns_to_drop if col in existing_columns]

    # Drop the existing columns
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Rename the 'salary_in_usd' column to 'salary'
    df.rename(columns={'salary_in_usd': 'salary'}, inplace=True)

    # Replace 'In-person' with 'Office' in the 'work_setting' column
    df['work_setting'] = df['work_setting'].replace('In-person', 'Office')

    # Shorten categories for 'job_title' and 'company_location' columns
    country_map_job_title = shorten_categories(df['job_title'].value_counts(), 150)
    df['job_title'] = df['job_title'].map(country_map_job_title)

    country_map_company_location = shorten_categories(df['company_location'].value_counts(), 20)
    df['company_location'] = df['company_location'].map(country_map_company_location)

    return df


df = load_data()

def show_explore_page(job_title=None):
    st.title("Explore Data Field Jobs Salaries")

    if job_title:
        st.write(f"### {job_title}")
        job_df = df[df["job_title"] == job_title]

        # Create a bar chart to visualize mean salary for the selected job title
        fig, ax = plt.subplots(facecolor=(0, 0, 0, 0))
        ax.hist(job_df["salary"], bins=20, edgecolor='white', alpha=0.7)
        ax.set_xlabel("Salary")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Salaries")
        st.pyplot(fig)

        # Create a pie chart to visualize the distribution of work settings for the selected job title
        fig, ax = plt.subplots(facecolor=(0, 0, 0, 0))
        ax.pie(job_df['work_setting'].value_counts(), labels=job_df['work_setting'].value_counts().index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("Distribution of Work Settings")
        st.pyplot(fig)

        # Create a count plot for company locations for the selected job title (excluding 'Other')
        fig, ax = plt.subplots(facecolor=(0, 0, 0, 0))
        sns.countplot(y="company_location", data=job_df[job_df['company_location'] != 'Other'],
                      order=job_df[job_df['company_location'] != 'Other']['company_location'].value_counts().index,
                      ax=ax, alpha=0.7)
        ax.set_xlabel("Count")
        ax.set_ylabel("Company Location")
        ax.set_title("Count of Company Locations")
        st.pyplot(fig)
    else:
        # Sort job titles by count and filter out 'Other'
        job_titles_counts = df[df['job_title'] != 'Other']['job_title'].value_counts()
        sorted_job_titles = job_titles_counts.index.tolist()

        # Create a selector for job titles
        selected_job_title = st.selectbox("Select a job title", sorted_job_titles)

        if selected_job_title:
            show_explore_page(selected_job_title)

# Call the function with your actual DataFrame
show_explore_page()

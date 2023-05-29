import pandas as pd
import streamlit as st
import altair as alt
import subprocess

# Install seaborn using pip
subprocess.check_call(["pip", "install", "seaborn"])

# Import seaborn after installation
import seaborn as sns


df = pd.read_csv('Breast_Cancer.csv')

# Define the age ranges
bins = [0, 9, 19, 29, 39, 49, 59, 69]

# Define the corresponding labels for each range
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69']

# Transform the 'Age' column into categorical ranges
df['Age'] = pd.cut(df['Age'], bins=bins, labels=labels)

def build_st_query_for_line_charts(title: str, options: list):
    feature = st.radio(f"Select {title}", options)
    return feature

def build_heatmap():
    st.subheader('Impact of demographic characteristics on the mortality of women with breast cancer in America')

    col1, col2 = st.columns(2)

    with col1:
        options_feature1 = ['Age', 'Race', 'Marital Status']
        feature1 = build_st_query_for_line_charts("First feature", options_feature1)

    with col2:
        options_feature2 = ['Age', 'Race', 'Marital Status']
        options_feature2.remove(feature1)
        feature2 = build_st_query_for_line_charts("Second feature", options_feature2)

    # Pivot the dataframe to calculate mortality rates
    pivot_df = df.pivot_table(index=f'{feature1}', columns=f'{feature2}', values='Status', aggfunc='count')

    # Calculate the mortality rates based on the "Dead" values
    mortality_rates = pivot_df.apply(lambda x: x['Dead'] / (x['Dead'] + x['Alive']), axis=1)

    # Create a heatmap using seaborn
    heatmap = sns.heatmap(pivot_df, annot=True, cmap='coolwarm')

    # Display the heatmap in Streamlit
    st.pyplot(heatmap.figure)



st.title('Visualization of information - Final Project')
build_heatmap()
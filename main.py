import pandas as pd
import streamlit as st
import altair as alt

df = pd.read_csv('Breast_Cancer.csv')

# Define the age ranges
bins = [0, 9, 19, 29, 39, 49, 59, 69]

# Define the corresponding labels for each range
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69']

# Transform the 'Age' column into categorical ranges
df['Age'] = pd.cut(df['Age'], bins=bins, labels=labels)

def build_st_query_for_line_charts(title: str, options: list):
    feature = st.Radio(f"Select {title}", options)
    return feature

def build_heatmap():
    st.subheader('Impact of demographic characteristics on the mortality of women with breast cancer in America')

    col1, col2 = st.columns(2)
    options = ['Age', 'Race', 'Marital Status']
    with col1:
        feature1 = build_st_query_for_line_charts("First feature", options)

    with col2:
        options2 = options
        options2.remove(feature1)
        feature2 = build_st_query_for_line_charts("Second feature", options2)

st.title('Visualization of information - Final Project')
build_heatmap()
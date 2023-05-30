import pandas as pd
import streamlit as st
import altair as alt
import seaborn as sns
import plotly.express as px


df = pd.read_csv('Breast_Cancer.csv')

# Define the age ranges
bins = [0, 9, 19, 29, 39, 49, 59, 69]

# Define the corresponding labels for each range
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69']

# Transform the 'Age' column into categorical ranges
df['Age'] = pd.cut(df['Age'], bins=bins, labels=labels)

def get_mortality_rate(feature_name):
    mortality_df = df.groupby(feature_name)['Status'].value_counts().unstack().fillna(0)
    mortality_df['Mortality Rate'] = mortality_df['Dead'] / (mortality_df['Dead'] + mortality_df['Alive'])
    return mortality_df

def build_st_query_for_line_charts(title: str, options: list):
    feature = st.radio(f'Select {title}', options)
    return feature

def build_heatmap():
    st.subheader('Impact of demographic characteristics on the mortality of women with breast cancer in America')

    col1 = st.columns(1)

    with col1:
        options_feature1 = ['Age', 'Race', 'Marital Status']
        feature1 = build_st_query_for_line_charts("main feature", options_feature1)

    mortality_df = get_mortality_rate(feature1)
    bar_fig = px.bar(mortality_df, x=mortality_df.index, y='Mortality Rate', title=f'{"Mortality Rate by " + feature1}')
    st.plotly_chart(bar_fig)


    col2 = st.columns(1)
    with col2:
        options_feature2 = ['Age', 'Race', 'Marital Status']
        options_feature2.remove(feature1)
        feature2 = build_st_query_for_line_charts("secondary feature", options_feature2)


    # Calculate the mortality rates based on the "Dead" values
    pivot_df = df.pivot_table(index=feature1, columns=feature2, values='Status',
                              aggfunc=lambda x: round(sum(x == 'Dead') / len(x), 2))

    # Create a heatmap using Plotly Express
    fig = px.imshow(pivot_df, text_auto=True, color_continuous_scale='reds', labels=dict(color="Mortality rate (%)"))
    fig.update_xaxes(side="top")
    fig.update_layout(height=600, width=800)
    fig.update_layout(
    yaxis=dict(title=dict(text=f"{feature1}", font=dict(size=24))),
    xaxis=dict(title=dict(text=f"{feature2}", font=dict(size=24))),
    coloraxis_colorbar=dict(title=dict(text='Mortality rate (%)', font=dict(size=22)))
)
    # Display the heatmap in Streamlit
    st.plotly_chart(fig)



st.title('Visualization final project')
build_heatmap()
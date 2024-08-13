import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    data = pd.read_csv('not_songs.csv')
    return data

data = load_data()

st.title("Hot or Not Data Visualization")

if st.checkbox('Show raw data'):
    st.write(data)

# Sidebar for selecting visualization options
st.sidebar.header('Setting')

# Select columns to visualize
columns = data.columns.tolist()[2:]
selected_column = st.sidebar.selectbox('Select column to visualize', columns)

# Plot data distribution
st.header(f'Data Distribution for {selected_column}')
plt.figure(figsize=(10, 6))
sns.histplot(data[selected_column], kde=True)
st.pyplot(plt)

# Plot data relationships
st.sidebar.header('Relationship Settings')
x_col = st.sidebar.selectbox('Select x-axis column', columns)
y_col = st.sidebar.selectbox('Select y-axis column', columns)

st.header(f'Relationship between {x_col} and {y_col}')
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x=x_col, y=y_col)
st.pyplot(plt)
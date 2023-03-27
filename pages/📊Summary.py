import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


df = pd.read_csv("Customers.csv") 

# Converting dates to datetime in pandas format
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df[~df.index.duplicated(keep='first')]

# Sidebar 
st.sidebar.header("Filters:")
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

category_type = st.sidebar.multiselect(
    "Select the Case Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique(),
)

start_date = st.sidebar.date_input("Start date", df.index.min())
end_date = st.sidebar.date_input("End date", df.index.max())

# Query from Sidebar
# df_selection = df.query(
#     "Category == @category_type & Gender == @gender").loc[start_date:end_date, :]
df_filtered = df.query("Category == @category_type & Gender == @gender")
df_selection = df_filtered[(df_filtered.index >= pd.to_datetime(start_date)) & (df_filtered.index <= pd.to_datetime(end_date))]
if df_selection.empty:
    st.warning("No data available for selected date range and filters.")

if not df_selection.empty:
    #KPIs
    average_age = round(df_selection["Age"].mean())
    total_cases = round(df_selection["Cases"].sum())
    average_sessions = round(df_selection["Sessions"].mean())
    average_satisfaction = round(df_selection["Satisfaction"].mean(),1)
    star_rating = ":star:" * int(round(average_satisfaction, 2))
else:
    st.error("Please make sure you have selected at least a gender and a case category!")

category_counts = df.groupby("Category").size()


st.markdown("<h2 style='color:green'>Summary Statistics</>",
unsafe_allow_html=True)
if not df_selection.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(""" ##### Total Cases: """, total_cases)
    with col2:
        st.write(""" ##### Average Age: """, average_age)
    with col3:
        st.write(""" ##### Average Satisfaction: """, average_satisfaction, star_rating)

# Pie Chart of Case Categories
category_counts = df_selection['Category'].value_counts()
case_categories = px.pie(category_counts, values=category_counts.values, names=category_counts.index, title='Distribution of Case Categories',color_discrete_sequence=px.colors.sequential.Aggrnyl)

## Histogram of Resolutions
# Create histogram of resolution time
resolution_histo = px.histogram(df_selection, x='Resolution Time', nbins=10, title='Distribution of Resolution Time', color='Category',color_discrete_sequence=px.colors.sequential.Aggrnyl)
resolution_histo.update_xaxes(title="Weeks")
resolution_histo.update_yaxes(title="Cases")

left_column, right_column = st.columns(2)
left_column.plotly_chart(case_categories, use_container_width=True)
right_column.plotly_chart(resolution_histo, use_container_width=True)

## Line Chart of Cases Against Time
# Group data by month
cases_by_month = df_selection.groupby(pd.Grouper(freq='M'))['Cases'].count()

cases_fig = px.line(cases_by_month, title="Number of New Cases", color_discrete_sequence=px.colors.sequential.Aggrnyl)
cases_fig.update_xaxes(title="")
cases_fig.update_yaxes(title="Number of Cases")
st.plotly_chart(cases_fig, use_container_width=True)



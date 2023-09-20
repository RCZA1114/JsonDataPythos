from columns import *
import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

#@st.cache_data


file = st.selectbox("Choose Data File", csv_files)


df = pd.read_csv(file)

df.rename(
    columns={"time": "date/time"},
    inplace =True
)

    #df["date/time"] = pd.to_datetime(df["date/time"])
    
df["date"] = df["date/time"].apply(lambda x: x.split(' ')[0])

df["time"] = df["date/time"].apply(lambda x: x.split(' ')[1])
    
df["hour"] = df["time"].apply(lambda x: x.split(':')[0])


column = st.selectbox("Select Column to Analyze", columns)
measure = st.selectbox("Select Measurement", measurement)

if measure == "Mean":
    x =df[column].mean()
    st.write(f"The Mean is {x}")
elif measure == "Standard Deviation":
    x =df[column].std()
    st.write(f"The Standard Deviation is {x}")

UCL = df[column].mean() + (3*(df[column].std()))
LCL = df[column].mean() - (3*(df[column].std()))
df["Limit"]= 0
df.loc[df[column] > UCL, 'Limit'] = 1
df.loc[df[column] < LCL, 'Limit'] = 1


st.write(f"Upper Control Limit (UCL) is {UCL}")
st.write(f"Lower Control Limit is (LCL) {LCL}")
st.write("Any value above the UCL or below the LCL is considered an outlier or 'Out of Control'.")

fig = px.scatter(df, x='date/time', y=column, title="Line Chart of the measurement for the last 24 hours")


st.plotly_chart(fig, use_container_width=True)

#filter = df[((df[column]) > UCL) or ((df[column]) < LCL)]

#for m in measurement:
#    x = measure
#    if m == x:
#        y = df[column].measurement[m]()
#        st.write(y)
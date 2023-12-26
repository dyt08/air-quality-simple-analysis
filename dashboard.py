import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta

df_new = pd.read_csv('datasets/dashboard.csv')
df_new['date'] = pd.to_datetime(df_new[['year', 'month', 'day', 'hour']])
stations = df_new['station'].unique()

# Filter data
min_date = df_new["date"].min()
max_date = df_new["date"].max()

min_year = df_new['year'].min()
max_year = df_new['year'].max()

yearly = ['No', 'month', 'day', 'hour'], ['station', 'year'], ['year', 1, 1, 0]
monthly = ['No', 'day', 'hour'], ['station', 'year', 'month'], ['year', 'month', 1, 0]
daily = ['No', 'hour'], ['station', 'year', 'month', 'day'], ['year', 'month', 'day', 0]
hourly = ['No'], ['station', 'year', 'month', 'day', 'hour'], ['year', 'month', 'day', 'hour'] 

with st.sidebar:
    st.image("assets/logo.png", width=200)
    st.title('China Air Quality Report')
    
    opt_station = st.multiselect(
        label="Select station",
        options=stations,
        default=stations
    )
    
    opt_period = st.radio(
        label="Select period",
        options=['Yearly', 'Monthly', 'Daily', 'Hourly'],
        index=1
    )
    
    if opt_period == 'Yearly':
        start_year, end_year = st.select_slider(
            label='Select a range of year',
            options=df_new['year'].unique(),
            value=(min_year, max_year)
        )
        opt_start_date = pd.to_datetime(f'{start_year}-1-1').date()
        opt_end_date = pd.to_datetime(f'{end_year}-1-1').date()
        opt_period_var = yearly
    elif opt_period == 'Monthly' or opt_period == 'Daily':
        opt_start_date, opt_end_date = st.date_input(
            label='Select a time range',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date] if opt_period == 'Monthly' else [min_date, min_date + relativedelta(months=1)]
        )
        opt_period_var = monthly  if opt_period == 'Monthly' else daily
    elif opt_period == 'Hourly':
        opt_date = st.date_input(
            label='Select Date',
            min_value=min_date,
            max_value=max_date,
            value=min_date
        )
        opt_start_date = pd.to_datetime(f'{opt_date} 00:00:00')
        opt_end_date = pd.to_datetime(f'{opt_date} 23:00:00')
        opt_period_var = hourly

# Create data
main_data = df_new.drop(opt_period_var[0], axis=1).groupby(opt_period_var[1]).mean(numeric_only=True).reset_index()
year = main_data[opt_period_var[2][0]]
month = main_data[opt_period_var[2][1]] if type(opt_period_var[2][1]) != int else opt_period_var[2][1]
day = main_data[opt_period_var[2][2]] if type(opt_period_var[2][2]) != int else opt_period_var[2][2]
hour = main_data[opt_period_var[2][3]] if type(opt_period_var[2][3]) != int else opt_period_var[2][3]
main_data['date'] = pd.to_datetime(dict(year=year, month=month, day=day, hour=hour))
df_filtered = main_data[(main_data['date'] >= np.datetime64(opt_start_date)) & (main_data['date'] <= np.datetime64(opt_end_date))]

# PM2.5
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['PM2.5'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average PM2.5 per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# PM10
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['PM10'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average PM10 per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# SO2
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['SO2'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average SO2 per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# NO2
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['NO2'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average NO2 per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# CO
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['CO'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average CO per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# O3
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['O3'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average O3 per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# TEMP
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['TEMP'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average Temperature per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

#PRES
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['PRES'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average Pressure per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# DEWP
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['DEWP'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average Dew Point Temperature per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)

# RAIN
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['RAIN'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average Precipitaion per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)


# WSPM
fig = go.Figure()

for station in opt_station:
    fig.add_trace(go.Scatter(
        x=df_filtered[df_filtered['station'] == station]['date'],
        y=df_filtered[df_filtered['station'] == station]['WSPM'], 
        mode='lines', 
        name=station 
    ))

fig.update_layout(
    title='Average Wind Speed per Month',
    showlegend=True,
    plot_bgcolor='#0F1018',
)

st.plotly_chart(fig, use_container_width=True)
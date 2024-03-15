import streamlit as st
import pandas as pd
import numpy as np

st.title('Dashboard Analitik ')

df = pd.read_csv('PRSA_Data.csv')
normal_df = pd.read_csv('PRSA_Data_Normalized.csv')

##======================================================================================##
##================================First Data Visualization==============================##
with st.container(border=True):

    station = st.selectbox(
                'Pilih Stasiun',
                [i for i in df['station'].drop_duplicates()],
                key='station')

    col1, col2 = st.columns(2)
    selection = ["Kandungan kimia dalam udara",
                "Keadaan cuaca"]

    with col1:
        select = st.radio(
                "Silahkan pilih :",
                ["Kandungan kimia dalam udara",
                "Keadaan cuaca"],
                index=None,
                )
    with col2:
        if select != None:

            if select == selection[0]:
                air_con = st.selectbox(
                            'Pilih kandungan udara :',
                            [i for i in df.columns[5:10]],
                            key='air_con')

            if select == selection[1]:
                air_con = st.selectbox(
                            'Pilih keadaan cuaca :',
                            [i for i in df.columns[10:14]],
                            key='weather_con')

    col1, col2 = st.columns(2)
    selection2 = ["Tiap bulan",
                "Tiap hari"]

    with col1:
        duration = st.radio(
                        "Silahkan pilih durasi :",
                        selection2,
                        index=None,
                        )

    with col2:
        if duration == selection2[0]:
            duration = st.radio(
                            "Silahkan pilih :",
                            ['Setiap tahun',
                            'Pada tahun tertentu'],
                            index=None,
                            )
            
    if duration == 'Setiap tahun':
        data = df[df['station'] == station].groupby(by=['year',
                                                        'month']).agg({air_con:'sum'}).reset_index()
        
        data['date'] = pd.to_datetime(data['year'].astype('str') + '-' + data['month'].astype('str'),
                                    format='%Y-%M').apply(lambda x: x.strftime('%Y-%M'))
        
        st.line_chart(data,
                    x='date',
                    y=air_con,
                    color="#0000FF")

    if duration == 'Pada tahun tertentu':
        with col2:
            year = st.selectbox(
                'Pilih Tahun',
                [i for i in range(df['year'].min(), df['year'].max()+1)]
                )
        
            data = df[df['station'] == station].groupby(by=['year',
                                                            'month']).agg({air_con:'sum'}).reset_index().query(f'year == {year}')
            
            data['date'] = pd.to_datetime(data['year'].astype('str') + '-' + data['month'].astype('str'),
                                        format='%Y-%M').apply(lambda x: x.strftime('%Y-%M'))
        
        st.line_chart(data,
                    x='date',
                    y=air_con,
                    color="#0000FF")

    if duration == selection2[1]:

        with col2:
            year = st.selectbox(
                'Pilih Tahun',
                [i for i in range(df['year'].min(), df['year'].max()+1)]
                )
            
            month = st.selectbox(
                    'Pilih Bulan',
                    [i for i in range(df['month'].min(), df['month'].max()+1)]
                    )

            data = df.query(f'year == {year}').query(f'month == {month}')

            data['date'] = pd.to_datetime(data['year'].astype('str') +\
                                        '-' +\
                                        data['month'].astype('str') +\
                                        '-' +\
                                        data['day'].astype('str'),
                                        format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m-%d'))
            
            data = data[data['station'] == station].groupby('date').agg({air_con:'sum'}).reset_index()
        
        st.line_chart(data,
                    x='date',
                    y=air_con,
                    color="#0000FF")


##======================================================================================##
##================================Second Data Visualization=============================##
with st.container(border=True):

    station = st.selectbox(
                'Pilih Stasiun',
                [i for i in df['station'].drop_duplicates()],
                key='station2')

    col1, col2 = st.columns(2)

    with col1:
        air_con = st.selectbox(
                            'Pilih kandungan udara :',
                            [i for i in df.columns[5:10]],
                            key='air_con2')
    
    with col2:
        weather_con = st.selectbox(
                            'Pilih keadaan cuaca :',
                            [i for i in df.columns[10:14]],
                            key='weather_con2')
    
    air_weather = [air_con, weather_con]
    aggregate = ['sum'] * 2

    normal_data = normal_df[normal_df['station'] == station].groupby(by=['year',
                                                                       'month']).agg(dict(zip(air_weather,
                                                                                              aggregate))).reset_index()
        
    normal_data['date'] = pd.to_datetime(normal_data['year'].astype('str') + '-' + normal_data['month'].astype('str'),
            format='%Y-%M').apply(lambda x: x.strftime('%Y-%M'))
    
    normal_data = normal_data[air_weather + ['date']]

    st.line_chart(normal_data,
                    x='date',
                    y=air_weather,
                    color=["#0000FF", "#008000"])
    
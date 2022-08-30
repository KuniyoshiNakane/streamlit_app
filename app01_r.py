import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

data_url_newly_confirmed = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
data_url_severe_cases = 'https://covid19.mhlw.go.jp/public/opendata/severe_cases_daily.csv'

st.title('新型コロナ関連ダッシュボード（ガジェット研究会）')
st.caption('新型コロナ関連データです')

col1, col2 = st.columns(2)

df_nc = pd.read_csv(data_url_newly_confirmed)
df_nc['Datetime'] = pd.to_datetime(df_nc['Date'])
df_nc_tochigi = df_nc[['Datetime', 'Tochigi', 'ALL']].copy()

df_sc = pd.read_csv(data_url_severe_cases)
df_sc['Datetime'] = pd.to_datetime(df_sc['Date'])
df_sc_tochigi = df_sc[['Datetime', 'Tochigi', 'ALL']].copy()

with col1:
    st.text('新規感染者')
    AgGrid(df_nc_tochigi,theme="blue")

    st.text('重症者')
    AgGrid(df_sc_tochigi,theme="blue")

with col2:

    #新規感染者
    fig = plt.figure(figsize=(12,5))

    ax1 = fig.add_subplot(1, 2, 1)
    plt.xticks(rotation=45)
    ax2 = fig.add_subplot(1, 2, 2)
    plt.xticks(rotation=45)

    ax1.bar(df_nc['Datetime'], df_nc['Tochigi'])
    ax1.set_title('新規感染者　栃木')

    ax2.bar(df_nc['Datetime'], df_nc['ALL'])
    ax2.set_title('新規感染者　全国')

    st.pyplot(fig)

    #重症者
    fig = plt.figure(figsize=(12,5))

    ax1 = fig.add_subplot(1, 2, 1)
    plt.xticks(rotation=45)
    ax2 = fig.add_subplot(1, 2, 2)
    plt.xticks(rotation=45)

    ax1.bar(df_sc['Datetime'], df_sc['Tochigi'])
    ax1.set_title('重症者　栃木')

    ax2.bar(df_sc['Datetime'], df_sc['ALL'])
    ax2.set_title('重症者　全国')

    st.pyplot(fig)

    

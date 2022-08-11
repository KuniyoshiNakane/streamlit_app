import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

data_url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'

st.title('ガジェット研究会　新型コロナ関連ダッシュボード')
st.caption('新型コロナに関連したデータです')

st.text('新規感染者データ')

col1, col2 = st.columns(2)

df = pd.read_csv(data_url)
df['Datetime'] = pd.to_datetime(df['Date'])
df_tochigi = df[['Datetime', 'Tochigi', 'ALL']].copy()

with col1:
    AgGrid(df_tochigi,theme="blue",fit_columns_on_grid_load=True)

with col2:

    #matplotlib
    fig = plt.figure(figsize=(12,6))

    ax1 = fig.add_subplot(1, 2, 1)
    plt.xticks(rotation=45)
    ax2 = fig.add_subplot(1, 2, 2)
    plt.xticks(rotation=45)

    ax1.plot(df['Datetime'], df['Tochigi'])
    ax1.set_title('Tochigi')

    ax2.plot(df['Datetime'], df['ALL'])
    ax2.set_title('ALL')

    st.pyplot(fig)

    

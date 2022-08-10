import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data_url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'

st.title('Sample App')
st.caption('Streamlit 開発練習用アプリです')

st.text('サンプル')

with st.form(key='input_form'):
    password = st.text_input('パスワード')
    btn_ok = st.form_submit_button('送信')

    if btn_ok & (password == 'poppy'):
        df = pd.read_csv(data_url)
        df['Date'] = pd.to_datetime(df['Date'])
        df_tochigi = df[['Date', 'Tochigi']]
        st.dataframe(df_tochigi)
        st.line_chart(df_tochigi)

        #matplotlib
        fig, ax = plt.subplots()
        plt.xticks(rotation=45)
        ax.plot(df['Date'], df['Tochigi'])
        ax.set_title('Tochigi')
        st.pyplot(fig)




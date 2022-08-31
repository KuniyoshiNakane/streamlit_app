import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import altair as alt

st.set_page_config(layout="wide")

data_url_newly_confirmed = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
data_url_severe_cases = 'https://covid19.mhlw.go.jp/public/opendata/severe_cases_daily.csv'
data_url_pcr_tested = 'https://www.mhlw.go.jp/content/pcr_tested_daily.csv'

st.title('新型コロナ関連ダッシュボード By ガジェット研究会')
st.caption('新型コロナ関連のデータです')

col1, col2 = st.columns(2)

df_nc = pd.read_csv(data_url_newly_confirmed)
df_nc['Date'] = pd.to_datetime(df_nc['Date'])
df_nc_tochigi = df_nc[['Date', 'Tochigi', 'ALL']]

df_sc = pd.read_csv(data_url_severe_cases)
df_sc['Date'] = pd.to_datetime(df_sc['Date'])
df_sc_tochigi = df_sc[['Date', 'Tochigi', 'ALL']].rename(columns={'Tochigi': '重症者_Tochigi', 'ALL': '重症者_ALL'})

df_pcr = pd.read_csv(data_url_pcr_tested)
df_pcr['日付'] = pd.to_datetime(df_pcr['日付'])
df_pcr['PCR 検査実施人数(単日)'] = df_pcr['PCR 検査実施人数(単日)'].fillna(0).astype(np.int64)

df_nc_pcr = pd.merge(df_pcr, df_nc_tochigi, how='outer', left_on='日付', right_on='Date')
df_nc_pcr['日付'].fillna(df_nc_pcr['Date'], inplace=True)

df_nc_sc_all = pd.merge(df_nc_tochigi[['Date', 'ALL']], df_sc_tochigi[['Date', '重症者_ALL']], how='outer', left_on='Date', right_on='Date')
df_nc_sc_all['重症者_ALL'].fillna(0, inplace=True)

df_nc_sc_tochigi = pd.merge(df_nc_tochigi[['Date', 'Tochigi']], df_sc_tochigi[['Date', '重症者_Tochigi']], how='outer', left_on='Date', right_on='Date')
df_nc_sc_tochigi['重症者_Tochigi'].fillna(0, inplace=True)

with col1:
    st.text('新規陽性者')
    AgGrid(df_nc_tochigi, theme='blue')

    st.text('重症者')
    AgGrid(df_sc_tochigi, theme='blue')

    st.text('PCR検査実施人数')
    AgGrid(df_pcr, theme='blue')



with col2:

    #新規陽性者とPCR実施人数
    mdf_nc = pd.melt(df_nc_pcr.drop(['Date', 'Tochigi'], axis=1).rename(columns={'ALL': '新規陽性者（全国）', 'PCR 検査実施人数(単日)': 'PCR検査実施人数（全国）'}), id_vars=['日付'],var_name="区分",value_name="人数" )
    selection = alt.selection_multi(fields=['区分'], bind='legend')
    chart = alt.Chart(mdf_nc, height=450).mark_line().encode( x="日付:T", y="人数", color="区分", opacity=alt.condition(selection, alt.value(1), alt.value(0.1)) ).add_selection( selection)

    # ホバー時にマーカーを表示
    hover = alt.selection_single( fields=["日付"], nearest=True, on="mouseover", empty="none")
    chart_temp = (alt.Chart(mdf_nc) .encode( x="日付:T", y="人数", color="区分"))
    points = chart_temp.transform_filter(hover).mark_circle(size=32)
    # ホバー時にツールチップを表示
    tooltips = ( alt.Chart(mdf_nc) .mark_rule() .encode( x="日付:T", y="人数", opacity=alt.condition(hover, alt.value(0.1), alt.value(0)), tooltip=[ alt.Tooltip("日付:T", title="日付"), alt.Tooltip("人数", title="人数"), alt.Tooltip("区分", title="区分")]) .add_selection(hover))
    
    st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)

    #新規陽性者と重症者
    #栃木
    mdf_nc_sc_tochigi = pd.melt(df_nc_sc_tochigi.rename(columns={'Date':'日付', 'Tochigi': '新規陽性者（栃木）', '重症者_Tochigi': '重症者（栃木）'}), id_vars=['日付'],var_name="区分",value_name="人数" )
    selection = alt.selection_multi(fields=['区分'], bind='legend')
    chart = alt.Chart(mdf_nc_sc_tochigi, height=450).mark_line().encode( x="日付:T", y="人数", color="区分", opacity=alt.condition(selection, alt.value(1), alt.value(0.1)) ).add_selection( selection)

    # ホバー時にマーカーを表示
    hover = alt.selection_single( fields=["日付"], nearest=True, on="mouseover", empty="none")
    chart_temp = (alt.Chart(mdf_nc_sc_tochigi) .encode( x="日付:T", y="人数", color="区分"))
    points = chart_temp.transform_filter(hover).mark_circle(size=32)
    # ホバー時にツールチップを表示
    tooltips = ( alt.Chart(mdf_nc_sc_tochigi) .mark_rule() .encode( x="日付:T", y="人数", opacity=alt.condition(hover, alt.value(0.1), alt.value(0)), tooltip=[ alt.Tooltip("日付:T", title="日付"), alt.Tooltip("人数", title="人数"), alt.Tooltip("区分", title="区分")]) .add_selection(hover))
    
    st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)

    #全国
    mdf_nc_sc_all = pd.melt(df_nc_sc_all.rename(columns={'Date':'日付', 'ALL': '新規陽性者（全国）', '重症者_ALL': '重症者（全国）'}), id_vars=['日付'],var_name="区分",value_name="人数" )
    selection = alt.selection_multi(fields=['区分'], bind='legend')
    chart = alt.Chart(mdf_nc_sc_all, height=450).mark_line().encode( x="日付:T", y="人数", color="区分", opacity=alt.condition(selection, alt.value(1), alt.value(0.1)) ).add_selection( selection)

    # ホバー時にマーカーを表示
    hover = alt.selection_single( fields=["日付"], nearest=True, on="mouseover", empty="none")
    chart_temp = (alt.Chart(mdf_nc_sc_all) .encode( x="日付:T", y="人数", color="区分"))
    points = chart_temp.transform_filter(hover).mark_circle(size=32)
    # ホバー時にツールチップを表示
    tooltips = ( alt.Chart(mdf_nc_sc_all) .mark_rule() .encode( x="日付:T", y="人数", opacity=alt.condition(hover, alt.value(0.1), alt.value(0)), tooltip=[ alt.Tooltip("日付:T", title="日付"), alt.Tooltip("人数", title="人数"), alt.Tooltip("区分", title="区分")]) .add_selection(hover))
    
    st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)

    

    

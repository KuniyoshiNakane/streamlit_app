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
areaname = df_nc.columns.values.tolist()
areaname.remove('Date')
areaname.remove('ALL')

df_sc = pd.read_csv(data_url_severe_cases)
df_sc['Date'] = pd.to_datetime(df_sc['Date'])
df_sc.columns = ['Date', 'ALL(重症者)'] + [f'{area}(重症者)' for area in areaname]

df_pcr = pd.read_csv(data_url_pcr_tested)
df_pcr['日付'] = pd.to_datetime(df_pcr['日付'])
df_pcr['PCR 検査実施人数(単日)'] = df_pcr['PCR 検査実施人数(単日)'].fillna(0).astype(np.int64)

df_nc_pcr = pd.merge(df_pcr, df_nc[['Date', 'ALL']], how='outer', left_on='日付', right_on='Date')
df_nc_pcr['日付'].fillna(df_nc_pcr['Date'], inplace=True)
df_nc_pcr.drop(columns='Date', inplace=True)

df_nc_sc_all = pd.merge(df_nc[['Date', 'ALL']], df_sc[['Date', 'ALL(重症者)']], how='outer', left_on='Date', right_on='Date')
df_nc_sc_all['ALL(重症者)'].fillna(0, inplace=True)


with col1:
    areas = st.multiselect('エリアを選んでください', areaname, ['Tochigi'])

    st.text('新規陽性者')
    df_nc_areas = df_nc[['Date', 'ALL'] + areas]
    AgGrid(df_nc_areas, theme='blue')

    st.text('重症者')
    df_sc_areas = df_sc[['Date', 'ALL(重症者)'] + [f'{area}(重症者)' for area in areas]]
    AgGrid(df_sc_areas, theme='blue')

    st.text('PCR検査実施人数')
    AgGrid(df_pcr, theme='blue')



with col2:
    st.info('新規陽性者と重症者(選択Area)')
    df_nc_sc_areas = pd.merge(df_nc_areas, df_sc_areas, how='outer', left_on='Date', right_on='Date')
    df_nc_sc_areas.drop(columns=['ALL','ALL(重症者)'], inplace=True)
    df_nc_sc_areas[[f'{area}(重症者)' for area in areas]].fillna(0, inplace=True)
    mdf_nc_sc_areas = pd.melt(df_nc_sc_areas, id_vars=['Date'],var_name="区分",value_name="人数" )
    selection = alt.selection_multi(fields=['区分'], bind='legend')
    chart = alt.Chart(mdf_nc_sc_areas, height=450).mark_line().encode( x="Date:T", y="人数", color="区分", opacity=alt.condition(selection, alt.value(1), alt.value(0.1)) ).add_selection( selection)

    # ホバー時にマーカーを表示
    hover = alt.selection_single( fields=["Date"], nearest=True, on="mouseover", empty="none")
    chart_temp = (alt.Chart(mdf_nc_sc_areas) .encode( x="Date:T", y="人数", color="区分"))
    points = chart_temp.transform_filter(hover).mark_circle(size=32)
    # ホバー時にツールチップを表示
    tooltips = ( alt.Chart(mdf_nc_sc_areas) .mark_rule() .encode( x="Date:T", y="人数", opacity=alt.condition(hover, alt.value(0.1), alt.value(0)), tooltip=[ alt.Tooltip("Date:T", title="日付"), alt.Tooltip("人数", title="人数"), alt.Tooltip("区分", title="区分")]) .add_selection(hover))
    
    st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)


    st.info('新規陽性者と重症者(全国)')
    mdf_nc_sc_all = pd.melt(df_nc_sc_all.rename(columns={'ALL': 'ALL(新規陽性者）', '重症者_ALL': 'ALL(重症者）'}), id_vars=['Date'],var_name="区分",value_name="人数" )
    selection = alt.selection_multi(fields=['区分'], bind='legend')
    chart = alt.Chart(mdf_nc_sc_all, height=450).mark_line().encode( x="Date:T", y="人数", color="区分", opacity=alt.condition(selection, alt.value(1), alt.value(0.1)) ).add_selection( selection)

    # ホバー時にマーカーを表示
    hover = alt.selection_single( fields=["Date"], nearest=True, on="mouseover", empty="none")
    chart_temp = (alt.Chart(mdf_nc_sc_all) .encode( x="Date:T", y="人数", color="区分"))
    points = chart_temp.transform_filter(hover).mark_circle(size=32)
    # ホバー時にツールチップを表示
    tooltips = ( alt.Chart(mdf_nc_sc_all) .mark_rule() .encode( x="Date:T", y="人数", opacity=alt.condition(hover, alt.value(0.1), alt.value(0)), tooltip=[ alt.Tooltip("Date:T", title="日付"), alt.Tooltip("人数", title="人数"), alt.Tooltip("区分", title="区分")]) .add_selection(hover))
    
    st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)


    st.info('新規陽性者とPCR実施人数')
    mdf_nc = pd.melt(df_nc_pcr.rename(columns={'ALL': 'ALL(新規陽性者)', 'PCR 検査実施人数(単日)': 'ALL(PCR検査実施人数）'}), id_vars=['日付'],var_name="区分",value_name="人数" )
    selection = alt.selection_multi(fields=['区分'], bind='legend')
    chart = alt.Chart(mdf_nc, height=450).mark_line().encode( x="日付:T", y="人数", color="区分", opacity=alt.condition(selection, alt.value(1), alt.value(0.1)) ).add_selection( selection)

    # ホバー時にマーカーを表示
    hover = alt.selection_single( fields=["日付"], nearest=True, on="mouseover", empty="none")
    chart_temp = (alt.Chart(mdf_nc) .encode( x="日付:T", y="人数", color="区分"))
    points = chart_temp.transform_filter(hover).mark_circle(size=32)
    # ホバー時にツールチップを表示
    tooltips = ( alt.Chart(mdf_nc) .mark_rule() .encode( x="日付:T", y="人数", opacity=alt.condition(hover, alt.value(0.1), alt.value(0)), tooltip=[ alt.Tooltip("日付:T", title="日付"), alt.Tooltip("人数", title="人数"), alt.Tooltip("区分", title="区分")]) .add_selection(hover))
    
    st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)


    

    

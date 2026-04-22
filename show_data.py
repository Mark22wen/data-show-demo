import streamlit as st
import pandas as pd
st.set_page_config(page_title="数据展示平台",layout="wide")
st.title("数据展示平台")
st.divider()
excel_file = pd.ExcelFile("基础数据汇总4.21.xlsx")
sheet_names = excel_file.sheet_names
selected_sheet = st.selectbox("选择要查看的工作表", sheet_names)
df = pd.read_excel(excel_file, sheet_name=selected_sheet)
col1,col2=st.columns(2)
with col1:
    st.info(f"当前工作表：{selected_sheet}")
with col2:
    st.info(f" 数据条数：{df.shape[0]} 条 | 字段数：{df.shape[1]} 项")
st.divider()
st.subheader("数据库总览")
st.dataframe(df,use_container_width=True,hide_index=True)
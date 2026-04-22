import streamlit as st
import pandas as pd
import altair as alt
st.set_page_config(page_title="数据展示平台",layout="wide")
# 放在 st.set_page_config 之后
hide_streamlit_style = """
<style>
/* 隐藏右上角菜单 */
#MainMenu {visibility: hidden !important;}
/* 隐藏页脚 */
footer {visibility: hidden !important;}
/* 隐藏顶部 header */
header {visibility: hidden !important;}
/* 隐藏悬浮工具栏 */
div[data-testid="stToolbar"] {
    visibility: hidden !important;
    height: 0px !important;
}
/* 隐藏滚动条（可选，让界面更干净） */
::-webkit-scrollbar {
    display: none;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
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
st.divider()
st.subheader("自适应可视化")
if"年份"in df.columns:
    time_col="年份"
elif"时间" in df.columns:
    time_col="时间"
else:
    time_col=None
    st.warning("数据中未找到'年份'或'时间'列，图表功能受限")
area_col="地区"if "地区"in df.columns else None
metric_cols = [col for col in df.columns if col not in [time_col, area_col] and pd.api.types.is_numeric_dtype(df[col])]
if not metric_cols:
    st.error("当前工作表无可用数值指标，无法生成图表")
    st.stop()
if area_col and time_col:
    st.markdown("多地区趋势对比")
    selected_areas = st.multiselect("选择地区（可多选）", df[area_col].unique(), default=df[area_col].unique()[:3])
    choose_col = st.selectbox("选择要分析的指标", metric_cols)
    filtered_df = df[df[area_col].isin(selected_areas)]
    line_chart=alt.Chart(filtered_df).mark_line(point=True,color='#1f77b4').encode(x=alt.X(time_col, title=time_col,type="ordinal"),y=alt.Y(choose_col,title=choose_col),color=alt.Color(area_col,legend=alt.Legend(title=area_col)),tooltip=[time_col,area_col,choose_col]).properties(title=f"不同地区{choose_col}随{time_col}变化趋势",height=400)
    st.altair_chart(line_chart,use_container_width=True)
elif time_col and not area_col:
    st.markdown("全国历年趋势分析")
    choose_col=st.selectbox("选择要分析的指标", metric_cols)
    line_chart=alt.Chart(df).mark_line(point=True,color='#1f77b4').encode(x=alt.X(time_col, title=time_col,type="ordinal"),y=alt.Y(choose_col,title=choose_col)).properties(title=f"全国{choose_col}历年变化趋势",height=350)
    st.altair_chart(line_chart,use_container_width=True)
    bar_chart=alt.Chart(df).mark_bar(color='#ff7f0e').encode(x=alt.X(time_col, title=time_col,type="ordinal"),y=alt.Y(choose_col, title=choose_col)).properties(title=f"全国{choose_col}年度分布",height=350)
    st.altair_chart(bar_chart,use_container_width=True)
else:
    st.info("当前工作表无适配的可视化方式")

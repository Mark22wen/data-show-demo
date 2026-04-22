import streamlit as st
import pandas as pd
import altair as alt
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
st.divider()
st.subheader("自主选择指标生成趋势图")
if"年份"in df.columns:
    x_axis_col = "年份"
elif"时间"in df.columns:
    x_axis_col = "时间"
else：
    x_axis_col=df.columns[0]
    st.warning("数据中未找到'年份'或'时间'列，将默认用【{x_axis_col}】作为x轴")
col_list=[col for col in df.columns if col !=x_axis_col]
if not col_list:
    st.error("当前工作表除了X轴列外，没有其他指标列可以用于可视化！")
    st.stop()
choose_col=st.selectbox("请选择需要可视化的指标",col_list)
st.markdown("折线图")
try：
    line_chart=alt.Chart(df).mark_line(point=True,color='#1f77b4').encode(x=alt.X(x_axis_col, title=x_axis_col),y=alt.Y(choose_col,title=choose_col)).properties(title=f"{choose_col}随{x_axis_col}变化趋势",height=350)
    st.altair_chart(line_chart,use_container_width=True)
except Exception as e:
    st.error(f"折线图绘制失败：{e}")
st.markdown("分布柱状图")
try:
    bar_chart=alt.Chart(df).mark_bar(color='#ff7f0e').encode(x=alt.X(x_axis_col, title=x_axis_col),y=alt.Y(choose_col, title=choose_col)).properties(title=f"{choose_col}按{x_axis_col}分布",height=350)
    st.altair_chart(bar_chart,use_container_width=True)
except Exception as e:
    st.error(f"柱状图绘制失败：{e}")

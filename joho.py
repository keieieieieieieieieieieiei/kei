import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["日付", "カテゴリ", "金額"])
if "budget" not in st.session_state:
    st.session_state.budget = 0  

st.title("家計簿アプリ")

st.header("今月の予算設定")
budget = st.number_input("予算を入力してください（円）", min_value=0, value=st.session_state.budget)
if st.button("予算を設定"):
    st.session_state.budget = budget
    st.success(f"予算を {budget:,} 円に設定しました！")

with st.form("entry_form"):
    date = st.date_input("日付を入力してください")
    category = st.selectbox('カテゴリ', ['食費', '交通費', '娯楽',"外食","生活雑費","ガソリン代","家賃","光熱費","電気代","水道代", "部費","その他"])
    amount = st.number_input("金額を入力してください", min_value=0)
    submitted = st.form_submit_button("追加")

    if submitted:
        new_entry = pd.DataFrame({"日付": [date], "カテゴリ": [category], "金額": [amount]})
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
        st.success("データが追加されました！")

st.subheader("入力データ")
st.dataframe(st.session_state.data)

current_month = datetime.now().strftime("%Y-%m")

if not st.session_state.data.empty:
    st.session_state.data["月"] = pd.to_datetime(st.session_state.data["日付"]).dt.to_period("M")
    this_month_data = st.session_state.data[st.session_state.data["月"] == current_month]
    total_spent = this_month_data["金額"].sum()
    remaining_budget = st.session_state.budget - total_spent

    if st.session_state.budget > 0:remaining_percentage = remaining_budget / st.session_state.budget
    else:remaining_percentage = 0

    st.subheader("今月の予算と残金")
    st.metric("今月の予算", f"{st.session_state.budget:,} 円")
    st.metric("今月の出費合計", f"{total_spent:,} 円")
    st.metric("残金", f"{remaining_budget:,} 円", delta=-total_spent)
    
    if remaining_percentage >= 0.5:
        st.success("ご利用は計画的に")
    elif remaining_percentage >= 0.3:
         st.success("無駄遣いを避けよう")
    elif remaining_percentage >= 0.1:
         st.warning("使い方を慎重に")
    elif remaining_percentage > 0:
        st.warning("予算が尽きそうです、支出を最小限に！")
    else:
       st.error("グットラック")

    st.subheader("日付ごとの金額（折れ線グラフ）")
    daily_summary = st.session_state.data.groupby("日付", as_index=False)["金額"].sum()
    line_chart = (alt.Chart(daily_summary).mark_line(point=True).encode(x=alt.X("yearmonthdate(日付):T", 
    title="日付", axis=alt.Axis(format="%Y-%m-%d")),y="金額:Q",tooltip=["日付:T", "金額:Q"]))
    st.altair_chart(line_chart, use_container_width=True)
    
    st.subheader("１ヶ月のカテゴリ別金額（円グラフ）")
    if not this_month_data.empty:
        category_summary = this_month_data.groupby("カテゴリ", as_index=False)["金額"].sum()
        pie_chart = (alt.Chart(category_summary).mark_arc().encode(theta="金額:Q",color="カテゴリ:N",tooltip=["カテゴリ", "金額"])) 
        st.altair_chart(pie_chart, use_container_width=True)
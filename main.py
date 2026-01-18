import streamlit as st
import pandas as pd
from models import Transaction
from data_manager import DataManager

# ページ設定
st.set_page_config(page_title="家計簿アプリ", layout="wide")
manager = DataManager()

# タイトル
st.title("高専家計簿")

# サイドバー：入力フォーム
st.sidebar.header("支出の追加")
with st.sidebar.form("entry_form"):
  date_input = st.date_input("日付")
  category = st.selectbox(
      "カテゴリ",
      ["食費", "交通費", "趣味", "光熱費", "その他"]
  )
  item = st.text_input("内容")
  amount = st.number_input("金額（円）", min_value=0, step=100)
  submitted = st.form_submit_button("追加")

  if submitted:
    if item and amount > 0:
      new_trans = Transaction(date_input, category, item, amount)
      manager.add_transaction(new_trans)
      st.success("追加しました！")
    else:
      st.error("内容と金額を入力してください。")

# メイン画面
st.header("ダッシュボード")
df = manager.load_data()

if not df.empty:
  df["date"] = pd.to_datetime(df["date"])

  col1, col2 = st.columns(2)

  with col1:
    st.subheader("最近の支出")
    st.dataframe(
        df.sort_values("date", ascending=False).head(10),
        use_container_width=True
    )

  with col2:
    st.subheader("カテゴリ別支出")
    st.bar_chart(df.groupby("category")["amount"].sum())

  st.subheader("合計支出")
  st.metric("合計金額", f"¥{df['amount'].sum():,}")
else:
  st.info("まだデータがありません。左側から追加してください。")

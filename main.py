import streamlit as st
import pandas as pd
from models import Transaction
from data_manager import DataManager

# ページ設定
st.set_page_config(page_title="家計簿アプリ", layout="wide")
manager = DataManager()

# タイトル
st.title("高専家計簿")

# =========================
# サイドバー：支出追加
# =========================
st.sidebar.header("支出の追加")
with st.sidebar.form("entry_form"):
  date_input = st.date_input("日付")
  category = st.selectbox(
      "カテゴリ",
      ["食費", "交通費", "趣味", "日用品", "その他"]
  )
  item = st.text_input("内容")
  amount = st.number_input("金額（円）", min_value=0, step=100)
  submitted = st.form_submit_button("追加")

  if submitted:
    if item and amount > 0:
      new_trans = Transaction(date_input, category, item, amount)
      manager.add_transaction(new_trans)
      st.success("追加しました！")
      st.experimental_rerun()
    else:
      st.error("内容と金額を入力してください。")

# =========================
# メイン画面
# =========================
st.header("ダッシュボード")
df = manager.load_data()

if not df.empty:
  df["date"] = pd.to_datetime(df["date"])

  # ---- 上段：履歴とグラフ ----
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

  # =========================
  # 一覧（削除）
  # =========================
  st.divider()
  st.subheader("支出一覧（削除）")

  for idx, row in df.iterrows():
    c1, c2, c3, c4, c5 = st.columns([2, 2, 3, 2, 1])

    c1.write(row["date"].date())
    c2.write(row["category"])
    c3.write(row["item"])
    c4.write(f"¥{row['amount']:,}")

    if c5.button("削除", key=f"delete_{idx}"):
      manager.delete_transaction(idx)
      st.experimental_rerun()

  # =========================
  # 修正（編集）
  # =========================
  st.divider()
  st.subheader("支出の修正")

  edit_index = st.selectbox(
      "修正するデータを選択",
      df.index,
      format_func=lambda i: f"{df.loc[i, 'date'].date()} | {df.loc[i, 'item']} | ¥{df.loc[i, 'amount']:,}"
  )

  edit_row = df.loc[edit_index]

  with st.form("edit_form"):
    edit_date = st.date_input(
        "日付",
        value=edit_row["date"]
    )
    edit_category = st.selectbox(
        "カテゴリ",
        ["食費", "交通費", "趣味", "日用品", "その他"],
        index=["食費", "交通費", "趣味", "日用品", "その他"].index(edit_row["category"])
    )
    edit_item = st.text_input("内容", value=edit_row["item"])
    edit_amount = st.number_input(
        "金額（円）",
        min_value=0,
        value=int(edit_row["amount"]),
        step=100
    )

    updated = st.form_submit_button("更新")

    if updated:
      updated_trans = Transaction(
          edit_date,
          edit_category,
          edit_item,
          edit_amount
      )
      manager.update_transaction(edit_index, updated_trans)
      st.success("更新しました！")
      st.experimental_rerun()

else:
  st.info("まだデータがありません。左側から追加してください。")

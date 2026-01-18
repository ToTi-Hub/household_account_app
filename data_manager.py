import pandas as pd
import os

class DataManager:
  def __init__(self, file_path="data.csv"):
    self.file_path = file_path

    # ファイルが存在しない場合は空のCSVを作成
    if not os.path.exists(self.file_path):
      df = pd.DataFrame(columns=["date", "category", "item", "amount"])
      df.to_csv(self.file_path, index=False)

  def load_data(self):
    return pd.read_csv(self.file_path)

  def add_transaction(self, transaction):
    df = self.load_data()
    new_row = {
        "date": transaction.date,
        "category": transaction.category,
        "item": transaction.item,
        "amount": transaction.amount
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(self.file_path, index=False)

  # =====================
  # 追加：削除機能
  # =====================
  def delete_transaction(self, index):
    df = self.load_data()
    df = df.drop(index)
    df.to_csv(self.file_path, index=False)

  # =====================
  # 追加：更新機能
  # =====================
  def update_transaction(self, index, transaction):
    df = self.load_data()
    df.loc[index] = [
        transaction.date,
        transaction.category,
        transaction.item,
        transaction.amount
    ]
    df.to_csv(self.file_path, index=False)

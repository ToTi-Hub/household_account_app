import pandas as pd
import os
from models import Transaction

class DataManager:
  """データの保存と読み込みを担当するクラス"""

  def __init__(self, file_path="data.csv"):
    self.file_path = file_path
    if not os.path.exists(self.file_path):
      df = pd.DataFrame(columns=["date", "category", "item", "amount"])
      df.to_csv(self.file_path, index=False)

  def load_data(self):
    return pd.read_csv(self.file_path)

  def add_transaction(self, transaction: Transaction):
    df = self.load_data()
    new_row = pd.DataFrame([transaction.to_dict()])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(self.file_path, index=False)

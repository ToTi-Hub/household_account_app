import datetime

class Transaction:
  """家計簿の1件の取引データを表すクラス"""

  def __init__(self, date: datetime.date, category: str, item: str, amount: int):
    self.date = date
    self.category = category
    self.item = item
    self.amount = amount

  def to_dict(self):
    """データフレーム用に辞書型に変換"""
    return {
        "date": self.date,
        "category": self.category,
        "item": self.item,
        "amount": self.amount
    }

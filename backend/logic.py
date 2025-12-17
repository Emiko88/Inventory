import pandas as pd
from pathlib import Path
from typing import List, Dict


class InventoryService:
    def __init__(self):
        self.df = pd.DataFrame()
        self.load_data()

    def load_data(self):
        try:
            base_path = Path(__file__).parent
            file_path = base_path / "data" / "inventory.xlsx"

            self.df = pd.read_excel(file_path, dtype=str).fillna("")

            self.df.columns = self.df.columns.str.strip().str.lower()
            print(f"Успешно загружено {len(self.df)} записей.")

        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.df = pd.DataFrame()

    def _calculate_score(self, row, query: str) -> float:
        """Внутренняя функция подсчета рейтинга"""
        material = str(row.get('material', '')).lower().strip()
        part_number = str(row.get('part_number', '')).lower().strip()
        description = str(row.get('description', '')).lower()
        full_row_text = " ".join(row.values.astype(str)).lower()

        if query == material or query == part_number:
            return 1.0
        elif f" {query} " in f" {description} ":
            return 0.8
        elif query in full_row_text:
            return 0.5
        return 0.0

    def search(self, query: str) -> List[Dict]:
        if not query or self.df.empty:
            return []

        q = query.lower().strip()
        df_result = self.df.copy()

        df_result['score'] = df_result.apply(lambda row: self._calculate_score(row, q), axis=1)

        df_result = df_result[df_result['score'] > 0]
        df_result = df_result.sort_values(by='score', ascending=False)

        return df_result.to_dict(orient='records')

inventory_service = InventoryService()
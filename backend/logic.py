import pandas as pd
from pathlib import Path
from typing import List, Dict
import re


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

            self.df['search_index'] = self.df.astype(str).agg(' '.join, axis=1).str.lower()

            print(f"--- ДАННЫЕ ЗАГРУЖЕНЫ: {len(self.df)} строк ---")

        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.df = pd.DataFrame()

    def _calculate_row_score(self, row, query_tokens: List[str]) -> float:
        """
        Проверяет Description (по сегментам) и остальные поля.
        """
        total_score = 0.0
        matches_count = 0

        desc_raw = str(row.get('description', ''))
        desc_segments = [s.strip().lower() for s in desc_raw.split(',') if s.strip()]

        other_values = []
        for col in self.df.columns:
            if col not in ['description', 'search_index', 'score']:
                val = str(row[col]).strip().lower()
                if val and val != 'nan':
                    other_values.append(val)

        for token in query_tokens:
            best_token_score = 0.0
            esc_token = re.escape(token)

            for segment in desc_segments:
                if segment == token:
                    best_token_score = max(best_token_score, 2.0)

                elif re.search(r'\b' + esc_token + r'\b', segment):
                    best_token_score = max(best_token_score, 1.0)

                elif token in segment:
                    best_token_score = max(best_token_score, 0.5)


            for val in other_values:
                if val == token:
                    best_token_score = max(best_token_score, 2.0)
                elif re.search(r'\b' + esc_token + r'\b', val):
                    best_token_score = max(best_token_score, 1.0)
                elif token in val:
                    best_token_score = max(best_token_score, 0.5)

            if best_token_score > 0:
                total_score += best_token_score
                matches_count += 1

        #Если искали 2 слова, а нашли только 1 -> скрываем
        if matches_count < len(query_tokens):
            return 0.0

        return total_score

    def search(self, query: str) -> List[Dict]:
        if not query or self.df.empty:
            return []

        clean_query = query.lower().strip()
        tokens = clean_query.split()

        if not tokens:
            return []

        df_result = self.df.copy()

        df_result['score'] = df_result.apply(
            lambda row: self._calculate_row_score(row, tokens),
            axis=1
        )

        df_result = df_result[df_result['score'] > 0]
        df_result = df_result.sort_values(by='score', ascending=False)

        if 'search_index' in df_result.columns:
            del df_result['search_index']

        return df_result.to_dict(orient='records')


inventory_service = InventoryService()
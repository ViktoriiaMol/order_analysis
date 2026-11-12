"""Класс OrderAnalyzer: пакетный анализ CSV-файлов с заказами."""
import logging
from pathlib import Path

import pandas as pd


class OrderAnalyzer:
    def __init__(self, data_dir, reports_dir, logs_dir, output_file, log_file,
                 status_column, status_value, amount_column, required_columns):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.logs_dir = Path(logs_dir)
        self.output_file = output_file
        self.status_column = status_column
        self.status_value = status_value
        self.amount_column = amount_column
        self.required_columns = list(required_columns)
        self.processed = 0
        self.failed = 0

        for d in (self.reports_dir, self.logs_dir):
            d.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger(self.logs_dir / log_file)

    @staticmethod
    def _setup_logger(path):
        logger = logging.getLogger("order_analyzer")
        logger.setLevel(logging.ERROR)
        logger.handlers.clear()
        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
        return logger

    def load_file(self, path):
        """Читает CSV и проверяет структуру. Бросает исключение при ошибке."""
        df = pd.read_csv(path)  # EmptyDataError, ParserError — пробрасываются
        if df.empty:
            raise ValueError("файл не содержит записей")
        missing = [c for c in self.required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"отсутствуют колонки: {missing}")
        df[self.amount_column] = pd.to_numeric(df[self.amount_column], errors="raise")
        return df

    def filter_delivered(self, df):
        return df[df[self.status_column] == self.status_value]

    def calculate_metrics(self, df):
        amounts = df[self.amount_column]
        count = int(len(amounts))
        return {
            "total_revenue": round(float(amounts.sum()), 2),
            "average_check": round(float(amounts.mean()), 2) if count else 0.0,
            "orders_count": count,
        }

    def process_file(self, path):
        """Обрабатывает один файл; при ошибке логирует и возвращает None."""
        path = Path(path)
        try:
            df = self.load_file(path)
            metrics = self.calculate_metrics(self.filter_delivered(df))
        except Exception as e:
            self.failed += 1
            self.logger.error("Файл %s пропущен: %s: %s", path.name, type(e).__name__, e)
            return None
        self.processed += 1
        return {"file_name": path.name, **metrics}

    def process_all(self):
        """Обрабатывает все CSV в data/ и сохраняет сводный отчёт."""
        self.processed = self.failed = 0
        rows = []
        for path in sorted(self.data_dir.glob("*.csv")):
            result = self.process_file(path)
            if result:
                rows.append(result)
        columns = ["file_name", "total_revenue", "average_check", "orders_count"]
        report = pd.DataFrame(rows, columns=columns)
        report.to_csv(self.reports_dir / self.output_file, index=False)
        return report

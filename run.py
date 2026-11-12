"""Точка входа: python run.py"""
import config
from src.analyzer import OrderAnalyzer


def main():
    analyzer = OrderAnalyzer(
        data_dir=config.DATA_DIR,
        reports_dir=config.REPORTS_DIR,
        logs_dir=config.LOGS_DIR,
        output_file=config.OUTPUT_FILE,
        log_file=config.LOG_FILE,
        status_column=config.STATUS_COLUMN,
        status_value=config.STATUS_VALUE,
        amount_column=config.AMOUNT_COLUMN,
        required_columns=config.REQUIRED_COLUMNS,
    )
    report = analyzer.process_all()
    print(report.to_string(index=False))
    print(f"Обработано файлов: {analyzer.processed}")
    print(f"Файлов с ошибками: {analyzer.failed}")


if __name__ == "__main__":
    main()

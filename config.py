"""Настройки проекта."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

OUTPUT_FILE = "summary_report.csv"
LOG_FILE = "errors.log"

STATUS_COLUMN = "status"
STATUS_VALUE = "Delivered"
AMOUNT_COLUMN = "total_amount"

REQUIRED_COLUMNS = [
    "order_id", "person_id", "order_date", "status", "total_amount",
    "currency", "payment_method", "shipping_method", "notes",
]

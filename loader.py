import pandas as pd
import os
from colorama import Fore, init

init(autoreset=True)

def load_csv(filepath):
    """Load and validate a CSV file. Returns a DataFrame."""

    # 1. Check file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # 2. Check it is a CSV
    if not filepath.endswith(".csv"):
        raise ValueError(f"Expected a .csv file, got: {filepath}")

    # 3. Load with encoding fallback
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin-1")

    # 4. Check not empty
    if df.empty:
        raise ValueError("The CSV file is empty.")

    # 5. Parse date columns automatically
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    print(Fore.GREEN + f"Loaded: {filepath}")
    print(f"  Rows: {df.shape[0]:,}  Columns: {df.shape[1]}")
    return df
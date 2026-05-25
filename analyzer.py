import pandas as pd
from tabulate import tabulate
from colorama import Fore, init

init(autoreset=True)

def summary(df):
    """Print dataset overview — shape, types, nulls."""
    print(Fore.CYAN + "\n=== Dataset Summary ===")
    print(f"Rows     : {df.shape[0]:,}")
    print(f"Columns  : {df.shape[1]}")
    print(f"Memory   : {df.memory_usage(deep=True).sum() / 1024:.1f} KB\n")

    info = pd.DataFrame({
        "Column"  : df.columns,
        "Type"    : df.dtypes.values,
        "Non-Null": df.notnull().sum().values,
        "Nulls"   : df.isnull().sum().values,
        "Unique"  : df.nunique().values
    })
    print(tabulate(info, headers="keys",
                   tablefmt="rounded_outline",
                   showindex=False))


def stats(df, column):
    """Print full statistics for a numeric column."""
    if column not in df.columns:
        print(Fore.RED + f"Column '{column}' not found.")
        print("Available columns: " + ", ".join(df.columns))
        return

    s = df[column].dropna()
    print(Fore.CYAN + f"\n=== Stats: {column} ===")
    data = [
        ["Count"  , f"{len(s):,}"],
        ["Mean"   , f"{s.mean():.2f}"],
        ["Median" , f"{s.median():.2f}"],
        ["Std Dev", f"{s.std():.2f}"],
        ["Min"    , f"{s.min():.2f}"],
        ["25%"    , f"{s.quantile(0.25):.2f}"],
        ["75%"    , f"{s.quantile(0.75):.2f}"],
        ["Max"    , f"{s.max():.2f}"],
    ]
    print(tabulate(data, headers=["Metric", "Value"],
                   tablefmt="rounded_outline"))


def filter_data(df, column, operator, value):
    """Filter rows by condition. Returns filtered DataFrame."""
    if column not in df.columns:
        print(Fore.RED + f"Column '{column}' not found.")
        print("Available columns: " + ", ".join(df.columns))
        return None

    ops = {
        "eq"      : lambda c, v: c == v,
        "ne"      : lambda c, v: c != v,
        "gt"      : lambda c, v: c > float(v),
        "lt"      : lambda c, v: c < float(v),
        "gte"     : lambda c, v: c >= float(v),
        "lte"     : lambda c, v: c <= float(v),
        "contains": lambda c, v: c.astype(str).str.contains(v, case=False)
    }

    if operator not in ops:
        print(Fore.RED + f"Unknown operator: '{operator}'")
        print("Use: eq  ne  gt  lt  gte  lte  contains")
        return None

    mask   = ops[operator](df[column], value)
    result = df[mask]

    print(Fore.CYAN + f"\n=== Filter: {column} {operator} {value} ===")
    print(f"Matched : {len(result):,} of {len(df):,} rows\n")

    print(tabulate(result.head(20), headers="keys",
                   tablefmt="rounded_outline",
                   showindex=False))
    return result
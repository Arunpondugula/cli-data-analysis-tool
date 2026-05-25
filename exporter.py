import os
from colorama import Fore, init
import analyzer

init(autoreset=True)


def export(df, column, operator, value, out_path):
    """Filter the DataFrame and save the result to a CSV file."""

    # Run the filter
    result = analyzer.filter_data(df, column, operator, value)

    # Nothing matched
    if result is None or result.empty:
        print(Fore.YELLOW + "No rows matched — nothing exported.")
        return

    # Create output folder if it does not exist
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Save to CSV
    result.to_csv(out_path, index=False)
    print(Fore.GREEN + f"Exported {len(result):,} rows to: {out_path}")
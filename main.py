import argparse
import sys
import loader
import analyzer
import plotter
import exporter
from colorama import Fore, init

init(autoreset=True)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="eda",
        description="EDA CLI Tool — Exploratory Data Analysis from your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py summary --file data/superstore.csv
  python main.py stats   --file data/superstore.csv --col Sales
  python main.py filter  --file data/superstore.csv --col Region --op eq --val West
  python main.py plot    --file data/superstore.csv --type hist --col Profit
  python main.py plot    --file data/superstore.csv --type bar  --col Category --val Sales
  python main.py plot    --file data/superstore.csv --type scatter --col Sales --val Profit
  python main.py export  --file data/superstore.csv --col Profit --op lt --val 0
        """
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ── summary ──────────────────────────────────────────────
    p_summary = sub.add_parser("summary",
        help="Dataset overview: shape, types, nulls")
    p_summary.add_argument("--file", required=True,
        help="Path to CSV file")

    # ── stats ─────────────────────────────────────────────────
    p_stats = sub.add_parser("stats",
        help="Full statistics for a numeric column")
    p_stats.add_argument("--file", required=True,
        help="Path to CSV file")
    p_stats.add_argument("--col", required=True,
        help="Column name")

    # ── filter ────────────────────────────────────────────────
    p_filter = sub.add_parser("filter",
        help="Filter rows by a condition")
    p_filter.add_argument("--file", required=True,
        help="Path to CSV file")
    p_filter.add_argument("--col", required=True,
        help="Column to filter on")
    p_filter.add_argument("--op", required=True,
        choices=["eq", "ne", "gt", "lt", "gte", "lte", "contains"],
        help="Operator: eq ne gt lt gte lte contains")
    p_filter.add_argument("--val", required=True,
        help="Value to filter by")

    # ── plot ──────────────────────────────────────────────────
    p_plot = sub.add_parser("plot",
        help="Generate a chart saved as PNG")
    p_plot.add_argument("--file", required=True,
        help="Path to CSV file")
    p_plot.add_argument("--type", required=True,
        choices=["hist", "bar", "scatter"],
        help="Chart type: hist bar scatter")
    p_plot.add_argument("--col", required=True,
        help="Column name (x-axis for scatter, group for bar)")
    p_plot.add_argument("--val",
        help="Value column for bar and scatter charts")

    # ── export ────────────────────────────────────────────────
    p_export = sub.add_parser("export",
        help="Filter rows and save to a new CSV")
    p_export.add_argument("--file", required=True,
        help="Path to CSV file")
    p_export.add_argument("--col", required=True,
        help="Column to filter on")
    p_export.add_argument("--op", required=True,
        choices=["eq", "ne", "gt", "lt", "gte", "lte", "contains"],
        help="Operator: eq ne gt lt gte lte contains")
    p_export.add_argument("--val", required=True,
        help="Value to filter by")
    p_export.add_argument("--out",
        default="outputs/filtered.csv",
        help="Output file path (default: outputs/filtered.csv)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # No command given — show help
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Load the data first — every command needs it
    try:
        df = loader.load_csv(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(Fore.RED + f"Error: {e}")
        sys.exit(1)

    # Route to the right function
    if args.command == "summary":
        analyzer.summary(df)

    elif args.command == "stats":
        analyzer.stats(df, args.col)

    elif args.command == "filter":
        analyzer.filter_data(df, args.col, args.op, args.val)

    elif args.command == "plot":
        if args.type == "hist":
            plotter.histogram(df, args.col)
        elif args.type == "bar":
            if not args.val:
                print(Fore.RED + "Error: --val required for bar chart")
                print("Example: --col Category --val Sales")
                sys.exit(1)
            plotter.bar_chart(df, args.col, args.val)
        elif args.type == "scatter":
            if not args.val:
                print(Fore.RED + "Error: --val required for scatter chart")
                print("Example: --col Sales --val Profit")
                sys.exit(1)
            plotter.scatter(df, args.col, args.val)

    elif args.command == "export":
        exporter.export(df, args.col, args.op, args.val, args.out)


if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
import os
from colorama import Fore, init

init(autoreset=True)

OUTPUT_DIR = "outputs"


def _save(fig, filename):
    """Save figure to outputs folder and close it."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(Fore.GREEN + f"Saved: {path}")


def histogram(df, column, bins=30):
    """Distribution histogram for a numeric column."""
    if column not in df.columns:
        print(Fore.RED + f"Column '{column}' not found.")
        print("Available columns: " + ", ".join(df.columns))
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df[column].dropna(), bins=bins,
            color="#4A90D9", edgecolor="white", linewidth=0.5)
    ax.set_title(f"Distribution of {column}",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    _save(fig, f"hist_{column}.png")


def bar_chart(df, group_col, value_col, agg="sum", top_n=10):
    """Bar chart — group by one column, aggregate another."""
    for col in [group_col, value_col]:
        if col not in df.columns:
            print(Fore.RED + f"Column '{col}' not found.")
            print("Available columns: " + ", ".join(df.columns))
            return

    grouped = (df.groupby(group_col)[value_col]
                 .agg(agg)
                 .sort_values(ascending=False)
                 .head(top_n))

    fig, ax = plt.subplots(figsize=(12, 5))
    grouped.plot(kind="bar", ax=ax,
                 color="#4A90D9", edgecolor="white")
    ax.set_title(
        f"{agg.capitalize()} of {value_col} by {group_col} (Top {top_n})",
        fontsize=14, fontweight="bold")
    ax.set_xlabel(group_col)
    ax.set_ylabel(value_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    _save(fig, f"bar_{group_col}_{value_col}.png")


def scatter(df, x_col, y_col):
    """Scatter plot showing correlation between two columns."""
    for col in [x_col, y_col]:
        if col not in df.columns:
            print(Fore.RED + f"Column '{col}' not found.")
            print("Available columns: " + ", ".join(df.columns))
            return

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(df[x_col], df[y_col],
               alpha=0.4, color="#4A90D9",
               edgecolors="none", s=20)
    corr = df[[x_col, y_col]].corr().iloc[0, 1]
    ax.set_title(f"{x_col} vs {y_col}  (r = {corr:.3f})",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    plt.tight_layout()
    _save(fig, f"scatter_{x_col}_{y_col}.png")
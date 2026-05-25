# CLI Data Analysis Tool

I built this tool because I was tired of opening Jupyter notebooks every time
I wanted to quickly explore a dataset. This is a command-line tool that lets
you load, analyse, filter, visualise, and export any CSV dataset directly
from your terminal — no notebook, no browser, no setup every time.

It works with any CSV file. Just point it at your data and start asking questions.

---

## What it can do

| Command   | What it does                                           |
|-----------|--------------------------------------------------------|
| `summary` | Instant overview — shape, column types, nulls, memory  |
| `stats`   | Deep statistics for any numeric column                 |
| `filter`  | Find rows matching any condition                       |
| `plot`    | Generate charts saved as PNG to your outputs folder    |
| `export`  | Filter and save results to a new CSV                   |

---

## Project structure

I kept the code modular — each file has one job and one job only.

cli-data-analysis-tool/
├── main.py          ← entry point — parses commands and routes them
├── loader.py        ← loads and validates any CSV with error handling
├── analyzer.py      ← summary, stats, and filter logic
├── plotter.py       ← generates and saves charts as PNG files
├── exporter.py      ← filters rows and saves results to CSV
├── data/            ← put your CSV datasets here
├── outputs/         ← all generated charts and exports land here
└── requirements.txt

If I want to add a new chart type in the future I only touch `plotter.py`.
Nothing else needs to change. That is why I structured it this way.

---

## Getting started

```bash
git clone https://github.com/ArunPondugula/cli-data-analysis-tool
cd cli-data-analysis-tool
pip install -r requirements.txt
```

Download your dataset and drop it in the `data/` folder. Then you are ready.

---

## How to use it

All examples below use the Superstore dataset but every command works
the same way with any CSV file you provide.

```bash
# Get an overview of your dataset
python main.py summary --file data/superstore.csv

# See full statistics for any numeric column
python main.py stats --file data/superstore.csv --col Sales
python main.py stats --file data/superstore.csv --col Profit

# Filter rows by any condition
python main.py filter --file data/superstore.csv --col Region --op eq --val West
python main.py filter --file data/superstore.csv --col Profit --op lt --val 0
python main.py filter --file data/superstore.csv --col Product Name --op contains --val Chair

# Generate charts — automatically saved to outputs/
python main.py plot --file data/superstore.csv --type hist    --col Profit
python main.py plot --file data/superstore.csv --type bar     --col Category --val Sales
python main.py plot --file data/superstore.csv --type scatter --col Sales    --val Profit

# Export filtered results to a new CSV
python main.py export --file data/superstore.csv --col Profit --op lt --val 0 --out outputs/loss_orders.csv
```

---

## Filter operators

| Operator   | Meaning                            | Example                         |
|------------|------------------------------------|---------------------------------|
| `eq`       | Equal to                           | `--op eq --val West`            |
| `ne`       | Not equal to                       | `--op ne --val West`            |
| `gt`       | Greater than                       | `--op gt --val 1000`            |
| `lt`       | Less than                          | `--op lt --val 0`               |
| `gte`      | Greater than or equal to           | `--op gte --val 500`            |
| `lte`      | Less than or equal to              | `--op lte --val 100`            |
| `contains` | String contains (case-insensitive) | `--op contains --val Chair`     |

---

## What I found in the Superstore data

I used this tool to analyse the Sample Superstore dataset and found some
genuinely interesting things that I would not have spotted just by scrolling
through the raw CSV.

- **1,871 out of 9,994 orders lose money** — that is nearly 1 in 5 orders
  with negative profit. A serious problem hiding in plain sight.

- **The mean sale is $229 but the median is only $54** — the average is being
  pulled up by a small number of very large orders. Most orders are actually
  quite small.

- **Technology has the highest profit margin at around 17%** — while Furniture
  barely breaks even and some sub-categories actively lose money.

- **The Tables sub-category consistently loses money** — every time the company
  sells a table, they lose on average. That is a fixable business problem.

- **West region drives the highest total sales** across all four regions.

All of these were found using the exact commands shown above.

---

## Dataset credit

**Dataset:** Sample Superstore — originally published by Tableau
**Downloaded from:** [Kaggle — vivek468/superstore-dataset-final](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

This dataset is publicly available on Kaggle for educational and analytical
purposes. All credit for the dataset goes to the original author. I used it
solely to demonstrate the tool's capabilities.

---

## A few things I am proud of

**Encoding fallback** — the loader tries UTF-8 first, falls back to Latin-1
automatically. Real-world CSVs come from all kinds of software and encoding
errors are one of the most common things that break naive scripts.

**Charts save to disk** — I made a deliberate choice not to show plots
interactively. This means the tool works on remote servers, inside Docker
containers, and in CI pipelines where there is no display available.

**Every command validates inputs** — if you give it a column that does not
exist, it tells you exactly what went wrong and lists the available columns.
No cryptic Python tracebacks.

**Works on any CSV** — there is no hardcoded logic tied to the Superstore
dataset. Drop in any CSV and every command works the same way.

---

## Tech stack

- **Python** — core language
- **Pandas** — data loading, filtering, and analysis
- **Matplotlib** — chart generation
- **Tabulate** — clean formatted tables in the terminal
- **Colorama** — coloured output that works on Windows, Mac, and Linux
- **Argparse** — CLI interface with subcommands and built-in validation

---

## About

I am Arun Pondugula, a Java developer transitioning into AI engineering.
This is one of the foundational projects in my  journey to become
an AI engineer. I built it to strengthen my Python fundamentals
and get comfortable building modular, production-style tools before moving
on to RAG systems, AI agents, and the Claude API.

[GitHub](https://github.com/ArunPondugula) · [LinkedIn](https://linkedin.com/in/arunpondugula)

---
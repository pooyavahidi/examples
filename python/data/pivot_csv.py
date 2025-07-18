import sys
import argparse
import pandas as pd


def pivot(infile, outfile, pivot_col, value_col):
    """
    Read CSV from infile, pivot values in `pivot_col` into new columns,
    placing the corresponding `value_col` under each, and write to outfile.
    """
    # Load into a DataFrame
    df = pd.read_csv(infile)

    # Identify the “index” columns (everything except pivot_col & value_col)
    index_cols = [c for c in df.columns if c not in {pivot_col, value_col}]

    # Perform the pivot
    # aggfunc="first", assume one value per (index, pivot) pair
    # Then turn index-cols back into columns
    wide = df.pivot_table(
        index=index_cols,
        columns=pivot_col,
        values=value_col,
        aggfunc="first",
    ).reset_index()

    # Clean up the MultiIndex name (so headers are just the keys)
    wide.columns.name = None

    # Write out
    wide.to_csv(outfile, index=False)


def main():
    parser = argparse.ArgumentParser(
        description="Pivot a CSV into wide format"
    )
    parser.add_argument(
        "-i", "--input", help="input CSV file (defaults to stdin)"
    )
    parser.add_argument(
        "-p", "--pivot", required=True, help="column to pivot (e.g. 'type')"
    )
    parser.add_argument(
        "-v",
        "--value",
        required=True,
        help="column to fill in values (e.g. 'amount')",
    )
    args = parser.parse_args()

    outfile = sys.stdout

    # Open input file or use stdin
    if args.input:
        with open(args.input, newline="", encoding="utf-8") as infile:
            pivot(infile, outfile, args.pivot, args.value)
    else:
        pivot(sys.stdin, outfile, args.pivot, args.value)


if __name__ == "__main__":
    main()

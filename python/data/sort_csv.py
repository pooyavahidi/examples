import sys
import argparse
import pandas as pd


def sort_csv(infile, outfile, sort_cols, ascending=True):
    """
    Read CSV from infile, sort by specified columns, and write to outfile.
    """
    # Load into a DataFrame
    df = pd.read_csv(infile)

    # Sort the DataFrame
    if isinstance(sort_cols, str):
        sort_cols = [sort_cols]

    sorted_df = df.sort_values(by=sort_cols, ascending=ascending)

    # Write out
    sorted_df.to_csv(outfile, index=False)


def main():
    parser = argparse.ArgumentParser(
        description="Sort a CSV file by specified columns"
    )
    parser.add_argument(
        "-i", "--input", help="input CSV file (defaults to stdin)"
    )
    parser.add_argument(
        "-c", "--columns", required=True, nargs="+",
        help="column(s) to sort by (e.g. 'name' or 'date amount')"
    )
    parser.add_argument(
        "-d", "--descending", action="store_true",
        help="sort in descending order (default is ascending)"
    )
    args = parser.parse_args()

    # Determine sort order
    ascending = not args.descending

    outfile = sys.stdout

    # Open input file or use stdin
    if args.input:
        with open(args.input, newline="", encoding="utf-8") as infile:
            sort_csv(infile, outfile, args.columns, ascending)
    else:
        sort_csv(sys.stdin, outfile, args.columns, ascending)


if __name__ == "__main__":
    main()

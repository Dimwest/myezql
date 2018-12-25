import argparse
import os
from antlrparser.extractor import FileProcessor
from output.json import to_json, summarize
from output.cmd import beautify
from output.mermaid import Mermaid
import timeit

if __name__ == '__main__':

    start = timeit.default_timer()

    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "dir",
        type=str,
        help="Directory containing the SQL procedures to parse")

    argparser.add_argument(
        "dest", type=str, help="Directory receiving the output files")

    argparser.add_argument(
        "--out",
        type=str,
        help="Output format, defaults to mermaid",
        required=False)

    argparser.add_argument(
        "--r",
        type=int,
        help="Walk recursively through the utils directory, can be 0 or 1",
        required=False)

    argparser.add_argument(
        "--d",
        type=str,
        help="Delimiter used for identifying stored procedures",
        required=False)

    argparser.add_argument(
        "--dialect",
        type=str,
        help="SQL dialect of files to parse. Currently unused.",
        required=False)

    args = argparser.parse_args()

    # Validating required parameters
    assert os.path.isdir(args.dir) and os.path.exists(
        args.dir), f"{args.dir} is not a valid directory"

    # Required arguments variables
    input_dir = args.dir
    output_dir = args.dest

    # Validating optional parameters
    SUPPORTED_DIALECTS = ['mysql', 'postgres']
    if args.dialect:
        assert args.dialect.lower(
        ) in SUPPORTED_DIALECTS, f"{args.dialect} is not a supported dialect. " \
                                 f"Supported dialects are: {SUPPORTED_DIALECTS}"

    SUPPORTED_OUTPUTS = ['mermaid']
    if args.out:
        assert args.out.lower(
        ) in SUPPORTED_OUTPUTS, f"{args.out} is not a supported format. " \
                                f"Supported formats are: {SUPPORTED_OUTPUTS}"

    if args.r:
        assert args.r in (
            0, 1), f"{args.r} is not a valid value. " \
                   f"-r must be either 0 or 1"

    # Optional arguments variables
    output_format = 'mermaid' if not args.out else args.out
    recursive = False if not args.r else args.r
    delimiter = ";;" if not args.d else args.d
    dialect = None if not args.dialect else args.dialect

    walker = FileProcessor()
    walker.parse_dir(input_dir)
    results = walker.results
    errors = walker.errored

    beautify(results)
    to_json(results, args.dest)
    mermaid = Mermaid(args.dest)

    summarize(f"{args.dest}")

    stop = timeit.default_timer()

    print('Execution finished in: ', stop - start, 'seconds')

import argparse
import ast
import logging
import sys
import radon.complexity as cc
import radon.raw as raw

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Calculates code complexity metrics for Python code."
    )
    parser.add_argument(
        "filepath", help="Path to the Python file to analyze."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=10,
        help="Complexity threshold for reporting functions/classes. Defaults to 10.",
    )
    parser.add_argument(
        "--report-raw",
        action="store_true",
        help="Also report raw code metrics (lines of code, comments, etc.)"
    )
    parser.add_argument(
        "--include-imports",
        action="store_true",
        help="Include import statements in the code complexity calculation."
    )
    return parser.parse_args()


def calculate_cyclomatic_complexity(filepath, include_imports=False):
    """
    Calculates the cyclomatic complexity of functions and classes in a Python file.

    Args:
        filepath (str): Path to the Python file.
        include_imports (bool): Whether to include import statements during parsing.

    Returns:
        list: A list of tuples containing the function/class name, complexity score,
              line number, and end line number. Returns an empty list if there's an error.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        if not include_imports:
            tree = ast.parse(code)
            # Remove Import and ImportFrom nodes from the AST to exclude them from complexity analysis.
            new_body = []
            for node in tree.body:
                if not isinstance(node, (ast.Import, ast.ImportFrom)):
                    new_body.append(node)
            tree.body = new_body
            code = ast.unparse(tree)
        
        results = cc.cc_visit(code)
        return [(res.name, res.complexity, res.lineno, res.endline) for res in results]

    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return []
    except SyntaxError as e:
        logging.error(f"Syntax error in {filepath}: {e}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return []


def calculate_raw_metrics(filepath):
    """
    Calculates raw code metrics like lines of code, comments, blank lines, etc.

    Args:
        filepath (str): Path to the Python file.

    Returns:
        dict: A dictionary containing raw metrics. Returns an empty dictionary if there's an error.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        metrics = raw.analyze(code)
        return {
            "sloc": metrics.sloc,
            "lloc": metrics.lloc,
            "comments": metrics.comments,
            "multi": metrics.multi,
            "blank": metrics.blank,
            "single_comments": metrics.single_comments
        }
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return {}
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return {}

def main():
    """
    Main function to execute the code complexity analysis.
    """
    args = setup_argparse()

    # Input validation for threshold
    if args.threshold <= 0:
        logging.error("Complexity threshold must be a positive integer.")
        sys.exit(1)

    complexity_results = calculate_cyclomatic_complexity(args.filepath, args.include_imports)

    if complexity_results:
        print(f"Code Complexity Analysis for {args.filepath}:\n")
        for name, complexity, lineno, endline in complexity_results:
            print(f"  - {name} (lines {lineno}-{endline}): Complexity = {complexity}")
            if complexity > args.threshold:
                print(f"    Warning: Complexity exceeds threshold ({args.threshold})!")
        print("\n")

    if args.report_raw:
        raw_metrics = calculate_raw_metrics(args.filepath)
        if raw_metrics:
            print("Raw Code Metrics:\n")
            for metric, value in raw_metrics.items():
                print(f"  - {metric}: {value}")
            print("\n")

    if not complexity_results and not args.report_raw:
        logging.info("No results to display.")

if __name__ == "__main__":
    # Example usage (from command line):
    # python main.py my_python_file.py --threshold 15 --report-raw
    # python main.py my_python_file.py
    main()
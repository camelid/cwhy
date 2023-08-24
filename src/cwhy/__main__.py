#! /usr/bin/env python3

import argparse
import importlib.metadata
import os
import subprocess
import sys
import tempfile
import textwrap

from . import cwhy


def main():
    parser = argparse.ArgumentParser(
        prog="cwhy",
        description="CWhy explains and fixes compiler diagnostic errors.",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="print the version of cwhy and exit",
    )

    parser.add_argument(
        "--llm",
        type=str,
        default="gpt-3.5-turbo",
        help="the language model to use, e.g., 'gpt-3.5-turbo' or 'gpt-4' (default: gpt-3.5-turbo)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="timeout for API calls in seconds (default: 60)",
    )
    # The default maximum context length for `gpt-3.5-turbo` is 4096 tokens.
    # We keep 256 tokens for other parts of the prompt, and split the remainder in two
    # for the error message and code sections, resulting in 1920 tokens for each.
    parser.add_argument(
        "--max-error-tokens",
        type=int,
        default=1920,
        help="maximum number of tokens from the error message to send in the prompt (default: 1920)",
    )
    parser.add_argument(
        "--max-code-tokens",
        type=int,
        default=1920,
        help="maximum number of code locations tokens to send in the prompt (default: 1920)",
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="only print prompt and exit (for debugging purposes)",
    )
    parser.add_argument(
        "--compiler-wrapper",
        metavar="COMPILER",
        type=str,
        default=None,
        help="enable compiler wrapper mode, providing the path to the compiler to wrap",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="enables interactive mode (currently only supported for the diff command)",
    )

    parser.add_argument(
        "subcommand",
        type=str,
        nargs="?",
        default="explain",
        help="explain, fix, diff, or extract-sources (default: explain)",
    )

    parser.add_argument(
        "---",
        dest="command",
        default=None,
        help=argparse.SUPPRESS,
        nargs=argparse.REMAINDER,
    )

    args = vars(parser.parse_args())

    if args["version"]:
        print(f"cwhy version {importlib.metadata.metadata('cwhy')['Version']}")
        sys.exit(0)

    if not (bool(args["command"]) ^ bool(args["compiler_wrapper"])):
        print(
            "Error: Please specify either a command to run (using ---) or --compiler-wrapper, but not both."
        )
        print()
        parser.print_help()
        sys.exit(1)

    if args["compiler_wrapper"]:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(
                textwrap.dedent(
                    f"""
                #! /usr/bin/env python3
                import sys
                from cwhy import cwhy
                cwhy.wrapper({args}, ["{args["compiler_wrapper"]}", *sys.argv[1:]])
                """
                ).lstrip()
            )
        # NamedTemporaryFiles are not executable by default. Set its mode to 755 here with an octal literal.
        os.chmod(f.name, 0o755)
        print(f.name)
    else:
        cwhy.wrapper(args, args["command"])

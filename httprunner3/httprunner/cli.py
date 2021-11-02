import argparse
import enum
import os
import sys

import pytest
from loguru import logger
from sentry_sdk import capture_message

sys.path.insert(0, os.getcwd())
from httprunner import __description__, __version__
from httprunner.compat import ensure_cli_args
from httprunner.ext.har2case import init_har2case_parser, main_har2case
from httprunner.make import init_make_parser, main_make
from httprunner.scaffold import init_parser_scaffold, main_scaffold
from httprunner.utils import init_sentry_sdk
from pathlib import Path

init_sentry_sdk()

BASE_DIR = Path(__file__).parent.parent


def init_parser_run(subparsers):
    sub_parser_run = subparsers.add_parser(
        "run", help="Make HttpRunner testcases and run with pytest."
    )
    sub_parser_run.add_argument(
        "--config", default="config/local.yml", help="Config YAML file path"
    )
    return sub_parser_run


def main_run(extra_args, config) -> enum.IntEnum:
    capture_message("start to run")
    logger.debug(f"[main run] config ==> {config}")
    logger.debug(f"[main run] extra_args ==> {extra_args}")
    # keep compatibility with v2
    extra_args = ensure_cli_args(extra_args)

    tests_path_list = []
    extra_args_new = []
    for item in extra_args:
        if not os.path.exists(item):
            # item is not file/folder path
            extra_args_new.append(item)
        else:
            # item is file/folder path
            tests_path_list.append(item)

    if config:
        extra_args_new.append(f"--config={config}")

    if len(tests_path_list) == 0:
        # has not specified any test_cases path
        logger.error(f"No valid testcase path in cli arguments: {extra_args}")
        sys.exit(1)

    testcase_path_list = main_make(tests_path_list)
    # config_to_debugtalk_make(config)
    # move_pytest_files_to_target(os.path.join(BASE_DIR, "test_cases"))
    # if not testcase_path_list:
    #     logger.error("No valid testcases found, exit 1.")
    #     sys.exit(1)

    if "--tb=short" not in extra_args_new:
        extra_args_new.append("--tb=short")
    if "-v" not in extra_args_new:
        extra_args_new.append("-v")
    for index, testcase_path in enumerate(testcase_path_list):
        testcase_path_list[index] = testcase_path.replace("test_cases", "target")
    extra_args_new.extend(testcase_path_list)
    logger.info(f"start to run tests with pytest. HttpRunner version: {__version__}")
    logger.info(f"extra_args_new ==> {extra_args_new}")
    return pytest.main(extra_args_new)


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="show version"
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_run = init_parser_run(subparsers)
    sub_parser_scaffold = init_parser_scaffold(subparsers)
    sub_parser_har2case = init_har2case_parser(subparsers)
    sub_parser_make = init_make_parser(subparsers)

    if len(sys.argv) == 1:
        # httprunner
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-V", "--version"]:
            # httprunner -V
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # httprunner -h
            parser.print_help()
        elif sys.argv[1] == "startproject":
            # httprunner startproject
            sub_parser_scaffold.print_help()
        elif sys.argv[1] == "har2case":
            # httprunner har2case
            sub_parser_har2case.print_help()
        elif sys.argv[1] == "run":
            # httprunner run
            pytest.main(["-h"])
        elif sys.argv[1] == "make":
            # httprunner make
            sub_parser_make.print_help()

        sys.exit(0)
    elif (
            len(sys.argv) == 3 and sys.argv[1] == "run" and sys.argv[2] in ["-h", "--help"]
    ):
        # httprunner run -h
        pytest.main(["-h"])
        sys.exit(0)

    extra_args = []
    if len(sys.argv) >= 2 and sys.argv[1] in ["run", "locusts"]:
        args, extra_args = parser.parse_known_args()
    else:
        args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    logger.debug(f"[main] args ==> {args}")
    logger.debug(f"[main] extra_args ==> {extra_args}")
    if sys.argv[1] == "run":
        sys.exit(main_run(extra_args, args.config))
    elif sys.argv[1] == "startproject":
        main_scaffold(args)
    elif sys.argv[1] == "har2case":
        main_har2case(args)
    elif sys.argv[1] == "make":
        main_make(args.testcase_path)
        # config_to_debugtalk_make(args.config)
        # move_pytest_files_to_target(os.path.join(BASE_DIR, "test_cases"))


def parser_test_case_path(extra_args: list):
    """parser test case path from extra args

    Args:
        extra_args (list):

    Returns:

    Examples:
    $ python httprunner/cli.py run -sv test_cases/tests --config=online.yml
    extra_args ==> ['-sv', '--count=2', 'test_cases/tests']

    >>> parser_test_case_path(['-sv', '--count=2', 'test_cases/tests'])
        "test_cases"
    """
    for extra_arg in extra_args:
        if extra_arg.startswith("test"):
            return extra_arg.split("/")[0]


def main_hrun_alias():
    """ command alias
        hrun = httprunner run
    """
    if len(sys.argv) == 2:
        if sys.argv[1] in ["-V", "--version"]:
            # hrun -V
            sys.argv = ["httprunner", "-V"]
        elif sys.argv[1] in ["-h", "--help"]:
            pytest.main(["-h"])
            sys.exit(0)
        else:
            # hrun /path/to/test_cases
            sys.argv.insert(1, "run")
    else:
        sys.argv.insert(1, "run")

    main()


def main_make_alias():
    """ command alias
        hmake = httprunner make
    """
    sys.argv.insert(1, "make")
    main()


def main_har2case_alias():
    """ command alias
        har2case = httprunner har2case.
    """
    sys.argv.insert(1, "har2case")
    main()


if __name__ == "__main__":
    main()

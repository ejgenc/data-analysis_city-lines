from pathlib import Path
from doit.tools import run_once


def show_cmd(task):
    return "executing... %s" % task.name


def task_prepare():
    action_path = Path("src/utility-scripts/prepare.py")
    return {
        "actions": ["python {}".format(action_path)],
        "uptodate": [run_once],
        "title": show_cmd
    }


def task_create_db():
    action_path = Path("src/data-processing/create-main.py")
    return {
        "file_dep": [Path("data/main/city-lines.sql")],
        "task_dep": ["prepare"],
        "actions": ["python {}".format(action_path)],
        "title": show_cmd
    }


def task_import_db():
    action_path = Path("src/data-processing/import-main.py")
    return {
        "task_dep": ["create_db"],
        "actions": ["python {}".format(action_path)],
        "title": show_cmd
    }

def task_clean_db():
    action_path = Path("src/data-cleaning/clean-main.py")
    return {
        "task_dep": ["import_db"],
        "actions": ["python {}".format(action_path)],
        "title": show_cmd
    }

def task_clean_externals():
    action_path = Path("src/data-cleaning/clean-externals.py")
    return {
        "task_dep": ["clean_db"],
        "file_dep": [Path("data/external/transport-modes.csv"),
                     Path("data/external/mobile-phone-usage.csv"),
                     Path("data/external/world-happiness-report.csv")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/cleaned/mobile-phone-usage-cleaned.csv"),
                    Path("data/cleaned/world-happiness-report-cleaned.csv")],
        "title": show_cmd
    }

def task_import_externals():
    action_path = Path("src/data-processing/import-externals.py")
    return {
        "task_dep": ["clean_externals"],
        "file_dep": [Path("data/external/transport-modes.csv"),
                     Path("data/cleaned/mobile-phone-usage-cleaned.csv"),
                     Path("data/cleaned/world-happiness-report-cleaned.csv")],
        "actions": ["python {}".format(action_path)],
        "title": show_cmd
    }

def task_teardown():
    action_path = Path("src/utility-scripts/teardown.py")
    return {
        "actions": ["python {}".format(action_path)],
        "title": show_cmd
    }

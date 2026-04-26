import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT_DIR / "tests" / "cases"
POSITIVE_CASES_DIR = CASES_DIR / "positive"
NEGATIVE_CASES_DIR = CASES_DIR / "negative"


def case_ids(files):
    return [file.stem for file in files]


POSITIVE_CASES = sorted(POSITIVE_CASES_DIR.glob("*.txt"))
NEGATIVE_CASES = sorted(NEGATIVE_CASES_DIR.glob("*.txt"))


def run_cli(input_file):
    return subprocess.run(
        [sys.executable, "-m", "src.main", str(input_file)],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("case_file", POSITIVE_CASES, ids=case_ids(POSITIVE_CASES))
def test_positive_cases(case_file, tmp_path):
    test_input = tmp_path / case_file.name
    shutil.copy(case_file, test_input)

    completed = run_cli(test_input)
    expected_output = case_file.with_suffix(".txt.out").read_text(encoding="utf-8")
    if not expected_output.strip():
        expected_output = ""
    actual_output_file = tmp_path / f"{case_file.name}.out"

    assert completed.returncode == 0
    assert "Success! Lexical analysis saved to" in completed.stdout
    assert actual_output_file.exists()
    assert actual_output_file.read_text(encoding="utf-8") == expected_output


@pytest.mark.parametrize("case_file", NEGATIVE_CASES, ids=case_ids(NEGATIVE_CASES))
def test_negative_cases(case_file, tmp_path):
    test_input = tmp_path / case_file.name
    shutil.copy(case_file, test_input)

    completed = run_cli(test_input)
    expected_error = case_file.with_suffix(".txt.err").read_text(encoding="utf-8").strip()
    actual_output_file = tmp_path / f"{case_file.name}.out"

    assert completed.returncode == 0
    assert completed.stdout.strip() == expected_error
    assert not actual_output_file.exists()

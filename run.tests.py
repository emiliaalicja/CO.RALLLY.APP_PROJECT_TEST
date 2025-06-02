import pytest
import sys
import os

def main():
    test_dir = os.path.abspath("Tests")

    pytest_args = [
        test_dir,
        "--maxfail=10",  # zatrzymaj po 2 błędach
        "--tb=short",  # skrócony traceback
        "--html=report.html",  # raport HTML (wymaga pytest-html)
        "--self-contained-html"
    ]

    exit_code = pytest.main(pytest_args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

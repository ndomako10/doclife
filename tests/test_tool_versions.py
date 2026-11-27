"""The toolchain's own consistency: versions pinned in two places agree."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CI = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
PRE_COMMIT = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
LOCK = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")


class TestToolVersions:
    def test_when_ci_and_pre_commit_both_run_ruff_they_use_one_version(self):
        locked = re.findall(r"^ruff==(\S+)", LOCK, re.MULTILINE)
        assert len(locked) == 1
        assert locked == re.findall(r"/ruff-pre-commit\n\s+rev: v(\S+)", PRE_COMMIT)

    def test_when_ci_and_pre_commit_both_run_gitleaks_they_use_one_version(self):
        in_ci = re.findall(r"GITLEAKS_VERSION: (\S+)", CI)
        assert len(in_ci) == 1
        assert in_ci == re.findall(r"/gitleaks\n\s+rev: v(\S+)", PRE_COMMIT)


class TestPythonInstalls:
    @pytest.mark.parametrize("command", re.findall(r"pip install .*", CI))
    def test_when_ci_installs_python_packages_nothing_unpinned_is_downloaded(
        self, command
    ):
        from_lock = "--require-hashes --only-binary :all:" in command
        local_only = "--no-index --no-deps" in command
        assert from_lock or local_only

from importlib.metadata import version

import pytest

from doclife.cli import main


class TestCli:
    def test_when_asked_for_its_version_prints_the_installed_version(self, capsys):
        with pytest.raises(SystemExit) as exited:
            main(["--version"])

        assert exited.value.code == 0
        assert capsys.readouterr().out.strip() == f"doclife {version('doclife')}"

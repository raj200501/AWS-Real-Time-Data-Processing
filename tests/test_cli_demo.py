from rtap.cli import main


def test_cli_demo_runs(monkeypatch):
    monkeypatch.setenv("USE_FAKE_AWS", "1")
    exit_code = main(["demo", "--events", "3"])
    assert exit_code == 0

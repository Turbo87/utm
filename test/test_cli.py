from pathlib import Path
import subprocess
import sys
import sysconfig

import pytest


@pytest.fixture(params=["console", "entry_point", "module"])
def cli_command(request):
    if request.param == "module":
        return [sys.executable, "-m", "utm.cli"]
    if request.param == "entry_point":
        return [sys.executable, "-c", (
            "from importlib.metadata import entry_points; "
            "entry, = entry_points(group='console_scripts', name='utm-converter'); "
            "entry.load()()"
        )]
    executable = "utm-converter.exe" if sys.platform == "win32" else "utm-converter"
    return [str(Path(sysconfig.get_path("scripts")) / executable)]


def run_cli(command, cwd, *args):
    # Keep imports and entry point discovery outside the source tree.
    result = subprocess.run(
        [*command, *args], cwd=cwd, capture_output=True, text=True, check=True
    )
    assert result.stderr == ""
    return result.stdout


def test_help(cli_command, tmp_path):
    output = run_cli(cli_command, tmp_path, "--help")
    assert "usage:" in output
    assert "{latlon,utm}" in output


def test_latlon(cli_command, tmp_path):
    output = run_cli(cli_command, tmp_path, "latlon", "51.2", "7.5")
    easting, northing, zone_number, zone_letter = output.strip().split(",")
    assert (float(easting), float(northing)) == pytest.approx(
        (395201.3103811303, 5673135.241182375), abs=0.01
    )
    assert (zone_number, zone_letter) == ("32", "U")


def test_utm(cli_command, tmp_path):
    output = run_cli(cli_command, tmp_path, "utm", "340000", "5710000", "32", "U")
    latitude, longitude = output.strip().split(",")
    assert (float(latitude), float(longitude)) == pytest.approx(
        (51.51843, 6.69388), abs=0.00001
    )


def test_missing_command(cli_command, tmp_path):
    result = subprocess.run(
        cli_command, cwd=tmp_path, capture_output=True, text=True, check=False
    )
    assert result.returncode == 2
    assert "usage:" in result.stderr
    assert "Traceback" not in result.stderr

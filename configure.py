# PsySymTrack
# Psychiatric symptom tracker with basic analysis
# Copyright (C) 2026 Nikita Serba. All rights reserved
# https://github.com/sandsbit/PsySymTrack
#
# PsySymTrack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# PsySymTrack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PsySymTrack. If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
import subprocess
import sys
import tomllib
from pathlib import Path

if __name__ == "__main__":
    if os.name == 'nt':
        print("This script is only for Unix-like operating systems. For Windows see 'build.bat' and 'package.bat'")
        sys.exit(1)

    # -- Parse project toml ---

    with open("pyproject.toml", "rb") as f:
        toml = tomllib.load(f)

    app_name: str = toml['project']['name']
    app_version: str = toml['project']['version']
    app_description: str = toml['project']['description']

    requires_py: str = toml['project']['requires-python']
    dependencies: list[str] = toml['project']['dependencies']

    # -- Parse command line arguments --

    parser = argparse.ArgumentParser(prog=app_name+app_version, description=app_description)
    parser.add_argument(
        "--pyexe",
        nargs=1,
        type=str,
        default=sys.executable,
        help="Python executable to use (default - use current)"
    )
    default_prefix = "/opt/" + app_name.lower().replace(" ", "_") + "/"
    parser.add_argument(
        "--prefix",
        nargs=1,
        type=str,
        default=default_prefix,
        help=f"Installation place for 'make install' (and deb/rpm) (default - {default_prefix})"
    )
    args = parser.parse_args()

    # -- Check configure.py dependencies

    try:
        # noinspection unused-imports
        from packaging import version
    except ImportError:
        print("Packaging module is required for this script. Try installing it with 'pip3 install packaging'")
        sys.exit(1)

    # -- Check python --

    pyexec = args.pyexe
    version_given = sys.version.split(' ')[0]
    if pyexec != sys.executable:
        pyexec_path = Path(pyexec)
        if not pyexec_path.exists():
            print("Invalid python executable: file does not exist: " + pyexec)
            sys.exit(1)
        if not pyexec_path.is_file():
            print("Invalid python executable: not a file: " + pyexec)
            sys.exit(1)

        print("New python executable is set. Checking version...", end='')
        py_proc = subprocess.run(
            [pyexec, "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if py_proc.returncode != 0:
            print("\n Python executable failed with exit code:", py_proc.returncode)
            sys.exit(1)
        if "Python" not in py_proc.stdout:
            print("\n Failed. Invalid python executable: invalid output.")
            sys.exit(1)
        version_given = py_proc.stdout.replace("Python ", "").strip()
        print(version_given)

    if ">=" not in requires_py:
        print("Invalid required python version format. Only >= identifier is supported. Check pyproject.toml.")
        sys.exit(1)
    requires_py = requires_py.replace(">=", "").strip()
    if ">" in requires_py or "<" in requires_py or "=" in requires_py:
        print("Invalid required python version format. Only >= identifier is supported. Check pyproject.toml.")
        sys.exit(1)

    if version.parse(version_given) < version.parse(requires_py):
        print(f"Incompatible python version was given. Requires Python {requires_py} or newer.")
        sys.exit(1)

    # -- Check dependencies --

    req_file = Path("requirements.txt")
    for dep in dependencies:
        req_file.write_text(dep + "\n")

    pip_proc = subprocess.run(
        [pyexec, "-m", "pip", "freeze", "-r", "requirements.tmp"],
        capture_output=True,
        text=True,
        check=False
    )
    req_file.unlink()
    if pip_proc.stderr.strip() != '':
        print("ERROR: not all dependencies are satisfied. Missing ones are listed below:")
        print(pip_proc.stderr)
        sys.exit(1)

    # -- Prepare makefile --

    makefile_text = (Path(__file__).resolve().parent / "Makefile.in").read_text(encoding='utf-8')

    makefile_text = makefile_text.replace("$$APPNAME$$", app_name)
    makefile_text = makefile_text.replace("$$VERSION$$", app_version)
    makefile_text = makefile_text.replace("$$FULLAPPNAME$$", '"' + app_name + ' ' + app_version + '"')
    makefile_text = makefile_text.replace("$$PYEXEC$$", pyexec)
    makefile_text = makefile_text.replace("$$PREFIX$$", args.prefix)
    makefile_text = makefile_text.replace("$$FPREFIX$$", app_name + "-v" + app_version)
    makefile_text = makefile_text.replace("    ", "\t")

    if sys.platform != "darwin":
        makefile_text = (makefile_text[0:makefile_text.index("$$START_MACOS1$$")] +
                         makefile_text[makefile_text.index("$$END_MACOS1$$") + len("$$END_MACOS1$$"):])
    else:
        makefile_text = makefile_text.replace("$$START_MACOS1$$", "")
        makefile_text = makefile_text.replace("$$END_MACOS1$$", "")

    # -- Check tools for make check --

    pip_proc = subprocess.run(
        [pyexec, "-m", "pip", "list"],
        capture_output=True,
        text=True,
        check=False
    )
    if pip_proc.returncode != 0:
        print(f"Pip returned with non-zero code {pip_proc.returncode}")
        sys.exit(1)
    if "ruff" in pip_proc.stdout or "mypy" in pip_proc.stdout:
        makefile_text += "\ncheck:\n"
    if "ruff" in pip_proc.stdout:
        makefile_text += "\t$(PYEXEC) -m ruff check src\n"
    if "mypy" in pip_proc.stdout:
        makefile_text += "\t$(PYEXEC) -m mypy --disallow-untyped-defs src\n"


    # Safe makefile
    with open("Makefile", "w") as f:
        f.write(makefile_text)

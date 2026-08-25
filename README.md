# PsySymTrack
Psychiatric symptom tracker with basic analysis.

PsySymTrack allows you to track a set of variables (both predefined and custom ones).
Based on them, it generates warnings or alerts, telling you something is off. Of course,
you can also see plots of your variables with basic statistics.

The project is new and is originally intended for personal use for a patient with bipolar disorder
and BPD. But I'd be glad to make the app useful for more people in the future. Feel free to make
an issue and describe what you want to see in the next release.
## Download
You can always download the latest version from the [releases](https://github.com/sandsbit/PsySymTrack/releases)
section on GitHub.

Supported platforms include:
- Windows
- macOS
- Linux (with deb and rpm packaging)

On other platforms (e.g., FreeBSD), the application may work if you compile it from source (see the section below).
## Features
- Tracking discrete (e.g., mood questionnaire) and continuous (i.e., weight) values
- Plotting and basic statistical analysis
- Adding your own values
- Built-in values for tracking mood, anxiety, quality of life, and BPD symptoms
- Metrics show trends across multiple variables, e.g., depression score
- Warnings show when values are continuously abnormal
- Alarms show important abnormalities, e.g., suspected mood episodes 
## How to use the app
When you first open the app, you will be asked to enter some basic information about yourself. Then you will be
redirected to the main screen:

![App's interface](https://i.ibb.co/QFjym06x/Bildschirmfoto-2026-08-25-um-10-24-03.png)

In section "B" you can choose the value you want to track. After clicking on it, you can change the value for a given
week in section "D", with the current week set as the default. Scale values (which require choosing one of several
options) are only set with an interval of one week. Physical values, like blood lithium level, can be set for any
given day. You can view the plot for saved values in section "C", along with some basic statistical analysis.
Coefficient of variation shows (in percentage) how much the data vary. Pearson correlation coefficient shows
whether a positive or negative trend is present in the selected time range (with -1 being steadily going down, 0 no
trend, and 1 steadily going up). Pearson coefficient value will be green if the trend is statistically significant 
or red if not. In section "A" you can add a new value or view warnings or alerts.

For any questions, you can contact the author (email is down below in the README) or, if you want to suggest a new feature or
believe you have found a bug, create an issue on GitHub.
## Issues and contribution
You can contribute to the project by suggesting new features or reporting bugs, or by helping implement new features or fix
reported bugs. Both new features and bugs are reported to our GitHub [issues](https://github.com/sandsbit/PsySymTrack/issues)
section.

Before creating an issue, keep the following in mind:
- **Search existing issues first** to avoid duplicates.
- **Use a clear, descriptive title** that summarizes the issue or feature.
- **Keep one issue focused on one problem or feature.**
- **Describe the problem and expected behavior**, not just the proposed solution.
- **For bugs, include steps to reproduce** and relevant system/version information.
- **For feature requests, explain the use case and why the feature would be useful.**
- **Attach screenshots or other relevant information** when appropriate.
- **Do not include sensitive personal or medical information.**
- **Consider whether the proposal fits PsySymTrack's purpose** and is worth its maintenance cost.
- **For medical/psychiatric features, provide a credible source or rationale** where applicable.
- **Be respectful and constructive.**

If you want to help the project as the developer, view our [CONTRIBUTING.md](https://github.com/sandsbit/PsySymTrack/blob/master/CONTRIBUTING.md)
file.
## Running tests & building from source
### Testing
Tests are located in the `tests` directory. Due to a known bug, you have to run each group of tests separately.<br>
On Windows, you can do that this way (replacing `<sub-dir>` with a directory name from `tests`):
```
cd src
python3 -m unittest discover ../tests/<sub-dir>
```
On Unix-like systems, you can use __make__:
```
python3 ./configure.py
make test
```
### Building
You can use this command (PyInstaller should be installed via __pip__):
```python3 -m PyInstaller --noconfirm main.spec```
The output will be located in the `dist/main` directory and can be used as a portable version.

On Unix-like systems, again you can use ___make__ to build and install the project:
```
python3 ./configure.py
make  # build
make test  # test (if needed)
make install  # install
make deb  # package as deb (if needed)
make rpm  # package as rpm (if needed)
```
By default, installation is made into `/opt/PsySymTrack`. The result of building will be in the `dist` and `out` directories,
consisting of a portable archive and .app application on macOS.
## Privacy 
All collected data is stored locally on your computer unencrypted and never leaves your computer. Support for encryption 
is planned.
## License
![GNU GPL v3 logo](https://www.gnu.org.cach3.com/graphics/gplv3-with-text-136x68.png)

PsySymTrack is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PsySymTrack is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PsySymTrack. If not, see <https://www.gnu.org/licenses/>.
## Links
* [Project releases](https://github.com/sandsbit/PsySymTrack/releases)
* [Latest stable source code](https://github.com/sandsbit/PsySymTrack/tree/master)
* [Latest non-stable source code](https://github.com/sandsbit/PsySymTrack/tree/develop)
* [Changelog](https://github.com/sandsbit/PsySymTrack/blob/master/CHANGELOG.md)
* [GNU GPL v3 text](https://github.com/sandsbit/PsySymTrack/blob/master/LICENSE)
* [Documentation](https://github.com/sandsbit/PsySymTrack/wiki)
* [Report a bug](https://github.com/sandsbit/PsySymTrack/issues)
## Authors and copyright
Copyright © 2026 Nikita S., All Rights Reserved<br>
*For any questions contact <<nikitaserba@icloud.com>>*

**Project team:**
- Nikita Serba <<nikitaserba@icloud.com>>

**Contributors:**
<br>*None yet :(*

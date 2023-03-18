## K1Manager - A tool for transfering presets to the Kawai K1 models of synthesizers
Copyright (C) 2022-2023  Markus Sundström

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

### About:
This application is intended for use with the Kawai K1, K1M and K1R synthesizers and the supplementary preset collections released by Kawai. K1Manager allows single presets to be selected from the bank files and transferred to any memory slot, offering greater flexibility than bulk transferring the entire bank file.

### Prerequisites:
Python 3 with Pyjack and PyQT5 modules.
j2amidi_bridge may be needed to allow passing SysEx messages to ALSA ports.
The soundbanks released by Kawai, which at the time of writing can be obtained here: http://www.kawaius.com/Downloads/K-1/K1.ZIP

### Installation:
Clone repo and cd into folder.
Optionally place the downloaded bankfiles (*.syx) in the banks folder and then run

`make install`

to install to the default prefix /usr/local. The application can be installed in another directory by supplying the PREFIX variable:

`PREFIX=/opt make install`

### Usage:
Run K1Manager.sh from $PREFIX/bin. The application will load any bank files found in $PREFIX/share/k1manager/banks as well as any bank files given as command line parameters. Select a preset from the list, and make desired settings for which memory slot to save in. Click the button to refresh midi ports and select desired port to send to from the dropdown then press send.

### Known issues:
The UI is not very pretty.
The application only handles single presets. The multi presets also available in the banks are not handled. It makes little sense to include them in the scope of the program, since they would to a high degree rely on the single patches from the same bank being available in their original memory slot.

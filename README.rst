This package is used to setup  a virtual environment 
for running mathy scripts in a jupyter qtconsole or spyder IDE. The intent
is to provide a quick setup for these tools, for a calcultor-like setting.

It creates a virtual environment, downloads the Scipy stack, Qt, and Spyder,
and creates shortcuts that run the Jupyter qtconsole or Spyder inside this environment.

Only compatible with Python versions greater than 3.3. 'python' and 'pip'
must be exposed to your system path. ('python3' and 'pip3' if using Linux.)

To by default, functions like sin, cos etc, and constants like pi and i will be tied
to numerical (ie numpy) funcs and constants. To switch, run 'from sym import *'; 
they will then by tied to Sympy. To revert, run 'from num import *'.

Installation instructions for Windows:
--------------------------------------
-Download or clone the repo. 
-Run the powershell script setup.ps1 under the windows subdirectory.
(You can run it by right clicking, and selecting 'Run with Powershell'. )

-You should now have shortcuts on your desktop for Jupyter qtconsole and Spyder, 
inside their own venv with the Scipy stack. Place these where you'd like 
(pin to Start etc).
If you'd like to regenerate the shortcuts later or if you change the virtual env's
directory, run create_shortcuts.ps1.

Note: If the shortcut doesn't launch, you may need to run the command:
Set-ExecutionPolicy Unrestricted
while running Powershell as an administrator.


Installation instructions for Linux:
------------------------------------
-Run the shell script setup.sh under the linux subdirectory.
(ie executing ./linux/setup.sh in a terminal)
-Edit the .desktop entries in the linux subdirectory to refer to the hard-coded icon
and executable paths here.

Note: Some Linux distros like Ubuntu do not include pip and virtual environment
support by default, despite them being built into python. You may install them with
the commands 'sudo apt install python-pip3' and 'sudo apt install 'python3-venv' respectively.
These must be setup first, or the setup will fail.

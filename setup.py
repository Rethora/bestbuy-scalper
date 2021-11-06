import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"

include_files = ['assets/']

executables = [Executable("main.py", base=base, targetName="Best Buy Scalper", icon="assets/robot-head.ico")]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
        'include_files': include_files
    },
}

setup(
    name="Best Buy Scalper",
    options=options,
    version="1.0.0",
    description='This is a scalper for bestbuy.com',
    executables=executables
)

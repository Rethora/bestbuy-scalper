# Best Buy Scalper GUI Application
This application with a simple GUI allows you to scalp pretty much any product on [Best Buy](https://bestbuy.com).

## Building the project
```shell
$ cd root/directory/of/project
$ python3 -m venv venv
$ source venv/bin/activate or... $ venv\Scripts\Activate.ps1
$ py -m pip install -r requirements.txt
```

## Building the Executable

### Windows
In root directory of activated environment:
```shell
$ py setup.py build
```
Bundled output to "/build"

### Mac
In root directory of activated environment:
```shell
$ pyinstaller main.spec
```
Bundled output to "/dist"

##Usage on Linux
We won't actually bundle program, we will just run it through PYTHON3
- Build the project
- In the active environment, run the main.py entry file

```shell
$ py path/to/root/main.py
```
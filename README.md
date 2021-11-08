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

## Usage on Linux
We won't actually bundle program, we will just run it through PYTHON3
- Build the project
- In the active environment, run the main.py entry file

```shell
$ py path/to/root/main.py
```

## Installing the Application

### Windows
I used Inno Setup Compiler to package this application. This will default build to User\AppData\Local\Programs\BestBuyScalper and allow user to uninstall through "Add or remove programs".

### Mac
Drag Best Buy Scalper.app to applications folder or wherever desired.

## Important Notes
I had to edit the file at Lib\site-packages\selenium\webdriver\common\service.py in the environment to get application to run without opening a console window for geckodriver.exe for WindowsOS.  

Modified from:
```python
self.creationflags = 0
```
to:
```python
self.creationflags = 0x08000000
```

In method:  
```python
Service.__init__()
```
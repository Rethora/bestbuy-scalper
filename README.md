# Best Buy Scalper GUI Application
This application with a simple GUI allows you to scalp pretty much any product on [Best Buy](https://bestbuy.com).

## Building the project
```shell
$ cd root/directory/of/project
$ python3 -m venv venv
$ source venv/bin/activate or... $ venv\Scripts\Activate.ps1
$ pip install -r requirements.txt
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
- Make sure you have "Tkinter" installed on the distro you're using
- In the root directory of active environment, run the main.py entry file

```shell
$ python main.py
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

On Windows this application is bundled with python 3.10 and on macOS it is bundled with python 3.8.  
Unfortunately I couldn't easily figure out app instances on macOS. So, to launch multiple instances of the application users will have to open a terminal and open the app via:  
```shell
$ open -n path/to/app.app
```
or

1. navigate to folder location of .app
2. right-click
3. "Open New Terminal at Folder"
```shell
$ open -n .
```

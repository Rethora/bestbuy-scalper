import sys
import os
import tempfile

from classes.App import App

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    os.chdir(application_path)

    tmp_dir = tempfile.TemporaryDirectory()
    for path in ["errors", "purchased"]:
        os.mkdir(os.path.join(tmp_dir.name, path))

    app = App(tmp_dir=tmp_dir.name)

    try:
        app.mainloop()
    except Exception as exp:
        print(exp)
    finally:
        try:
            tmp_dir.cleanup()
        except Exception as exp:
            print(exp)

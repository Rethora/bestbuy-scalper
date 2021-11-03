import os
import tempfile

from classes.App import App

if __name__ == "__main__":
    tmp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
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

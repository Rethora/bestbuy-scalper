try:
    from tkinter import *
    from tkinter.ttk import Progressbar
    from tkinter import messagebox
    from tkinter import font as tkfont
except ImportError:
    from Tkinter import *
    from Tkinter.ttk import Progressbar
    from Tkinter import messagebox
    import Tkinter.font as tkfont
except Exception as e:
    print(e)
    quit()


import time
from datetime import datetime
import threading
import webbrowser
from os import listdir, name, getcwd
from os.path import isfile, join

from classes.frames.StartPage import StartPage
from classes.frames.LoginPage import LoginPage
from classes.frames.ConfirmPage import ConfirmPage
from classes.frames.WatchPage import WatchPage
from classes.frames.FinishPage import FinishPage
from classes.frames.HelpPage import HelpPage
from classes.frames.ErrorsPage import ErrorsPage
from classes.frames.PurchasedPage import PurchasedPage


class App(Tk):
    """My tkinter application"""

    def __init__(self, tmp_dir, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Best Buy Scalper")
        self.minsize(1000, 700)
        if name != "posix":
            icon = PhotoImage(file=join(getcwd(), "assets", "robot-head.png"))
            self.iconphoto(False, icon)

        "global window styles"
        self.bg_color = "white"
        self.fg_color = "black"
        self.accent_color = "grey"
        self.accent_fg_color = "white"

        "fonts"
        self.title_font = tkfont.Font(
            family="Helvetica", size=18, weight="bold", slant="roman"
        )
        self.body_font = tkfont.Font(family="Sans-Serif", size=11)
        self.button_font = tkfont.Font(
            family="Cursive", size=14, weight="bold")
        self.italic_font = tkfont.Font(family="Sans-Serif", slant="italic", size=10)
        self.md_font = tkfont.Font(family="Sans-Serif", size=5)

        "button style"
        self.button_width = 8
        self.button_padding = 10

        "menu bar"
        if name == "posix":
            win = self
            menu_bar = Menu(win)
            app_menu = Menu(menu_bar, name='apple')
            menu_bar.add_cascade(menu=app_menu)
            app_menu.add_command(label='Help', command=lambda: self.show_frame("HelpPage"))
            app_menu.add_separator()
            win['menu'] = menu_bar
        else:
            menu = Menu(
                self, fg=self.accent_fg_color, bg=self.accent_color, font=self.body_font
            )
            menu.add_command(
                label="Help",
                command=lambda: self.show_frame("HelpPage"),
            )
            Tk.config(self, menu=menu, bg=self.accent_fg_color)

        """the container is where we'll stack a bunch of frames on top of each other
        then the one we want visible will be raised above the others """
        container = Frame(self)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        "storage"
        self.frames = self.user_settings = {}
        self.drivers = self.test_drivers = []
        self.tmp_dir = tmp_dir
        self.err_dir = join(tmp_dir, "errors")
        self.pur_dir = join(tmp_dir, "purchased")

        "frames"
        for F in (
                StartPage,
                LoginPage,
                ConfirmPage,
                WatchPage,
                FinishPage,
                HelpPage,
                ErrorsPage,
                PurchasedPage
        ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.configure(bg=self.bg_color)
            self.frames[page_name] = frame

            """put all of the pages in the same location
            the one on the top of the stacking order will be the one that is visible."""
            frame.grid(row=0, column=0, sticky="nsew")

        "Set the starting frame of application"
        start_frame = self.prev_page = "StartPage"
        self.show_frame(start_frame)

        "states"
        self.loading = False

        "event listeners"
        self.bind("<Button-3>", lambda e: self.event_generate("<Control-v>"))

        "handle exit application"
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def get_curr_time(self):
        """get local time in string format"""
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def add_user_setting(self, key, value):
        """store user's settings in object"""
        self.user_settings[key] = value

    def get_user_setting(self, setting):
        """get a user's setting"""
        return self.user_settings[setting]

    def close_all_drivers(self, drivers=None):
        """delete drivers in drivers array, default App.drivers"""
        if drivers is None:
            drivers = self.drivers
        for driver in drivers:
            driver.quit()
        self.drivers = []

    def show_frame(self, frame_name=None, prev_option=False):
        """Show a frame for the given page name"""
        if prev_option:
            frame = self.frames[self.prev_page]
        else:
            frame = self.frames[frame_name]
            if frame_name != "HelpPage":
                self.prev_page = frame_name
        frame.tkraise()

    def frame_func(self, frame_name, method_name, args=None):
        """call exclusive method of the given frame"""
        frame = self.frames[frame_name]
        if args is None:
            getattr(frame, method_name)()
        else:
            getattr(frame, method_name)(args)

    def print_error(self, message):
        """shows message on error"""
        messagebox.showerror(title="Error", message=message,
                             icon="error", parent=self)

    def open_page(self, url):
        """Opens url in a new browser"""
        webbrowser.open_new(url)

    def start_thread(self, thread):
        """start a thread"""
        threading.Thread(target=getattr(self, thread), daemon=True).start()

    def loading_bar(self, frame):
        """loading bar that will be displayed on loading"""
        loader = Progressbar(frame, orient=HORIZONTAL)
        loader.pack(pady=(20, 0), padx=(350, 0))
        loader.start()
        while self.loading:
            time.sleep(.5)
        loader.stop()
        loader.pack_forget()

    def start_page_check_thread(self):
        """thread to run on check start page input"""
        frame = self.frames["StartPage"]
        self.loading = True
        threading.Thread(
            target=lambda: self.loading_bar(frame), daemon=True).start()
        self.frame_func("StartPage", "check_input")
        self.loading = False

    def login_page_check_thread(self):
        """thread to run on check login page input"""
        frame = self.frames["LoginPage"]
        self.loading = True
        threading.Thread(target=lambda: self.loading_bar(
            frame), daemon=True).start()
        self.frame_func("LoginPage", "check_input")
        self.loading = False

    def scalper_thread(self):
        """this is the thread that drives the scalper"""
        closed_drivers = []
        d = self.drivers[0]
        try:
            "use a single driver to check if item is in stock"
            try:
                while not d.check_stock():
                    self.frame_func("WatchPage", "redraw", False)
                    time.sleep(3)
                    d.refresh()
            except Exception as exp:
                d.take_screenshot(self.err_dir, name="watching")
                d.quit()
                closed_drivers.append(d)
                raise Exception(exp)

            "when in stock:"
            "redraw frame with info"
            self.frame_func("WatchPage", "redraw", True)

            "refresh all browsers except for one that was used to check"
            for driver in self.drivers:
                if driver != d:
                    driver.refresh()

            "add to cart for all drivers"
            closed_drivers = self._clean_drivers(closed_drivers)
            for driver in self.drivers:
                email = driver.get_user_prop("email")
                try:
                    driver.add_to_cart()
                except Exception as exp:
                    print("Error while adding product to cart for driver with email " +
                          email + ". Continuing to next driver...")
                    print(exp)
                    driver.take_screenshot(
                        self.err_dir,
                        name="add-to-cart-" + self._format_email(email)
                    )
                    driver.quit()
                    closed_drivers.append(driver)

            closed_drivers = self._clean_drivers(closed_drivers)
            "buy for all drivers that had product added to cart"
            for driver in self.drivers:
                email = driver.get_user_prop("email")
                try:
                    driver.buy_product()
                    driver.take_screenshot(
                        self.pur_dir,
                        name=self._format_email(email)
                    )
                    driver.quit()
                except Exception as exp:
                    print("Error while buying product for driver with email " +
                          driver.user_properties['email'] + ". Continuing to next driver...")
                    print(exp)
                    driver.take_screenshot(
                        self.err_dir,
                        name="buying_" + self._format_email(email)
                    )
                    driver.quit()
                    closed_drivers.append(driver)
        except Exception as exp:
            self.print_error("Something went wrong while scalping")
            print(exp)
        finally:
            self._clean_drivers(closed_drivers)
            self._write_my_files()
            self.frame_func("ErrorsPage", "draw_info", self.tmp_dir)
            self.frame_func("PurchasedPage", "draw_info", self.tmp_dir)
            self.frame_func("FinishPage", "draw_info")
            self.unbind("<Button-3>")
            self.bind("<Button-3>", lambda e: self.event_generate("<Control-c>"))
            self.show_frame("FinishPage")

    def _clean_drivers(self, closed):
        """Remove closed drivers from self"""
        for driver in closed:
            self.drivers.remove(driver)
        return []

    def _write_my_files(self):
        """Writes md files for pictures of purchased items/errors"""
        err_pics = [f for f in listdir(
            self.err_dir) if isfile(join(self.err_dir, f))]
        purchased_pics = [f for f in listdir(
            self.pur_dir) if isfile(join(self.pur_dir, f))]

        err_md = open(join(self.tmp_dir, "errors.md"), "x")
        err_md.write("### Errors\n")
        if len(err_pics) == 0:
            err_md.write("Nothing to show.")
        else:
            err_md.write("If the picture does not open, this is the file path on your computer.  \n")
            err_md.write("You can open it there. Once you close this app the images will be deleted.  \n")
            err_md.write("So if you would like to, leave this window open until you are done viewing/saving.  \n")
            err_md.write(
                "**The folder may be hidden. You will have to enable 'show hidden items' in file manager.**  \n  \n"
            )
            for f in err_pics:
                path = join(self.err_dir, f)
                string = "<sub>[{}]({})</sub>\n".format(path, path)
                err_md.write(string)
        err_md.close()

        purchased_md = open(join(self.tmp_dir, "purchased.md"), "x")
        purchased_md.write("### Purchased Items\n")
        if len(purchased_pics) == 0:
            purchased_md.write("Nothing to show.")
        else:
            purchased_md.write("If the picture does not open, this is the file path on your computer.  \n")
            purchased_md.write("You can open it there. Once you close this app the images will be deleted.  \n")
            purchased_md.write("So if you would like to, leave this window open until you are done viewing/saving.  \n")
            purchased_md.write(
                "The folder may be hidden. You will have to enable 'show hidden items' in file manager.  \n  \n"
            )
            for f in purchased_pics:
                path = join(self.pur_dir, f)
                string = "<sub>[{}]({})</sub>\n".format(path, path)
                purchased_md.write(string)
        purchased_md.close()

    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                for driver in self.test_drivers:
                    driver.quit()
                for driver in self.drivers:
                    driver.quit()
            except Exception as exp:
                print(exp)
                pass
            finally:
                self.destroy()

    @staticmethod
    def _format_email(email):
        email = email.lower().replace(".", "").replace(":", "").replace("/", "").replace("_", "")
        email = (email[:8] if len(email) > 8 else email)
        return email

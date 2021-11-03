try:
    from tkinter import *
except ImportError:
    from Tkinter import *
except Exception as e:
    print(e)
    quit()

from classes.Driver import Driver
from classes.myWidgets.Scrollable import Scrollable


class LoginPage(Frame):
    """frame for user to login and set settings"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.input = []
        self.drivers = []

        "info text"
        Label(
            self,
            text="Enter your Best Buy account login details. Logins will be validated but security code will not! "
                 "Make sure you correctly enter the appropriate security code for each account!",
            wraplength=650,
            font=controller.body_font,
            bg=controller.bg_color,
            fg=controller.fg_color,
        ).pack(pady=(40, 10))

        "scrollable widget with inputs for user's logins"
        frame = Frame(self)
        self.scrollable = Scrollable(
            frame,
            canvas_color=controller.bg_color,
        )
        self.scrollable.pack()
        frame.pack()

        "continue button"
        self.continue_btn = Button(
            self,
            text="Continue",
            font=controller.button_font,
            width=controller.button_width,
            bg=controller.accent_color,
            fg=controller.accent_fg_color,
            command=lambda: self.controller.start_thread(
                "login_page_check_thread")
        )
        self.continue_btn.bind(
            "<Return>", lambda e: self.controller.start_thread("login_page_check_thread"))
        self.continue_btn.pack_configure(side=RIGHT, padx=(10, 0))

        "back button"
        self.back_btn = Button(
            self,
            text="Back",
            font=controller.button_font,
            width=controller.button_width,
            bg=controller.accent_color,
            fg=controller.accent_fg_color,
            command=lambda: controller.show_frame("StartPage"),
        )
        self.back_btn.bind(
            "<Return>", lambda e: self.controller.show_frame("StartPage"))
        self.back_btn.pack_configure(side=RIGHT, padx=(0, 10))

    def check_input(self):
        """check that all user's settings and logins are valid"""
        try:
            self.continue_btn.config(state=DISABLED)
            self.back_btn.config(state=DISABLED)
            count = 0
            for user in self.input:
                count += 1
                for k, v in user.items():
                    if k in ["email", "password", "security_code"]:
                        if v.get() == "":
                            raise ValueError(
                                "Missing " + k +
                                " at login number " + str(count)
                            )
                        if k == "email" and "@" not in v.get():
                            raise ValueError(
                                "Invalid email at login number " + str(count)
                            )
                        if k == "security_code":
                            code = v.get()
                            if len(code) != 3 or not code.isdigit():
                                raise ValueError(
                                    "Invalid security code at login number "
                                    + str(count)
                                )

            "check login"
            count = 0
            for user in self.input:
                count += 1
                driver = Driver()
                self.drivers.append(driver)
                for k, v in user.items():
                    driver.add_user_prop(k, v.get())

                logged_in = driver.initial_login()

                if not logged_in:
                    raise ValueError(
                        "Wrong email or password at login with email: "
                        + user["email"].get()
                    )

            "store drivers with valid credentials"
            for driver in self.drivers:
                driver.get(self.controller.user_settings["url"])
                driver.set_cookies()
            self.controller.drivers = self.drivers
            self.controller.frame_func("ConfirmPage", "draw_info")
            self.controller.show_frame("ConfirmPage")

        except ValueError as exp:
            self.controller.close_all_drivers(self.drivers)
            self.controller.print_error(exp)

        except Exception as exp:
            print(exp)
            self.controller.close_all_drivers(self.drivers)
            self.controller.print_error(
                "Something went wrong, check all fields and try again. If you keep getting this error it is possible "
                "that this application is out of date. "
            )
        finally:
            self.drivers = []
            self.continue_btn.config(state=NORMAL)
            self.back_btn.config(state=NORMAL)

    def redraw(self):
        """delete all the container's children and redraw frame with appropriate number of login fields"""
        self.input = []
        container_children = self.scrollable.scrollable_frame.winfo_children()
        if len(container_children) > 0:
            for child in container_children:
                child.destroy()

        for i in range(self.controller.user_settings["num_products"]):
            sub_container = Frame(self.scrollable.scrollable_frame, pady=20,
                                  bg=self.controller.bg_color)

            "user input: email"
            email = StringVar()
            Label(
                sub_container,
                font=self.controller.body_font,
                text="Email:",
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=0, row=0, sticky=E)
            Entry(
                sub_container,
                font=self.controller.body_font,
                width=50,
                textvariable=email,
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=1, row=0)

            "user input: password"
            password = StringVar()
            Label(
                sub_container,
                font=self.controller.body_font,
                text="Password:",
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=0, row=1, sticky=E)
            Entry(
                sub_container,
                font=self.controller.body_font,
                show="*",
                width=50,
                textvariable=password,
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=1, row=1)

            "user input: card security code"
            security_code = StringVar()
            Label(
                sub_container,
                font=self.controller.body_font,
                text="Card Security Code:",
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=0, row=2, sticky=E)
            Entry(
                sub_container,
                font=self.controller.body_font,
                width=50,
                textvariable=security_code,
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=1, row=2)

            "user input: warranty option"
            warranty = BooleanVar()
            Label(
                sub_container,
                font=self.controller.body_font,
                text="Standard Warranty Option:",
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=0, row=3, sticky=E)
            Checkbutton(
                sub_container,
                font=self.controller.body_font,
                offvalue=False,
                onvalue=True,
                padx=0,
                pady=0,
                selectcolor="white",
                variable=warranty,
                bg=self.controller.bg_color,
                fg=self.controller.fg_color,
            ).grid(column=1, row=3, sticky=W)

            "append user's input to check"
            self.input.append(
                {
                    "email": email,
                    "password": password,
                    "security_code": security_code,
                    "warranty": warranty,
                }
            )
            "add widgets to a sub-container"
            sub_container.pack(padx=(150, 0))
        "update canvas scrollable widget"

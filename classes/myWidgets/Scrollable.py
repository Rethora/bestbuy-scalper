# try:
#     from tkinter import *
# except ImportError:
#     from Tkinter import *
# except Exception as e:
#     print(e)
#     quit()
#
#
# class Scrollable(Frame):
#     """
#     Make a frame scrollable with scrollbar on the right.
#     After adding or removing widgets to the scrollable frame,
#     call the update() method to refresh the scrollable area.
#     """
#
#     def __init__(
#         self,
#         frame,
#         sb_width=16,
#         sb_color="black",
#         canvas_width=950,
#         canvas_height=500,
#         canvas_color="white",
#         frame_color="white",
#     ):
#
#         scrollbar = Scrollbar(frame, width=sb_width, bg=sb_color)
#         scrollbar.pack(side=RIGHT, fill=Y)
#
#         self.canvas = Canvas(
#             frame,
#             yscrollcommand=scrollbar.set,
#             bg=canvas_color,
#             width=canvas_width,
#             height=canvas_height,
#             border=2,
#         )
#         self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
#
#         scrollbar.config(command=self.canvas.yview)
#
#         self.canvas.bind("<Configure>", self.__fill_canvas)
#
#         "base class initialization"
#         Frame.__init__(self, frame, bg=frame_color)
#
#         "assign this obj (the inner frame) to the windows item of the canvas"
#         self.windows_item = self.canvas.create_window(
#             0, 0, window=self, anchor=NW)
#
#     def __fill_canvas(self, event):
#         """Enlarge the windows item to the canvas width"""
#         canvas_width = event.width
#         self.canvas.itemconfig(self.windows_item, width=canvas_width)
#
#     def update(self):
#         """Update the canvas and the scrolling region"""
#         self.update_idletasks()

# try:
#     from tkinter import *
# except ImportError:
#     from Tkinter import *
# except Exception as e:
#     print(e)
#     quit()
#
#
# class Scrollable(Frame):
#     """
#     Make a frame scrollable with scrollbar on the right.
#     After adding or removing widgets to the scrollable frame,
#     call the update() method to refresh the scrollable area.
#     """
#
#     def __init__(
#         self,
#         frame,
#         sb_width=16,
#         sb_color="black",
#         canvas_width=950,
#         canvas_height=500,
#         canvas_color="white",
#         frame_color="white",
#     ):
#
#         scrollbar = Scrollbar(frame, width=sb_width, bg=sb_color)
#         scrollbar.pack(side=RIGHT, fill=Y)
#
#         self.canvas = Canvas(
#             frame,
#             yscrollcommand=scrollbar.set,
#             bg=canvas_color,
#             width=canvas_width,
#             height=canvas_height,
#             # border=2,
#         )
#         self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
#
#         scrollbar.config(command=self.canvas.yview)
#
#         self.canvas.bind("<Configure>", self.__fill_canvas)
#
#         "base class initialization"
#         Frame.__init__(self, self.canvas, bg=frame_color)
#
#         "assign this obj (the inner frame) to the windows item of the canvas"
#         self.windows_item = self.canvas.create_window(
#             0, 0, window=self, anchor=NW)
#
#         self.update()
#
#     def __fill_canvas(self, event):
#         """Enlarge the windows item to the canvas width"""
#         canvas_width = event.width
#         self.canvas.itemconfig(self.windows_item, width=canvas_width)
#
#     def update(self):
#         """Update the canvas and the scrolling region"""
#         self.update_idletasks()


# class Scrollable(Frame):
#     def __init__(self, master):
#         self.master = master
#
#         self.canvas = Canvas(master)
#         self.canvas.pack(side=LEFT)
#
#         scrollbar = Scrollbar(self.canvas, command=self.canvas.yview)
#         scrollbar.pack(side=LEFT, fill=Y)
#
#         self.canvas.configure(yscrollcommand=scrollbar.set)
#
#         self.canvas.bind("<Configure>", self.on_configure)
#
#         # Frame.__init__(self, self.canvas)
#
#         self.canvas.create_window((0, 0), window=master, anchor=NW)
#
#     def on_configure(self, event):
#         # update scrollregion after starting 'mainloop'
#         # when all widgets are in canvas
#         self.canvas.configure(scrollregion=self.canvas.bbox('all'))

import tkinter as tk
from tkinter import ttk


class Scrollable(ttk.Frame):
    def __init__(
            self,
            container,
            canvas_color="white",
            *args,
            **kwargs
                 ):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg=canvas_color, width=950, height=500, border=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

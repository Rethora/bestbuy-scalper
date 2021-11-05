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

        self.scrollable_frame = tk.Frame(canvas, bg=canvas_color)

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

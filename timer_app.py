import tkinter as tk
from tkinter import font
import math

BG = "#1a1a2e"
CARD = "#16213e"
GREEN = "#68d391"
RED = "#fc8181"
ORANGE = "#f6ad55"
GRAY = "#4a5568"
TEXT = "#e2e8f0"
MUTED = "#718096"

class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("タイマー")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.total = 0
        self.remaining = 0
        self._job = None
        self.running = False

        self._build()
        self._update_ring(0, 0)

    def _build(self):
        outer = tk.Frame(self, bg=BG, padx=30, pady=30)
        outer.pack()

        tk.Label(outer, text="T I M E R", bg=BG, fg=MUTED,
                 font=("Helvetica", 11, "bold"), letterSpacing=4).pack(pady=(0, 10))

        # Canvas for ring + time display
        self.canvas = tk.Canvas(outer, width=220, height=220,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()

        # Input row
        inp = tk.Frame(outer, bg=BG)
        inp.pack(pady=14)

        self.min_var = tk.StringVar(value="5")
        self.sec_var = tk.StringVar(value="0")

        for label, var, col in [("分", self.min_var, 0), ("秒", self.sec_var, 2)]:
            tk.Label(inp, text=label, bg=BG, fg=MUTED,
                     font=("Helvetica", 9)).grid(row=0, column=col, padx=4)
            e = tk.Entry(inp, textvariable=var, width=4, justify="center",
                         bg=CARD, fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Helvetica", 20),
                         highlightthickness=2, highlightbackground=GRAY,
                         highlightcolor=GREEN)
            e.grid(row=0, column=col + 1, padx=4) if col == 2 else e.grid(row=0, column=1, padx=4)

        self.min_entry = inp.grid_slaves(row=0, column=1)[0]
        self.sec_entry = inp.grid_slaves(row=0, column=3)[0]

        # Buttons
        btns = tk.Frame(outer, bg=BG)
        btns.pack()

        self.start_btn = self._btn(btns, "スタート", GREEN, "#1a1a2e", self._start)
        self.pause_btn = self._btn(btns, "一時停止", ORANGE, "#1a1a2e", self._pause, state="disabled")
        self._btn(btns, "リセット", GRAY, TEXT, self._reset)

        for i, b in enumerate(btns.winfo_children()):
            b.grid(row=0, column=i, padx=5)

        # Message
        self.msg_var = tk.StringVar()
        tk.Label(outer, textvariable=self.msg_var, bg=BG, fg=RED,
                 font=("Helvetica", 12, "bold")).pack(pady=(12, 0))

    def _btn(self, parent, text, bg, fg, cmd, state="normal"):
        b = tk.Button(parent, text=text, bg=bg, fg=fg, activebackground=bg,
                      activeforeground=fg, font=("Helvetica", 11, "bold"),
                      relief="flat", padx=16, pady=8, cursor="hand2",
                      command=cmd, state=state, bd=0)
        return b

    def _update_ring(self, remaining, total):
        c = self.canvas
        c.delete("all")
        cx, cy, r = 110, 110, 90
        W = 10

        # Track
        c.create_oval(cx-r, cy-r, cx+r, cy+r,
                      outline=CARD, width=W+4)
        c.create_oval(cx-r, cy-r, cx+r, cy+r,
                      outline="#2d3748", width=W)

        # Progress arc
        if total > 0 and remaining > 0:
            ratio = remaining / total
            extent = -360 * ratio
            color = GREEN if remaining > total * 0.2 else RED
            c.create_arc(cx-r, cy-r, cx+r, cy+r,
                         start=90, extent=extent,
                         style="arc", outline=color, width=W)

        # Time text
        m = remaining // 60
        s = remaining % 60
        time_str = f"{m:02d}:{s:02d}"
        color = GREEN if self.running else (RED if remaining == 0 and total > 0 else TEXT)
        c.create_text(cx, cy, text=time_str,
                      font=("Helvetica", 42, "bold"),
                      fill=color)

    def _start(self):
        if not self.running:
            if self.remaining == 0:
                try:
                    m = max(0, int(self.min_var.get() or 0))
                    s = max(0, min(59, int(self.sec_var.get() or 0)))
                except ValueError:
                    return
                self.total = m * 60 + s
                self.remaining = self.total
                if self.remaining == 0:
                    return

            self.msg_var.set("")
            self.running = True
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.min_entry.config(state="disabled")
            self.sec_entry.config(state="disabled")
            self._tick()

    def _tick(self):
        if self.remaining > 0:
            self._update_ring(self.remaining, self.total)
            self.remaining -= 1
            self._job = self.after(1000, self._tick)
        else:
            self._update_ring(0, self.total)
            self.running = False
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")
            self.msg_var.set("⏰ 時間です！")
            self.bell()

    def _pause(self):
        if self.running:
            if self._job:
                self.after_cancel(self._job)
                self._job = None
            self.running = False
            self.start_btn.config(text="再開", state="normal")
            self.pause_btn.config(state="disabled")
            self._update_ring(self.remaining, self.total)

    def _reset(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.running = False
        self.remaining = 0
        self.total = 0
        self.start_btn.config(text="スタート", state="normal")
        self.pause_btn.config(state="disabled")
        self.min_entry.config(state="normal")
        self.sec_entry.config(state="normal")
        self.msg_var.set("")
        self._update_ring(0, 0)

if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()

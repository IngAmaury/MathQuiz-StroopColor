import tkinter as tk
from tkinter import ttk
import re
# import platform


PROBLEMS = [
    "25 + 37 =",
    "120 – 48 =",
    "14 × 6 =",
    "300 + 450 =",
    "81−19 =",
    "275 + 368 – 142 =",
    "(45×12) – 250 =",
    "(320 − 178) + 645 =",
    "(72 × 15) – 630 =",
    "(500 + 625) − (275 + 350) =",
    "48 × 25 + 125 =",
    "(920 − 450) × 8 =",
    "1,200 + (340 × 6) – 850 =",
    "(125 × 41) − (75 × 32) =",
    "3,452 + 2,768 − 4,915 =",
]

def _sanitize(expr: str) -> str:
    return expr.replace('×','*').replace('−','-').replace('–','-').replace(',','').replace('=','')

def _eval_expr(expr: str) -> int:
    return int(eval(_sanitize(expr), {"__builtins__": None}, {}))

ANSWERS = [_eval_expr(p) for p in PROBLEMS]

class MathQuiz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prueba de matemáticas")
        self.minsize(620, 260)
        self.current_idx = 0

        # --- Pantalla inicial ---
        self.start_btn = ttk.Button(self, text="iniciar", command=self.start_quiz)
        self.start_btn.pack(expand=True)

        # --- Quiz ---
        self.main_frame = ttk.Frame(self)

        self.header = ttk.Label(self.main_frame, text="Prueba de matemáticas",
                                font=("Segoe UI", 20, "bold"))

        self.problem_var = tk.StringVar(value="")
        self.problem_lbl = ttk.Label(self.main_frame, textvariable=self.problem_var,
                                     font=("Segoe UI", 26, "bold"))  # << letra más grande

        vcmd = (self.register(self._validate_numeric), "%P")
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(self.main_frame, width=12, textvariable=self.answer_var,
                                      validate="key", validatecommand=vcmd)
        self.answer_entry.bind("<KeyRelease>", self.on_entry_change)
        self.answer_entry.bind("<Return>", self.on_entry_change)

        self.feedback_var = tk.StringVar(value="")
        self.feedback_lbl = ttk.Label(self.main_frame, textvariable=self.feedback_var,
                                      font=("Segoe UI Emoji", 20))

        # Contador inferior derecho
        self.remaining_var = tk.StringVar(value="")
        self.remaining_lbl = ttk.Label(self.main_frame, textvariable=self.remaining_var,
                                       font=("Segoe UI", 15))

        self.done_lbl = ttk.Label(self.main_frame, text="¡Completado !",
                                  font=("Segoe UI", 20, "bold"))

    def _validate_numeric(self, proposed: str) -> bool:
        return re.fullmatch(r"-?\d*", proposed) is not None

    def start_quiz(self):
        self.start_btn.pack_forget()
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Layout
        self.header.grid(row=0, column=0, columnspan=2, pady=(0, 12))
        # Menos separación: poco padding y SIN pesos en columnas
        self.problem_lbl.grid(row=1, column=0, sticky="w", padx=(0, 6))
        self.answer_entry.grid(row=1, column=1, sticky="e", padx=(0, 0))

        self.feedback_lbl.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="w")

        # fila “elástica” para empujar el contador hacia abajo
        self.main_frame.rowconfigure(2, weight=1)
        # columnas sin expansión para que no se separen
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=0)

        # Contador en esquina inferior derecha
        self.remaining_lbl.grid(row=3, column=1, sticky="se")

        self.show_problem(0)

    def show_problem(self, idx: int):
        self.current_idx = idx
        self.done_lbl.grid_forget()
        self.problem_var.set(PROBLEMS[idx])
        self.answer_var.set("")
        self.feedback_var.set("")
        self.answer_entry.state(["!disabled"])
        self.answer_entry.focus_set()
        self.update_remaining()

    def update_remaining(self):
        remaining = len(PROBLEMS) - self.current_idx
        self.remaining_var.set(f"Faltan: {remaining}")

    def on_entry_change(self, event=None):
        text = self.answer_var.get()
        if text in ("", "-", "+"):
            self.feedback_var.set("")
            return
        try:
            user_val = int(text)
        except ValueError:
            self.feedback_var.set("Incorrecto \U0001F641")
            return

        correct = ANSWERS[self.current_idx]
        if user_val == correct:
            self.feedback_var.set("Correcto \U0001F642")
            self.answer_entry.state(["disabled"])
            self.after(2000, self.next_problem)
        else:
            self.feedback_var.set("Incorrecto \U0001F641")

    def next_problem(self):
        nxt = self.current_idx + 1
        if nxt >= len(PROBLEMS):
            self.problem_var.set("")
            self.answer_var.set("")
            self.feedback_var.set("")
            self.answer_entry.grid_remove()
            self.problem_lbl.grid_remove()
            self.remaining_var.set("Faltan: 0")
            self.done_lbl.grid(row=1, column=0, columnspan=2, pady=(20, 0))
        else:
            self.show_problem(nxt)

if __name__ == "__main__":
    app = MathQuiz()
    app.mainloop()

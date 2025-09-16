import tkinter as tk
from tkinter import ttk
import re
from pathlib import Path
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


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
    return (expr.replace('×', '*')
                .replace('−', '-')
                .replace('–', '-')
                .replace(',', '')
                .replace('=', ''))

def _eval_expr(expr: str) -> int:
    return int(eval(_sanitize(expr), {"__builtins__": None}, {}))

ANSWERS = [_eval_expr(p) for p in PROBLEMS]


class MathQuiz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prueba de matemáticas")
        self.minsize(680, 300)
        self.current_idx = 0

        # Base dir (misma carpeta del script)
        try:
            self.base_dir = Path(__file__).resolve().parent
        except NameError:
            self.base_dir = Path.cwd()

        # --- Pantalla inicial ---
        self.start_btn = ttk.Button(self, text="iniciar", command=self.start_quiz)
        self.start_btn.pack(expand=True)

        # --- Quiz ---
        self.main_frame = ttk.Frame(self)

        self.header = ttk.Label(self.main_frame, text="Prueba de matemáticas",
                                font=("Segoe UI", 18, "bold"))

        self.problem_var = tk.StringVar(value="")
        self.problem_lbl = ttk.Label(self.main_frame, textvariable=self.problem_var,
                                     font=("Segoe UI", 22, "bold"))

        vcmd = (self.register(self._validate_numeric), "%P")
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(self.main_frame, width=12, textvariable=self.answer_var,
                                      validate="key", validatecommand=vcmd)
        self.answer_entry.bind("<KeyRelease>", self.on_entry_change)
        self.answer_entry.bind("<Return>", self.on_entry_change)

        self.feedback_var = tk.StringVar(value="")
        self.feedback_lbl = ttk.Label(self.main_frame, textvariable=self.feedback_var,
                                      font=("Segoe UI", 22, "bold"))

        # Contador inferior derecho
        self.remaining_var = tk.StringVar(value="")
        self.remaining_lbl = ttk.Label(self.main_frame, textvariable=self.remaining_var,
                                       font=("Segoe UI", 10))

        self.done_lbl = ttk.Label(self.main_frame, text="¡Completado !",
                                  font=("Segoe UI", 16, "bold"))

        # Botón para iniciar Stroop al terminar el quiz
        self.start_stroop_btn = ttk.Button(self.main_frame, text="Iniar Stroop",
                                           command=self.start_stroop)

        # --- Stroop ---
        self.stroop_frame = None
        self.stroop_trials = [
            ("1.webp", 15),
            ("2.jpg", 16),
            ("3.png", 18),
        ]
        self.current_trial_idx = 0
        self._timer_after_id = None
        self._current_photo = None  # referencia para no perder la imagen

    def _validate_numeric(self, proposed: str) -> bool:
        return re.fullmatch(r"-?\d*", proposed) is not None

    def start_quiz(self):
        self.start_btn.pack_forget()
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Layout
        self.header.grid(row=0, column=0, columnspan=2, pady=(0, 12))
        # poco padding y SIN pesos para que no se separen
        self.problem_lbl.grid(row=1, column=0, sticky="w", padx=(0, 6))
        self.answer_entry.grid(row=1, column=1, sticky="w", padx=(0, 0))

        self.feedback_lbl.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="w")

        # fila “elástica” para empujar el contador hacia abajo
        self.main_frame.rowconfigure(2, weight=1)
        # columnas sin expansión
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=0)

        # Contador en esquina inferior derecha
        self.remaining_lbl.grid(row=3, column=1, sticky="se")

        self.show_problem(0)

    def show_problem(self, idx: int):
        self.current_idx = idx
        self.done_lbl.grid_forget()
        self.start_stroop_btn.grid_forget()
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
            self.feedback_var.set("Incorrecto ):")
            return

        correct = ANSWERS[self.current_idx]
        if user_val == correct:
            self.feedback_var.set("Correcto 🙂")
            self.answer_entry.state(["disabled"])
            self.after(650, self.next_problem)
        else:
            self.feedback_var.set("Incorrecto ):")

    def next_problem(self):
        nxt = self.current_idx + 1
        if nxt >= len(PROBLEMS):
            # Fin del cuestionario
            self.problem_var.set("")
            self.answer_var.set("")
            self.feedback_var.set("")
            self.answer_entry.grid_remove()
            self.problem_lbl.grid_remove()
            self.remaining_var.set("Faltan: 0")
            self.done_lbl.grid(row=1, column=0, columnspan=2, pady=(12, 8))
            # Muestra botón "Iniar Stroop"
            self.start_stroop_btn.grid(row=2, column=0, columnspan=2, pady=(6, 0))
        else:
            self.show_problem(nxt)

    # ===================== Stroop =====================
    def build_stroop_ui(self):
        if self.stroop_frame is not None:
            return
        self.stroop_frame = ttk.Frame(self)

        self.stroop_title = ttk.Label(self.stroop_frame,
                                      text="Prueba Stroop (Color)",
                                      font=("Segoe UI", 18, "bold"))
        self.timer_var = tk.StringVar(value="")
        self.timer_label = ttk.Label(self.stroop_frame, textvariable=self.timer_var,
                                     font=("Segoe UI", 14, "bold"))

        self.image_label = ttk.Label(self.stroop_frame)

        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(self.stroop_frame, textvariable=self.status_var,
                                      font=("Segoe UI", 16, "bold"))

        self.next_trial_btn = ttk.Button(self.stroop_frame, text="siguiente",
                                         command=self.next_stroop_trial)

        # Layout
        self.stroop_title.grid(row=0, column=0, pady=(8, 10))
        self.timer_label.grid(row=1, column=0, pady=(0, 8))
        self.image_label.grid(row=2, column=0, pady=(0, 8))
        self.status_label.grid(row=3, column=0, pady=(8, 6))
        # botón se mostrará/ocultará según estado

        self.stroop_frame.rowconfigure(4, weight=1)
        self.stroop_frame.columnconfigure(0, weight=1)

    def start_stroop(self):
        # Oculta la UI del quiz y muestra la de Stroop
        self.main_frame.pack_forget()
        self.build_stroop_ui()
        self.stroop_frame.pack(fill="both", expand=True, padx=16, pady=16)
        self.current_trial_idx = 0
        self.show_stroop_trial(self.current_trial_idx)

    def load_image(self, filename: str, max_w=1000, max_h=700):
        path = (self.base_dir / filename).resolve()
        if not path.exists():
            raise FileNotFoundError(f"No se encontró la imagen: {path}")

        if PIL_AVAILABLE:
            img = Image.open(path)
            img.thumbnail((max_w, max_h), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            return photo
        else:
            # Fallback limitado (solo PNG/GIF suelen funcionar sin Pillow)
            if path.suffix.lower() not in (".png", ".gif"):
                raise RuntimeError(
                    f"Pillow no instalado: no puedo abrir {path.suffix.upper()}. "
                    "Instala 'Pillow' o usa PNG/GIF."
                )
            return tk.PhotoImage(file=str(path))

    def show_stroop_trial(self, idx: int):
        # Cancela timer previo si existía
        if self._timer_after_id:
            self.after_cancel(self._timer_after_id)
            self._timer_after_id = None

        self.status_var.set("")
        self.next_trial_btn.grid_forget()

        fname, duration = self.stroop_trials[idx]

        # Carga y muestra la imagen
        try:
            self._current_photo = self.load_image(fname)
            self.image_label.configure(image=self._current_photo)
        except Exception as e:
            self._current_photo = None
            self.image_label.configure(image="", text=str(e))

        # Inicia contador
        self._remaining_secs = int(duration)
        self.update_stroop_timer()

    def update_stroop_timer(self):
        self.timer_var.set(f"Tiempo: {self._remaining_secs} s")
        if self._remaining_secs <= 0:
            # Fin del trial
            # Quita la imagen y muestra el mensaje + botón siguiente
            self.image_label.configure(image="", text="")
            fin_msg = f"Fin de prueba {self.current_trial_idx + 1}"
            self.status_var.set(fin_msg)
            self.next_trial_btn.grid(row=4, column=0, pady=(6, 0))
            self._timer_after_id = None
        else:
            self._remaining_secs -= 1
            self._timer_after_id = self.after(1000, self.update_stroop_timer)

    def next_stroop_trial(self):
        # Cancela timer si por alguna razón sigue activo
        if self._timer_after_id:
            self.after_cancel(self._timer_after_id)
            self._timer_after_id = None

        self.current_trial_idx += 1
        if self.current_trial_idx >= len(self.stroop_trials):
            # Mensaje final
            self.timer_var.set("")
            self.image_label.configure(image="", text="")
            self.status_var.set("Fin de la prueba Stroop Color, Gracias por participar")
            self.next_trial_btn.grid_forget()
        else:
            self.show_stroop_trial(self.current_trial_idx)


if __name__ == "__main__":
    app = MathQuiz()
    app.mainloop()

# 🧮 Math Quiz + 🎯 Stroop Color Test (Tkinter) — Spanish UI
A lightweight desktop app built with Python and Tkinter that first runs a short Math Quiz (auto-validated numeric answers with “Correct 🙂 / Incorrect 🙁” feedback), and upon completion launches a timed Stroop Color sequence that displays images with a visible countdown and “Next” prompts between trials.

## 🛠 Features 
* Start → Math Quiz → Stroop flow in a single window.

* Numeric-only input, instant validation, and progression only on correct answers.

* Clear feedback messages in spanish.

* Stroop sequence: shows 1.webp (15s), 2.jpg (16s), 3.png (18s) with a countdown at the top, then per-trial “End of test” screens and a final thank-you message.

* Simple to customize (problems list, image files, and per-trial durations).

## 📌 Requirements
* Python 3.8+
* Tkinter
* Pillow for WEBP/JPG/PNG support:

## ✨ Getting started 
1. Place the script (app.py) and the images 1.webp, 2.jpg, 3.png in the same folder.
2. Install requirements.

Create and activate a virtual environment, then install dependencies.
**Windows / macOS**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS
source .venv/bin/activate

pip install -r requirements.txt
```
3. Run "app.py".

``` bash
python app.py

```

## 📑 Usage 
- Click the button "Iniciar" to begin the Math Quiz.
- Type your answer in the numeric box.
    - Correct → shows “Correcto 🙂” and advances automatically.
    - Incorrect → shows “Incorrecto 🙁” and waits for a new answer.

- When the quiz finishes, the app shows “¡Completado!” and a button with the label “Iniciar Stroop”.

- The Stroop sequence displays each image for its configured time with a live countdown. After each image, you’ll see the message end of the current test and a “siguiente” button to move on to the next test.

- After the last image, the app shows “Fin de la prueba Stroop Color, Gracias por participar”.

## ⚙ Configuration
- Math problems: edit de **PROBLEMS** list, e.g:
```python
PROBLEMS = [
    "25 + 37 =",
    "120 – 48 =",
    ...
]
```
> [!WARNING]
> Problem checking relies on _eval_expr() (below), which sanitizes symbols and auto-evaluates arithmetic expressions. If you add problems that can’t be auto-evaluated by this function, either extend _eval_expr() or disable auto-eval and provide ANSWERS manually.
```python
def _sanitize(expr: str) -> str:
    return (expr.replace('×','*').replace('−','-').replace('–','-')
                .replace(',','').replace('=',''))

def _eval_expr(expr: str) -> int:
    return int(eval(_sanitize(expr), {"__builtins__": None}, {}))

# Default (auto-eval):
ANSWERS = [_eval_expr(p) for p in PROBLEMS]

# Manual fallback (remove/disable the line above and define 1:1 with PROBLEMS):
# ANSWERS = [62, 72, 84, ...]
```
- Stroop trials (filename & duration): edit self.stroop_trials list, e.g.:
```python
self.stroop_trials = [
    ("1.webp", 15),
    ("2.jpg", 16),
    ("3.png", 18),
]
```
- Feedback font size / emojis: adjust the font used by the feedback Label, e.g.:
```python
self.feedback_lbl = ttk.Label(self.main_frame, textvariable=self.feedback_var,
font=("Segoe UI", 14, "bold"))
```
> [!NOTE]
> On Windows/Tk 8.6, color emojis in labels are limited.
## 📕 Language 
- Spanish-only UI. All labels, buttons, and feedback messages are in Spanish.
- The Stroop Color stimuli/prompt flow is also presented in Spanish.
## 🧾 License
This project is licensed under the **MIT License**.  
Copyright © 2025 Amaury Santiago Horta.
See the [LICENSE](LICENSE) file for details.

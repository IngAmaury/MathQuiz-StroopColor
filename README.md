# Math Quiz + Stroop Color Test (Tkinter) - — Spanish UI
A lightweight desktop app built with Python and Tkinter that first runs a short Math Quiz (auto-validated numeric answers with “Correct 🙂 / Incorrect 🙁” feedback), and upon completion launches a timed Stroop Color sequence that displays images with a visible countdown and “Next” prompts between trials.

## Features 
* Start → Math Quiz → Stroop flow in a single window.

* Numeric-only input, instant validation, and progression only on correct answers.

* Clear feedback messages in spanish (e.g.:“Correct 🙂 / Incorrect 🙁”).

* Stroop sequence: shows 1.webp (15s), 2.jpg (16s), 3.png (18s) with a countdown at the top, then per-trial “End of test” screens and a final thank-you message.

* Simple to customize (problems list, image files, and per-trial durations).

## Requirements
* Python 3.8+
* Tkinter
* Pillow for WEBP/JPG/PNG support:

## Getting started 
1. Place the script (app.py) and the images 1.webp, 2.jpg, 3.png in the same folder.
2. Install Pillow (see above).
3. Run

``` bash
python app.py

```

## Usage 
- Click "Iniciar" to begin the Math Quiz
- Type your answer in the numeric box.
    - Correct → shows “Correct 🙂” and advances automatically.
    - Incorrect → shows “Incorrect 🙁” and waits for a new answer.

- When the quiz finishes, the app shows “¡Completado !” and a button “Iniar Stroop”.

- The Stroop sequence displays each image for its configured time with a live countdown. After each image, you’ll see “End of test X” and a “siguiente” button.

- After the last image, the app shows “Fin de la prueba Stroop Color, Gracias por participar”.

## Configuration
- Math problems: edit de **PROBLEMS** list.
- Stroop trials (filename & duration): edit self.stroop_trials list, e.g.:
```python
self.stroop_trials = [
    ("1.webp", 15),
    ("2.jpg", 16),
    ("3.png", 18),
]
```
- Feedback font size / emojis: adjust the font used by the feedback Label. On Windows/Tk 8.6, color emojis in labels are limited.

## License

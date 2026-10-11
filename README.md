# 🧮 FX Scientific Pro - Keyboard-First Calculator

A sleek, high-precision scientific calculator web application built with **Python**, **Streamlit**, and **`uv`**.

Engineered for seamless physical keyboard workflow: continuous typing without mouse intervention, permanent blinking cursor, instant evaluation, smart token deletion, calculation history tape, audio haptics, function graphing, and scientific constant reference.

---

## 🚀 Quick Start with `uv`

### 1. Run the application
```bash
uv run streamlit run app.py
```

Open your browser to `http://127.0.0.1:8501`.

### 2. Run unit tests
```bash
uv run pytest
```

---

## ⌨️ Physical Keyboard Controls

You can type calculations immediately upon loading the application. **You never need to click on the calculator screen to focus the input field.**

| Key | Action |
|---|---|
| **Enter** or **=** | Evaluate expression, display formatted result, record in history |
| **Backspace** | Smart delete: removes previous character or entire multi-character token (`sin(`, `sqrt(`, etc.) |
| **Escape (Esc)** | **All Clear (AC)**: Instantly clears expression, resets preview and errors |
| **0 – 9**, **.** | Number and decimal entry |
| **+**, **-**, **\***, **/** | Basic arithmetic operators (+, −, ×, ÷) |
| **^**, **%** | Power ($x^y$) and modulo (%) |
| **(** and **)** | Parentheses grouping |
| **s** | Inserts `sin(` |
| **c** | Inserts `cos(` |
| **t** | Inserts `tan(` |
| **l** | Inserts `ln(` (natural logarithm) |
| **L** | Inserts `log(` (base-10 logarithm) |
| **p** | Inserts constant `π` (3.14159...) |
| **e** | Inserts constant `e` (2.71828...) |
| **r** or **v** | Inserts `sqrt(` ($\sqrt{x}$) |
| **d** | Toggles angle mode between **DEG** (Degrees) and **RAD** (Radians) |

---

## 🌟 Key Features

1. **Continuous Autofocus & Caret Persistence**:
   - The expression input remains continuously focused. Even when tapping on-screen buttons or viewing history, focus returns immediately with caret placed precisely after the inserted token.
2. **Comprehensive Scientific Functions**:
   - Trigonometry: `sin`, `cos`, `tan`, `asin`, `acos`, `atan` (respects DEG / RAD modes).
   - Hyperbolic: `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`.
   - Powers & Roots: $x^2$, $x^3$, $x^y$, $\sqrt{x}$, $\sqrt[3]{x}$, $10^x$, $e^x$.
   - Logarithms: $\ln(x)$, $\log_{10}(x)$, $\log_2(x)$.
   - Factorials ($n!$), absolute value ($|x|$), reciprocal ($1/x$), negation ($\pm$).
3. **Calculation Tape (History)**:
   - Expandable history drawer recording computations with timestamps.
   - Click any past expression or result to immediately paste it into your active input.
   - Stored in browser `localStorage`.
4. **Memory Registers**:
   - Memory Clear (`MC`), Memory Recall (`MR`), Memory Add (`M+`), Memory Subtract (`M-`) with active indicator badge.
5. **Tactile Audio Haptics**:
   - Optional mechanical switch audio feedback generated via Web Audio API synthesis (can be toggled on/off with 🔊 / 🔇 button).
6. **Function Grapher & Calculus Analyzer (Tab 2)**:
   - Interactive curve plotting for any mathematical function $f(x)$ with SymPy and NumPy.
   - Analytical computation of derivative $\frac{d}{dx}f(x)$ and indefinite integral $\int f(x) dx$.
7. **Scientific Constants & Unit Converter (Tab 3)**:
   - Searchable physics and math fundamental constants.
   - Fast conversion for Angles, Temperature, Length, and Energy.

---

## 🔒 Security & Code Quality

- Enforces strict localhost binding (`127.0.0.1:8501`).
- XSS-safe DOM manipulation: uses `textContent`, `setAttribute`, and `replaceChildren`.
- AST Shunting-Yard parser without unsafe `eval()`.
- Modern accessible modal dialogs without blocking native alerts.

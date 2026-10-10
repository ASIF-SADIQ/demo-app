import ast
import html
import math
import operator

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Orbit Scientific Calculator", page_icon="∑", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    :root { color-scheme: dark; }

    .stApp {
        background:
            radial-gradient(circle at 50% -20%, rgba(37, 99, 235, 0.16), transparent 55%),
            radial-gradient(circle at 100% 100%, rgba(14, 165, 233, 0.08), transparent 40%),
            #0b1018;
        color: #e5edf8;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    [data-testid="stHeader"] { background: rgba(11, 16, 24, 0.72); }
    [data-testid="stToolbar"] { color: #cbd5e1; }
    [data-testid="stMainBlockContainer"] { max-width: 680px; padding-top: 2rem; padding-bottom: 3rem; }
    h1, h2, h3, p, label { color: #e5edf8; }
    [data-testid="stAppViewContainer"] { background: transparent; }
    [data-testid="stSidebar"] { background: #101722; border-right: 1px solid #253244; }
    [data-testid="stStatusWidget"] { color: #cbd5e1; }

    .brand-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #263449;
        padding-bottom: 1rem;
    }
    .brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #f1f5f9;
        margin: 0;
    }
    .brand-subtitle {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #fb923c;
        margin-top: 0.2rem;
    }
    .designer-badge {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        background: rgba(37, 99, 235, 0.12);
        border: 1px solid rgba(96, 165, 250, 0.3);
        color: #93c5fd;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        letter-spacing: 0.05em;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(155deg, rgba(24, 34, 49, 0.98), rgba(15, 23, 34, 0.99));
        border: 1px solid #2e3c51;
        border-radius: 24px;
        box-shadow: 0 20px 55px rgba(0, 0, 0, 0.36), inset 0 1px 0 rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 1.5rem;
    }

    [data-testid="stTextInput"] input {
        background: #0b111b !important;
        color: #f8fafc !important;
        border: 1px solid #394a62 !important;
        border-radius: 14px;
        font: 500 clamp(1.2rem, 3.5vw, 1.6rem) 'DM Mono', monospace;
        min-height: 4.5rem;
        padding: 0 1.25rem;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.32);
        transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2), inset 0 2px 8px rgba(0, 0, 0, 0.32) !important;
    }
    [data-testid="stTextInput"] input::placeholder { color: #718096; }

    .answer {
        color: #93c5fd;
        font: 500 0.9rem 'DM Mono', monospace;
        text-align: right;
        min-height: 1.4rem;
        overflow-wrap: anywhere;
        letter-spacing: 0.02em;
    }

    .stButton button {
        min-height: 3.25rem;
        border: 1px solid #35445a;
        border-radius: 12px;
        background: linear-gradient(180deg, #263349, #1c2738);
        color: #e2eaf5;
        font: 600 0.9rem 'DM Mono', monospace;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 120ms ease;
    }
    .stButton button:hover {
        background: linear-gradient(180deg, #34445e, #26364c);
        border-color: #5a7395;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 7px 16px rgba(0, 0, 0, 0.3);
    }
    .stButton button:active {
        transform: translateY(1px);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    .stButton button:focus-visible {
        outline: 2px solid #93c5fd;
        outline-offset: 2px;
    }

    div[class*="st-key-calc-key-scientific"] button {
        background: linear-gradient(180deg, #202c3d, #182333);
        color: #b8c8dc;
        border-color: #2d3c51;
        font-size: 0.82rem;
    }
    div[class*="st-key-calc-key-operator"] button {
        background: linear-gradient(180deg, #253a56, #1b2c43);
        color: #a8d3ff;
        border-color: #3b5c83;
    }
    div[class*="st-key-calc-key-utility"] button {
        background: linear-gradient(180deg, #452d36, #35232c);
        color: #ffb4bd;
        border-color: #70404d;
    }
    div[class*="st-key-calc-key-equals"] button {
        background: linear-gradient(180deg, #3b82f6, #2563eb);
        color: #ffffff;
        border-color: #60a5fa;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 5px 18px rgba(37, 99, 235, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    div[class*="st-key-calc-key-equals"] button:hover {
        background: linear-gradient(180deg, #3b82f6, #2563eb);
        color: #ffffff;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
    }

    div[data-testid="stRadio"] label {
        font-size: 0.82rem;
        font-family: 'DM Mono', monospace;
        color: #bac8da;
    }
    
    .stCaption {
        color: #9aaac0;
        font-size: 0.8rem;
    }
    
    hr {
        border-color: #2e3c51;
    }

    [data-testid="stExpander"] {
        background: #121b28;
        border: 1px solid #2e3c51;
        border-radius: 12px;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p { color: #dbe7f5; }
    [data-testid="stAlert"] {
        background: #321d26;
        border: 1px solid #713846;
        color: #ffd0d5;
    }
    [data-testid="stAlert"] p { color: #ffd0d5; }
    [data-testid="stRadio"] [role="radiogroup"] { gap: 0.5rem; }
    [data-testid="stRadio"] [role="radio"] p { color: #bac8da; }

    @media (max-width: 520px) {
        [data-testid="stMainBlockContainer"] { padding: 1rem 0.5rem; }
        div[data-testid="stVerticalBlockBorderWrapper"] > div { padding: 1rem; }
        .stButton button { min-height: 2.8rem; border-radius: 10px; font-size: 0.8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _trig(function, inverse=False):
    def apply(value):
        angle_mode = st.session_state.get("angle_mode", "RAD")
        if inverse:
            result = function(value)
            return math.degrees(result) if angle_mode == "DEG" else result
        argument = math.radians(value) if angle_mode == "DEG" else value
        return function(argument)

    return apply


def _factorial(value):
    if not isinstance(value, (int, float)) or not float(value).is_integer() or value < 0:
        raise ValueError("Factorial requires a non-negative integer")
    return math.factorial(int(value))


def _evaluate(expression):
    if not expression.strip():
        raise ValueError("Enter an expression first")
    if len(expression) > 240:
        raise ValueError("Expression is too long")

    normalized = (
        expression.replace("π", "pi")
        .replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace("^", "**")
    )
    tree = ast.parse(normalized, mode="eval")
    binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    unary_operators = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    functions = {
        "sin": _trig(math.sin),
        "cos": _trig(math.cos),
        "tan": _trig(math.tan),
        "asin": _trig(math.asin, inverse=True),
        "acos": _trig(math.acos, inverse=True),
        "atan": _trig(math.atan, inverse=True),
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "sqrt": math.sqrt,
        "ln": math.log,
        "log": math.log10,
        "log2": math.log2,
        "exp": math.exp,
        "abs": abs,
        "fact": _factorial,
        "floor": math.floor,
        "ceil": math.ceil,
        "degrees": math.degrees,
        "radians": math.radians,
    }
    constants = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
        "ans": st.session_state.get("answer_value", 0),
    }

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id in constants:
            return constants[node.id]
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_operators:
            return unary_operators[type(node.op)](visit(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in binary_operators:
            if isinstance(node.op, ast.Pow):
                exponent = visit(node.right)
                if abs(exponent) > 1000:
                    raise ValueError("Exponent is too large")
                value = binary_operators[type(node.op)](visit(node.left), exponent)
            else:
                value = binary_operators[type(node.op)](visit(node.left), visit(node.right))
            return value
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in functions:
            if node.keywords or len(node.args) != 1:
                raise ValueError("Functions take exactly one argument")
            return functions[node.func.id](visit(node.args[0]))
        raise ValueError("That expression is not supported")

    result = visit(tree)
    if isinstance(result, complex) or not isinstance(result, (int, float)):
        raise ValueError("Result is not a real number")
    if isinstance(result, int):
        if result.bit_length() > 4096:
            raise ValueError("Result is too large")
        return result
    if not math.isfinite(result):
        raise ValueError("Result is not finite")
    return result


def _display_number(value):
    if isinstance(value, int):
        return str(value)
    if value.is_integer() and abs(value) < 1e15:
        return str(int(value))
    return format(value, ".12g")


def _complete_parentheses(expression):
    open_parentheses = expression.count("(")
    close_parentheses = expression.count(")")
    if open_parentheses > close_parentheses:
        return expression + ")" * (open_parentheses - close_parentheses)
    return expression


def _calculate():
    expression = _complete_parentheses(st.session_state.get("expression", ""))
    try:
        value = _evaluate(expression)
        result = _display_number(value)
        st.session_state.previous_expression = expression
        st.session_state.answer_value = value
        st.session_state.last_result = result
        st.session_state.expression = result
        st.session_state.calculation_complete = True
        st.session_state.calculation_error = ""
        st.session_state.history.insert(0, (expression, result))
        del st.session_state.history[8:]
    except (ArithmeticError, SyntaxError, ValueError, TypeError, OverflowError) as error:
        st.session_state.calculation_complete = False
        st.session_state.calculation_error = str(error) or "Unable to calculate this expression"


def _clear():
    st.session_state.expression = ""
    st.session_state.answer_value = 0
    st.session_state.previous_expression = ""
    st.session_state.last_result = ""
    st.session_state.calculation_complete = False
    st.session_state.calculation_error = ""


def _press(token):
    if token == "AC":
        _clear()
    elif token == "⌫":
        st.session_state.expression = st.session_state.get("expression", "")[:-1]
        st.session_state.calculation_complete = False
        st.session_state.previous_expression = ""
        st.session_state.last_result = ""
        st.session_state.calculation_error = ""
    elif token == "=":
        _calculate()
    else:
        expression = st.session_state.get("expression", "")
        if st.session_state.get("calculation_complete", False):
            if token in ("+", "−", "×", "÷", "^", "%"):
                expression = st.session_state.last_result
            else:
                expression = ""
                st.session_state.previous_expression = ""
                st.session_state.last_result = ""
        st.session_state.expression = expression + ("ans" if token == "Ans" else token)
        st.session_state.calculation_complete = False
        st.session_state.calculation_error = ""


for key, initial_value in (
    ("expression", ""),
    ("answer_value", 0),
    ("previous_expression", ""),
    ("last_result", ""),
    ("calculation_complete", False),
    ("calculation_error", ""),
    ("history", []),
    ("angle_mode", "RAD"),
):
    if key not in st.session_state:
        st.session_state[key] = initial_value

# Brand Header Block featuring ASIF SADIQ
st.markdown(
    """
    <div class="brand-container">
        <div>
            <h1 class="brand-title">Orbit Scientific</h1>
            <div class="brand-subtitle">Precision Computation System</div>
        </div>
        <div class="designer-badge">ASIF SADIQ</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    mode_col, result_col = st.columns([1, 2], vertical_alignment="center")
    with mode_col:
        st.radio("Angle mode", ["RAD", "DEG"], horizontal=True, key="angle_mode", label_visibility="collapsed")
    with result_col:
        if st.session_state.previous_expression and st.session_state.last_result:
            st.markdown(
                f'<div class="answer" data-result="{html.escape(st.session_state.last_result, quote=True)}" data-calculation-complete="true">{html.escape(st.session_state.previous_expression)} = {html.escape(st.session_state.last_result)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="answer" data-calculation-complete="false">&nbsp;</div>', unsafe_allow_html=True)

    st.text_input(
        "Expression",
        placeholder="Type expression, e.g. sin(30) + sqrt(16)",
        key="expression",
        on_change=_calculate,
        label_visibility="collapsed",
    )
    if st.session_state.calculation_error:
        st.error(st.session_state.calculation_error)
    else:
        st.caption("Keyboard shortcuts active: numbers, operators, Enter/=, Backspace, Esc.")

    st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
    keypad = [
        [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("ln", "ln("), ("log", "log(")],
        [("asin", "asin("), ("acos", "acos("), ("atan", "atan("), ("√", "sqrt("), ("π", "π")],
        [("sinh", "sinh("), ("cosh", "cosh("), ("tanh", "tanh("), ("e", "e"), ("^", "^")],
        [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "÷"), ("(", "(")],
        [("4", "4"), ("5", "5"), ("6", "6"), ("×", "×"), (")", ")")],
        [("1", "1"), ("2", "2"), ("3", "3"), ("−", "−"), ("+", "+")],
        [("0", "0"), (".", "."), ("Ans", "Ans"), ("%", "%"), ("!x", "fact(")],
        [("AC", "AC"), ("⌫", "⌫"), ("10ˣ", "10**("), ("=", "="), ("", "")],
    ]

    for row_index, row in enumerate(keypad):
        columns = st.columns(5, gap="small")
        for column_index, (column, (label, token)) in enumerate(zip(columns, row)):
            if label:
                if label == "=":
                    category = "equals"
                elif label in ("AC", "⌫"):
                    category = "utility"
                elif label in ("+", "−", "×", "÷", "^", "%", "(", ")"):
                    category = "operator"
                elif label.isdigit() or label == ".":
                    category = "number"
                else:
                    category = "scientific"
                column.button(
                    label,
                    key=f"calc-key-{category}-{row_index}-{column_index}",
                    on_click=_press,
                    args=(token,),
                    use_container_width=True,
                    type="primary" if label == "=" else "secondary",
                )

if st.session_state.history:
    st.divider()
    with st.expander("Recent calculations history"):
        for expression, result in st.session_state.history:
            st.markdown(f"`{html.escape(expression)}` = **{result}**")

components.html(
    """
    <script>
    const appWindow = window.parent;
    const appDocument = appWindow.document;
    const buttonTokens = {
        "sin": "sin(", "cos": "cos(", "tan": "tan(", "ln": "ln(", "log": "log(",
        "asin": "asin(", "acos": "acos(", "atan": "atan(", "√": "sqrt(", "π": "π",
        "sinh": "sinh(", "cosh": "cosh(", "tanh": "tanh(", "e": "e", "^": "^",
        "÷": "÷", "×": "×", "−": "−", "+": "+", "(": "(", ")": ")",
        "%": "%", "Ans": "ans", "!x": "fact(", "10ˣ": "10**(",
        "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
        "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", ".": "."
    };
    const keyButtonSelector = '[class*="st-key-calc-key-"] button';
    const inputSelector = '[data-testid="stTextInput"] input';
    const answerSelector = '.answer[data-calculation-complete="true"]';
    const operatorTokens = new Set(["+", "−", "×", "÷", "^", "%"]);
    const valueSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;

    function currentInput() {
        return appDocument.querySelector(inputSelector);
    }

    function setExpression(input, value) {
        valueSetter.call(input, value);
        input.dispatchEvent(new Event("input", { bubbles: true }));
    }

    function appendToken(token) {
        const input = currentInput();
        if (!input) return;
        let expression = input.value;
        const answer = appDocument.querySelector(answerSelector);
        const result = answer?.dataset.result;
        const isShowingResult = answer && result === expression;
        if (isShowingResult) {
            expression = operatorTokens.has(token) ? result : "";
        }
        setExpression(input, expression + token);
    }

    if (appWindow.__orbitCalculatorKeyHandler) {
        appDocument.removeEventListener("keydown", appWindow.__orbitCalculatorKeyHandler, true);
        appDocument.removeEventListener("click", appWindow.__orbitCalculatorClickHandler, true);
    }
    appWindow.__orbitCalculatorKeyHandler = function(event) {
        if (event.ctrlKey || event.metaKey || event.altKey) return;
        const input = currentInput();
        if (event.key === "Escape" || event.key === "Delete") {
            const clearButton = Array.from(appDocument.querySelectorAll(keyButtonSelector))
                .find((button) => button.textContent.trim() === "AC");
            if (clearButton) {
                event.preventDefault();
                event.stopPropagation();
                clearButton.click();
            }
            return;
        }
        if (event.key === "Enter" || event.key === "=") {
            if (input && event.target === input) return;
            const equalsButton = Array.from(appDocument.querySelectorAll(keyButtonSelector))
                .find((button) => button.textContent.trim() === "=");
            if (equalsButton) {
                event.preventDefault();
                event.stopPropagation();
                equalsButton.click();
            }
            return;
        }
        if (input && event.target === input) return;
        if (event.key === "Backspace") {
            if (!input) return;
            event.preventDefault();
            event.stopPropagation();
            setExpression(input, input.value.slice(0, -1));
            return;
        }
        const token = ({
            "-": "−", "*": "×", "/": "÷"
        })[event.key] || event.key;
        if (/^[0-9a-zA-Z.]$/.test(token) || ["+", "−", "×", "÷", "^", "%", "(", ")"].includes(token)) {
            event.preventDefault();
            event.stopPropagation();
            appendToken(token);
        }
    };
    appWindow.__orbitCalculatorClickHandler = function(event) {
        const button = event.target.closest(keyButtonSelector);
        if (!button) return;
        const label = button.textContent.trim();
        if (label === "=" || label === "AC") return;
        if (label === "⌫") {
            const input = currentInput();
            if (input) setExpression(input, input.value.slice(0, -1));
        } else if (buttonTokens[label]) {
            appendToken(buttonTokens[label]);
        } else {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
    };
    appDocument.addEventListener("keydown", appWindow.__orbitCalculatorKeyHandler, true);
    appDocument.addEventListener("click", appWindow.__orbitCalculatorClickHandler, true);
    </script>
    """,
    height=0,
)
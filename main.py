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
    
    :root { color-scheme: light; }

    .stApp {
        background: 
            radial-gradient(circle at 50% -20%, rgba(37, 99, 235, 0.08), transparent 55%),
            radial-gradient(circle at 100% 100%, rgba(14, 165, 233, 0.04), transparent 40%),
            #f8fafc;
        color: #87047;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMainBlockContainer"] { max-width: 680px; padding-top: 2rem; padding-bottom: 3rem; }

    /* Brand Header Styling */
    .brand-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        padding-bottom: 1rem;
    }
    .brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #867e7a;
        margin: 0;
    }
    .brand-subtitle {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #f4935e;
        margin-top: 0.2rem;
    }
    .designer-badge {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        background: rgba(37, 99, 235, 0.08);
        border: 1px solid rgba(37, 99, 235, 0.2);
        color: #5e8ef4;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        letter-spacing: 0.05em;
    }

    /* Calculator Main Container Wrapper */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(155deg, rgba(255, 255, 255, 0.95), rgba(241, 245, 249, 0.98));
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 24px;
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08), inset 0 1px 0 rgba(255, 255, 255, 1);
        backdrop-filter: blur(12px);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 1.5rem;
    }

    /* Display Screen Styling */
    .stTextInput input {
        background: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        font: 500 clamp(1.2rem, 3.5vw, 1.6rem) 'DM Mono', monospace;
        min-height: 4.5rem;
        padding: 0 1.25rem;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
        transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTextInput input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.02);
    }

    /* Result Preview Box */
    .answer {
        color: #2563eb;
        font: 500 0.9rem 'DM Mono', monospace;
        text-align: right;
        min-height: 1.4rem;
        overflow-wrap: anywhere;
        letter-spacing: 0.02em;
    }

    /* Base Button Styling */
    .stButton button {
        min-height: 3.25rem;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        background: linear-gradient(180deg, #ffffff, #f8fafc);
        color: #334155;
        font: 600 0.9rem 'DM Mono', monospace;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.03), inset 0 1px 0 rgba(255, 255, 255, 1);
        transition: all 120ms ease;
    }
    .stButton button:hover {
        background: linear-gradient(180deg, #f1f5f9, #e2e8f0);
        border-color: #cbd5e1;
        color: #0f172a;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.06);
    }
    .stButton button:active {
        transform: translateY(1px);
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    .stButton button:focus-visible {
        outline: 2px solid #2563eb;
        outline-offset: 2px;
    }

    /* Category Specific Key Styling */
    div[class*="st-key-calc-key-scientific"] button {
        background: #f1f5f9;
        color: #475569;
        border-color: #e2e8f0;
        font-size: 0.82rem;
    }
    div[class*="st-key-calc-key-operator"] button {
        background: linear-gradient(180deg, #eff6ff, #dbeafe);
        color: #1d4ed8;
        border-color: #bfdbfe;
    }
    div[class*="st-key-calc-key-utility"] button {
        background: linear-gradient(180deg, #fef2f2, #fee2e2);
        color: #dc2626;
        border-color: #fecaca;
    }
    div[class*="st-key-calc-key-equals"] button {
        background: linear-gradient(180deg, #2563eb, #1d4ed8);
        color: #ffffff;
        border-color: #3b82f6;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    div[class*="st-key-calc-key-equals"] button:hover {
        background: linear-gradient(180deg, #3b82f6, #2563eb);
        color: #ffffff;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
    }

    /* Radio button / angle mode styling */
    div[data-testid="stRadio"] label {
        font-size: 0.82rem;
        font-family: 'DM Mono', monospace;
        color: #475569;
    }
    
    .stCaption {
        color: #64748b;
        font-size: 0.8rem;
    }
    
    hr {
        border-color: #e2e8f0;
    }

    /* Responsive adjustments */
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
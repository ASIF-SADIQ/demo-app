import ast
import html
import math
import operator

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Orbit Scientific Calculator", page_icon="∑", layout="centered")

st.title("ASIF SADIQ")

st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
	:root { color-scheme: dark; }
	.stApp {
		background:
			radial-gradient(ellipse at 50% 0%, rgba(91, 130, 102, 0.16), transparent 42%),
			#101512;
		color: #eef4ef;
	}
	[data-testid="stHeader"] { background: transparent; }
	[data-testid="stMainBlockContainer"] { max-width: 720px; padding-top: 2.5rem; }
	h1, h2, h3, p, label { font-family: 'Manrope', sans-serif; }
	.eyebrow { color: #91b4a1; font: 500 0.76rem 'DM Mono', monospace; letter-spacing: 0.08em; text-transform: uppercase; }
	.stTextInput input {
		background: #111914; color: #f1f7f2; border: 1px solid #43554a;
		border-radius: 11px; font: 500 clamp(1.1rem, 4vw, 1.65rem) 'DM Mono', monospace; min-height: 4.2rem;
		box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.22);
	}
	.stTextInput input:focus { border-color: #b5e66d; box-shadow: 0 0 0 2px rgba(181, 230, 109, 0.28); }
	div[data-testid="stVerticalBlockBorderWrapper"] {
		background: linear-gradient(145deg, rgba(31, 42, 35, 0.96), rgba(20, 28, 23, 0.98));
		border: 1px solid #35443a;
		border-radius: 18px;
		box-shadow: 0 18px 50px rgba(0, 0, 0, 0.2);
	}
	div[data-testid="stVerticalBlockBorderWrapper"] > div {
		padding: 1.1rem 1.15rem 1.2rem;
	}
	.stButton button {
		min-height: 3.15rem; border: 1px solid #3a4a40; border-radius: 10px;
		background: linear-gradient(180deg, #29352d, #222c25); color: #e8efe9;
		font: 600 0.94rem 'DM Mono', monospace;
		box-shadow: 0 2px 0 #121a15, 0 5px 12px rgba(0, 0, 0, 0.12);
		transition: background 120ms ease, border-color 120ms ease, transform 120ms ease, box-shadow 120ms ease;
	}
	.stButton button:hover {
		background: linear-gradient(180deg, #34443a, #29372e);
		border-color: #809687; color: #fff; transform: translateY(-1px);
		box-shadow: 0 3px 0 #121a15, 0 7px 16px rgba(0, 0, 0, 0.2);
	}
	.stButton button:active { transform: translateY(1px); box-shadow: 0 1px 0 #121a15; }
	.stButton button:focus-visible { outline: 2px solid #c4f47b; outline-offset: 2px; }
	div[class*="st-key-calc-key-scientific"] button {
		background: #202b24; color: #b9cbbf; border-color: #34443a;
	}
	div[class*="st-key-calc-key-operator"] button {
		background: linear-gradient(180deg, #35493c, #2a3a30);
		color: #c9eea0; border-color: #49624f;
	}
	div[class*="st-key-calc-key-utility"] button {
		background: linear-gradient(180deg, #493532, #382926);
		color: #ffc2a8; border-color: #63453d;
	}
	div[class*="st-key-calc-key-equals"] button {
		background: linear-gradient(180deg, #c9f381, #a8d95d);
		color: #172111; border-color: #d9ff9a;
		font-size: 1.15rem;
		box-shadow: 0 2px 0 #607b35, 0 6px 14px rgba(181, 230, 109, 0.12);
	}
	div[class*="st-key-calc-key-equals"] button:hover {
		background: linear-gradient(180deg, #d8ff9b, #b9eb6e);
		color: #111a0d; border-color: #e3ffb2;
	}
	div[data-testid="stRadio"] label { font-size: 0.88rem; }
	.answer {
		color: #b5e66d; font: 500 0.88rem 'DM Mono', monospace;
		text-align: right; min-height: 1.35rem; overflow-wrap: anywhere;
	}
	.stCaption { color: #9aaba0; }
	hr { border-color: #344139; }
	@media (max-width: 520px) {
		[data-testid="stMainBlockContainer"] { padding: 1.25rem 0.75rem 2rem; }
		div[data-testid="stVerticalBlockBorderWrapper"] > div { padding: 0.8rem; }
		.stButton button { min-height: 2.75rem; border-radius: 8px; font-size: 0.82rem; }
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
	elif token == "=" :
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


st.markdown('<div class="eyebrow">ORBIT / SCIENTIFIC</div>', unsafe_allow_html=True)
st.title("Calculator")
st.caption("A precise workspace for everyday calculations and deeper explorations.")

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
		placeholder="Type an expression, e.g. sin(30) + sqrt(16)",
		key="expression",
		on_change=_calculate,
		label_visibility="collapsed",
	)
	if st.session_state.calculation_error:
		st.error(st.session_state.calculation_error)
	else:
		st.caption("Use the keypad or keyboard: 0–9, operators, Enter/= to calculate, Backspace to delete, and Esc to clear.")

	st.markdown("<div style='height: 0.35rem'></div>", unsafe_allow_html=True)
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
	with st.expander("Recent calculations"):
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
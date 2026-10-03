import ast
import html
import math
import operator

import streamlit as st


st.set_page_config(page_title="Orbit Scientific Calculator", page_icon="∑", layout="centered")

st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
	:root { color-scheme: dark; }
	.stApp { background: #111614; color: #eef4ef; }
	[data-testid="stHeader"] { background: transparent; }
	[data-testid="stMainBlockContainer"] { max-width: 680px; padding-top: 3rem; }
	h1, h2, h3, p, label { font-family: 'Manrope', sans-serif; }
	.eyebrow { color: #91b4a1; font: 500 0.76rem 'DM Mono', monospace; letter-spacing: 0.08em; text-transform: uppercase; }
	.stTextInput input {
		background: #1b2420; color: #f1f7f2; border: 1px solid #394940;
		border-radius: 8px; font: 500 1.55rem 'DM Mono', monospace; min-height: 3.8rem;
	}
	.stTextInput input:focus { border-color: #b5e66d; box-shadow: 0 0 0 1px #b5e66d; }
	.stButton button {
		min-height: 3rem; border: 1px solid #344139; border-radius: 7px;
		background: #202a24; color: #e4ece5; font: 600 0.96rem 'DM Mono', monospace;
		transition: background 120ms ease, border-color 120ms ease, transform 120ms ease;
	}
	.stButton button:hover { background: #2b3830; border-color: #9eb5a5; color: #fff; transform: translateY(-1px); }
	.stButton button:focus-visible { outline: 2px solid #b5e66d; outline-offset: 2px; }
	div[data-testid="stRadio"] label { font-size: 0.88rem; }
	.answer { color: #b5e66d; font: 500 0.9rem 'DM Mono', monospace; text-align: right; min-height: 1.35rem; }
	.stCaption { color: #91a197; }
	hr { border-color: #344139; }
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


def _calculate():
	expression = st.session_state.get("expression", "")
	try:
		value = _evaluate(expression)
		result = _display_number(value)
		st.session_state.previous_expression = expression
		st.session_state.answer_value = value
		st.session_state.last_result = result
		st.session_state.expression = result
		st.session_state.calculation_error = ""
		st.session_state.history.insert(0, (expression, result))
		del st.session_state.history[8:]
	except (ArithmeticError, SyntaxError, ValueError, TypeError, OverflowError) as error:
		st.session_state.calculation_error = str(error) or "Unable to calculate this expression"


def _press(token):
	if token == "AC":
		st.session_state.expression = ""
		st.session_state.calculation_error = ""
	elif token == "⌫":
		st.session_state.expression = st.session_state.get("expression", "")[:-1]
		st.session_state.calculation_error = ""
	elif token == "=" :
		_calculate()
	elif token == "Ans":
		st.session_state.expression = st.session_state.get("expression", "") + "ans"
		st.session_state.calculation_error = ""
	else:
		st.session_state.expression = st.session_state.get("expression", "") + token
		st.session_state.calculation_error = ""


for key, initial_value in (
	("expression", ""),
	("answer_value", 0),
	("last_result", ""),
	("calculation_error", ""),
	("history", []),
	("angle_mode", "RAD"),
):
	if key not in st.session_state:
		st.session_state[key] = initial_value


st.markdown('<div class="eyebrow">ORBIT / SCIENTIFIC</div>', unsafe_allow_html=True)
st.title("Calculator")
st.caption("A precise workspace for everyday calculations and deeper explorations.")

mode_col, result_col = st.columns([1, 2])
with mode_col:
	st.radio("Angle mode", ["RAD", "DEG"], horizontal=True, key="angle_mode", label_visibility="collapsed")
with result_col:
	if st.session_state.previous_expression and st.session_state.last_result:
		st.markdown(
			f'<div class="answer">{st.session_state.previous_expression} = {st.session_state.last_result}</div>',
			unsafe_allow_html=True,
		)
	else:
		st.markdown('<div class="answer">&nbsp;</div>', unsafe_allow_html=True)

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
	st.caption("Type and press Enter, or use the keypad. Use * for multiplication and ^ for powers.")

st.markdown("<div style='height: 0.55rem'></div>", unsafe_allow_html=True)
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
			column.button(
				label,
				key=f"key_{row_index}_{column_index}",
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
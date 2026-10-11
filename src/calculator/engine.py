"""
Scientific calculation, calculus analysis, and unit conversion engine.
Provides safe symbolic and numerical computation utilities for Streamlit.
"""



from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
import numpy as np
import sympy as sp


class ScientificEngine:
    """Mathematical evaluation, calculus, and analysis engine backed by SymPy and NumPy."""

    def __init__(self) -> None:
        self.x = sp.Symbol("x")

    def parse_and_plot(
        self,
        expression_str: str,
        x_min: float = -10.0,
        x_max: float = 10.0,
        num_points: int = 500,
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
        """
        Safely parses a mathematical function f(x) and evaluates it over [x_min, x_max].
        Returns (x_vals, y_vals, metadata).
        """
        # Clean expression
        clean_expr = (
            expression_str.replace("^", "**")
            .replace("π", "pi")
            .replace("ln(", "log(")
        )

        # Auto-close unclosed parentheses if user omitted end brackets
        open_count = clean_expr.count("(") - clean_expr.count(")")
        if open_count > 0:
            clean_expr += ")" * open_count

        metadata: Dict[str, Any] = {
            "valid": False,
            "error": None,
            "derivative": "N/A",
            "integral": "N/A",
            "critical_points": [],
            "roots": [],
            "sym_expr": None,
            "deriv_expr": None,
        }

        try:
            # Parse symbolic expression with restricted transformations
            sym_expr = sp.sympify(clean_expr, locals={"pi": sp.pi, "E": sp.E})
            metadata["sym_expr"] = sym_expr

            # Derivative and indefinite integral
            try:
                derivative = sp.diff(sym_expr, self.x)
                metadata["derivative"] = str(derivative).replace("**", "^")
                metadata["deriv_expr"] = derivative
            except Exception:
                metadata["derivative"] = "N/A"

            try:
                integral = sp.integrate(sym_expr, self.x)
                metadata["integral"] = str(integral).replace("**", "^") + " + C"
            except Exception:
                metadata["integral"] = "N/A"

            # Numerical evaluation
            f_lambdified = sp.lambdify(self.x, sym_expr, modules=["numpy", "math"])
            x_vals = np.linspace(x_min, x_max, num_points)

            try:
                y_vals = f_lambdified(x_vals)
                # Handle scalar output if constant function like f(x) = 5
                if isinstance(y_vals, (int, float, np.number)):
                    y_vals = np.full_like(x_vals, float(y_vals))
                else:
                    y_vals = np.asarray(y_vals, dtype=np.float64)
                    # Filter out non-finite numbers (e.g. division by zero, asymptotes)
                    y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)

                metadata["valid"] = True
                return x_vals, y_vals, metadata
            except Exception as num_err:
                metadata["error"] = f"Numerical evaluation error: {num_err}"
                return np.array([]), np.array([]), metadata

        except Exception as parse_err:
            metadata["error"] = f"Syntax / Parse error: {parse_err}"
            return np.array([]), np.array([]), metadata

    def evaluate_point(self, expression_str: str, x_val: float) -> Tuple[float | None, float | None, str | None]:
        """
        Evaluates f(x) and f'(x) at a single numerical point x_val.
        Returns (f_val, deriv_val, error_message).
        """
        clean_expr = (
            expression_str.replace("^", "**")
            .replace("π", "pi")
            .replace("ln(", "log(")
        )
        open_count = clean_expr.count("(") - clean_expr.count(")")
        if open_count > 0:
            clean_expr += ")" * open_count

        try:
            sym_expr = sp.sympify(clean_expr, locals={"pi": sp.pi, "E": sp.E})
            f_val = float(sym_expr.subs(self.x, x_val).evalf())

            deriv_val: float | None = None
            try:
                deriv_expr = sp.diff(sym_expr, self.x)
                deriv_val = float(deriv_expr.subs(self.x, x_val).evalf())
            except Exception:
                deriv_val = None

            return f_val, deriv_val, None
        except Exception as e:
            return None, None, str(e)

    @staticmethod
    def get_constants() -> List[Dict[str, str]]:
        """Returns standard scientific and mathematical constants."""
        return [
            {"Name": "Pi (π)", "Symbol": "π", "Value": "3.141592653589793", "Category": "Mathematics"},
            {"Name": "Euler's Number (e)", "Symbol": "e", "Value": "2.718281828459045", "Category": "Mathematics"},
            {"Name": "Golden Ratio (φ)", "Symbol": "φ", "Value": "1.618033988749895", "Category": "Mathematics"},
            {"Name": "Speed of Light in Vacuum (c)", "Symbol": "c", "Value": "299,792,458 m/s", "Category": "Physics"},
            {"Name": "Gravitational Constant (G)", "Symbol": "G", "Value": "6.67430 × 10⁻¹¹ m³/(kg·s²)", "Category": "Physics"},
            {"Name": "Planck Constant (h)", "Symbol": "h", "Value": "6.62607015 × 10⁻³⁴ J·s", "Category": "Physics"},
            {"Name": "Reduced Planck Constant (ℏ)", "Symbol": "ℏ", "Value": "1.054571817 × 10⁻³⁴ J·s", "Category": "Physics"},
            {"Name": "Elementary Charge (e)", "Symbol": "qe", "Value": "1.602176634 × 10⁻¹⁹ C", "Category": "Physics"},
            {"Name": "Avogadro Constant (N_A)", "Symbol": "N_A", "Value": "6.02214076 × 10²³ mol⁻¹", "Category": "Physics"},
            {"Name": "Boltzmann Constant (k_B)", "Symbol": "k_B", "Value": "1.380649 × 10⁻²³ J/K", "Category": "Physics"},
            {"Name": "Standard Atmospheric Pressure", "Symbol": "1 atm", "Value": "101,325 Pa", "Category": "Physics"},
            {"Name": "Standard Acceleration of Gravity", "Symbol": "g", "Value": "9.80665 m/s²", "Category": "Physics"},
            {"Name": "Universal Gas Constant (R)", "Symbol": "R", "Value": "8.314462618 J/(mol·K)", "Category": "Physics"},
            {"Name": "Stefan-Boltzmann Constant (σ)", "Symbol": "σ", "Value": "5.670374419 × 10⁻⁸ W/(m²·K⁴)", "Category": "Physics"},
            {"Name": "Fine-Structure Constant (α)", "Symbol": "α", "Value": "7.2973525693 × 10⁻³ (≈ 1/137)", "Category": "Physics"},
        ]

    @staticmethod
    def get_unit_categories() -> Dict[str, List[str]]:
        """Returns supported unit conversion categories and their unit names."""
        return {
            "Angle": ["Degrees (°)", "Radians (rad)", "Gradians (grad)", "Arcminutes (arcmin)", "Arcseconds (arcsec)"],
            "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)", "Rankine (°R)"],
            "Length": [
                "Meters (m)", "Kilometers (km)", "Centimeters (cm)", "Millimeters (mm)",
                "Micrometers (µm)", "Nanometers (nm)", "Miles (mi)", "Yards (yd)",
                "Feet (ft)", "Inches (in)", "Nautical Miles (NM)"
            ],
            "Mass": [
                "Kilograms (kg)", "Grams (g)", "Milligrams (mg)", "Metric Tons (t)",
                "Pounds (lb)", "Ounces (oz)", "Grains (gr)"
            ],
            "Speed": ["Meters/second (m/s)", "Kilometers/hour (km/h)", "Miles/hour (mph)", "Knots (kn)", "Mach (std sea level)"],
            "Pressure": [
                "Pascal (Pa)", "Kilopascal (kPa)", "Bar (bar)", "Millibar (mbar)",
                "Atmosphere (atm)", "Pounds/sq inch (psi)", "Torr / mmHg"
            ],
            "Energy": [
                "Joules (J)", "Kilojoules (kJ)", "Calories (cal)", "Kilocalories (kcal)",
                "Watt-hours (Wh)", "Kilowatt-hours (kWh)", "Electronvolts (eV)", "BTU (IT)"
            ],
        }

    @classmethod
    def convert_units(
        cls, category: str, value: float, from_unit: str, to_unit: str
    ) -> Tuple[float, str]:
        """
        Converts value from `from_unit` to `to_unit` in the specified category.
        Returns (converted_value, explanation_formula).
        """
        if from_unit == to_unit:
            return value, f"{value} = {value}"

        # Temperature
        if category == "Temperature":
            # Convert to Kelvin first
            k_val: float
            if "Celsius" in from_unit:
                k_val = value + 273.15
            elif "Fahrenheit" in from_unit:
                k_val = (value - 32.0) * (5.0 / 9.0) + 273.15
            elif "Kelvin" in from_unit:
                k_val = value
            elif "Rankine" in from_unit:
                k_val = value * (5.0 / 9.0)
            else:
                k_val = value

            # Convert Kelvin to target
            res: float
            if "Celsius" in to_unit:
                res = k_val - 273.15
                formula = f"({value} in K) - 273.15 = {res:.6g} °C"
            elif "Fahrenheit" in to_unit:
                res = (k_val - 273.15) * (9.0 / 5.0) + 32.0
                formula = f"(({value} in K) - 273.15) × 9/5 + 32 = {res:.6g} °F"
            elif "Kelvin" in to_unit:
                res = k_val
                formula = f"{res:.6g} K"
            elif "Rankine" in to_unit:
                res = k_val * (9.0 / 5.0)
                formula = f"({value} in K) × 9/5 = {res:.6g} °R"
            else:
                res = k_val
                formula = str(res)
            return res, formula

        # Linear conversions (Convert to base unit, then to target)
        factors_to_base: Dict[str, Dict[str, float]] = {
            "Angle": {
                # Base: Radians
                "Radians (rad)": 1.0,
                "Degrees (°)": math.pi / 180.0,
                "Gradians (grad)": math.pi / 200.0,
                "Arcminutes (arcmin)": (math.pi / 180.0) / 60.0,
                "Arcseconds (arcsec)": (math.pi / 180.0) / 3600.0,
            },
            "Length": {
                # Base: Meters
                "Meters (m)": 1.0,
                "Kilometers (km)": 1000.0,
                "Centimeters (cm)": 0.01,
                "Millimeters (mm)": 0.001,
                "Micrometers (µm)": 1e-6,
                "Nanometers (nm)": 1e-9,
                "Miles (mi)": 1609.344,
                "Yards (yd)": 0.9144,
                "Feet (ft)": 0.3048,
                "Inches (in)": 0.0254,
                "Nautical Miles (NM)": 1852.0,
            },
            "Mass": {
                # Base: Kilograms
                "Kilograms (kg)": 1.0,
                "Grams (g)": 0.001,
                "Milligrams (mg)": 1e-6,
                "Metric Tons (t)": 1000.0,
                "Pounds (lb)": 0.45359237,
                "Ounces (oz)": 0.028349523125,
                "Grains (gr)": 0.00006479891,
            },
            "Speed": {
                # Base: m/s
                "Meters/second (m/s)": 1.0,
                "Kilometers/hour (km/h)": 1.0 / 3.6,
                "Miles/hour (mph)": 0.44704,
                "Knots (kn)": 0.5144444444,
                "Mach (std sea level)": 340.29,
            },
            "Pressure": {
                # Base: Pascal
                "Pascal (Pa)": 1.0,
                "Kilopascal (kPa)": 1000.0,
                "Bar (bar)": 100000.0,
                "Millibar (mbar)": 100.0,
                "Atmosphere (atm)": 101325.0,
                "Pounds/sq inch (psi)": 6894.75729,
                "Torr / mmHg": 133.322368,
            },
            "Energy": {
                # Base: Joules
                "Joules (J)": 1.0,
                "Kilojoules (kJ)": 1000.0,
                "Calories (cal)": 4.184,
                "Kilocalories (kcal)": 4184.0,
                "Watt-hours (Wh)": 3600.0,
                "Kilowatt-hours (kWh)": 3.6e6,
                "Electronvolts (eV)": 1.602176634e-19,
                "BTU (IT)": 1055.05585,
            },
        }

        cat_factors = factors_to_base.get(category, {})
        from_factor = cat_factors.get(from_unit, 1.0)
        to_factor = cat_factors.get(to_unit, 1.0)

        base_val = value * from_factor
        result = base_val / to_factor
        ratio = from_factor / to_factor
        explanation = f"1 {from_unit} = {ratio:.6g} {to_unit} (Factor: × {ratio:.8g})"

        return result, explanation

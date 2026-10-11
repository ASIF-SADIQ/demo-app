"""
Unit tests for Scientific Calculator Engine and Component Generator.
"""

from __future__ import annotations

import pytest
import numpy as np

try:
    from calculator.engine import ScientificEngine
    from calculator.calculator_ui import get_calculator_html
except ImportError:
    from src.calculator.engine import ScientificEngine
    from src.calculator.calculator_ui import get_calculator_html


def test_engine_constants() -> None:
    engine = ScientificEngine()
    constants = engine.get_constants()
    assert len(constants) >= 10
    pi_const = next(c for c in constants if c["Symbol"] == "π")
    assert "3.1415" in pi_const["Value"]


def test_engine_parse_and_plot() -> None:
    engine = ScientificEngine()
    x_vals, y_vals, meta = engine.parse_and_plot("sin(x)", x_min=-np.pi, x_max=np.pi, num_points=100)

    assert meta["valid"] is True
    assert len(x_vals) == 100
    assert len(y_vals) == 100
    assert "cos(x)" in meta["derivative"]
    assert "cos(x)" in meta["integral"]


def test_engine_polynomial() -> None:
    engine = ScientificEngine()
    x_vals, y_vals, meta = engine.parse_and_plot("x^2 - 4", x_min=-3.0, x_max=3.0, num_points=50)

    assert meta["valid"] is True
    assert "2*x" in meta["derivative"]


def test_engine_evaluate_point() -> None:
    engine = ScientificEngine()
    f_val, deriv_val, err = engine.evaluate_point("x^2 + 3*x", 2.0)
    assert err is None
    assert f_val == pytest.approx(10.0)
    assert deriv_val == pytest.approx(7.0)


def test_engine_unit_converter() -> None:
    engine = ScientificEngine()
    # 100 Celsius to Fahrenheit: 212
    f_val, formula = engine.convert_units("Temperature", 100.0, "Celsius (°C)", "Fahrenheit (°F)")
    assert f_val == pytest.approx(212.0)
    assert "°F" in formula

    # 180 Degrees to Radians: pi
    rad_val, _ = engine.convert_units("Angle", 180.0, "Degrees (°)", "Radians (rad)")
    assert rad_val == pytest.approx(np.pi)

    # 1 km to m: 1000
    m_val, _ = engine.convert_units("Length", 1.0, "Kilometers (km)", "Meters (m)")
    assert m_val == pytest.approx(1000.0)


def test_calculator_html_generation() -> None:
    html = get_calculator_html()
    assert "<!DOCTYPE html>" in html
    assert "calc-input" in html
    assert "eval-result" in html
    assert "btn-deg-toggle" in html
    assert "btn-2nd" in html
    assert "help-modal" in html
    # Verify no forbidden native alert dialogs
    assert "alert(" not in html

"""
Unit tests for FX Scientific Calculator Component Generator.
"""

from __future__ import annotations

import pytest

try:
    from calculator.calculator_ui import get_calculator_html
except ImportError:
    from src.calculator.calculator_ui import get_calculator_html


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

"""
Pro Scientific Calculator Application
Built with Python, Streamlit, and uv.
Featuring Keyboard-First Interaction, Permanent Blinking Cursor,
Auto-Closing Parentheses, and Complete Scientific Functions.
"""

from __future__ import annotations

import importlib
import streamlit as st
import streamlit.components.v1 as components

try:
    import calculator.calculator_ui as calc_module
except ImportError:
    import src.calculator.calculator_ui as calc_module

importlib.reload(calc_module)
get_calculator_html = calc_module.get_calculator_html


def setup_page() -> None:
    """Configures page title, icon, and custom dark aesthetics."""
    st.set_page_config(
        page_title="FX Scientific Calculator",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Custom styling
    st.markdown(
        """
        <style>
        /* Modern dark theme background adjustments */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #111827 0%, #090d16 100%);
            color: #f8fafc;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 900px;
            margin: 0 auto;
        }
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: rgba(13, 17, 27, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }
        .sidebar-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 10px;
            padding: 12px 14px;
            margin-bottom: 14px;
        }
        .kbd-badge {
            background: rgba(99, 102, 241, 0.2);
            color: #c7d2fe;
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 4px;
            padding: 2px 6px;
            font-family: monospace;
            font-size: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Renders the left sidebar with shortcuts guide and system status."""
    with st.sidebar:
        st.markdown("### 🧮 FX Scientific Calculator")
        st.caption("Keyboard-first high-precision scientific workspace")

        st.markdown(
            """
            <div class="sidebar-card">
                <div style="font-weight:700; font-size:13px; color:#e2e8f0; margin-bottom:8px;">
                    ⌨️ Physical Keyboard Controls
                </div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.7;">
                    • <span class="kbd-badge">Enter</span> / <span class="kbd-badge">=</span> : Calculate result<br/>
                    • <span class="kbd-badge">Backspace</span> : Smart token delete<br/>
                    • <span class="kbd-badge">Esc</span> : All Clear (AC)<br/>
                    • <span class="kbd-badge">0-9</span> <span class="kbd-badge">.</span> : Digits & Decimals<br/>
                    • <span class="kbd-badge">+ - * /</span> : Operators<br/>
                    • <span class="kbd-badge">s</span>, <span class="kbd-badge">c</span>, <span class="kbd-badge">t</span> : sin, cos, tan<br/>
                    • <span class="kbd-badge">l</span> / <span class="kbd-badge">L</span> : ln / log₁₀<br/>
                    • <span class="kbd-badge">p</span> / <span class="kbd-badge">e</span> : π / e<br/>
                    • <span class="kbd-badge">r</span> : Square root (√)<br/>
                    • <span class="kbd-badge">d</span> : Toggle DEG/RAD mode
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-card">
                <div style="font-weight:700; font-size:13px; color:#e2e8f0; margin-bottom:6px;">
                    ⚡ Auto-Close Parentheses
                </div>
                <div style="font-size:12px; color:#94a3b8;">
                    No need to manually type closing brackets like <code>)</code>. Expressions like <code>cos(90</code> evaluate directly on <span class="kbd-badge">Enter</span>!
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.caption("Precision Engine: Shunting-Yard AST")
        st.caption("Managed with `uv` • Streamlit Dark Theme")


def main() -> None:
    """Main application loop."""
    setup_page()
    render_sidebar()

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 12px;">
            <h1 style="font-size: 32px; font-weight: 800; letter-spacing: 1.5px; background: linear-gradient(135deg, #c7d2fe 0%, #818cf8 40%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; text-transform: uppercase;">ASIF SADIQ</h1>
            <p style="color: #94a3b8; font-size: 13px; margin-top: 4px; font-weight: 500; letter-spacing: 0.5px;">FX Scientific Calculator Pro</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render the pure keyboard-first scientific calculator component
    html_code = get_calculator_html()
    components.html(html_code, height=780, scrolling=False)


if __name__ == "__main__":
    main()

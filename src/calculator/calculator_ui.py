"""
HTML, CSS, and JavaScript renderer for the Keyboard-First Scientific Calculator.
Provides instant autofocus, continuous cursor, auto-closing parentheses,
comprehensive keyboard handling, tactile audio haptics, history tape, and AST-based evaluation.
"""

from __future__ import annotations


def get_calculator_html() -> str:
    """Returns self-contained, high-performance HTML/CSS/JS for the Scientific Calculator."""
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Scientific Calculator FX</title>
<style>
  :root {
    --bg-dark: #090d16;
    --panel-bg: rgba(18, 24, 38, 0.92);
    --panel-border: rgba(255, 255, 255, 0.08);
    --display-bg: rgba(10, 14, 23, 0.95);
    --btn-num-bg: rgba(255, 255, 255, 0.04);
    --btn-num-hover: rgba(255, 255, 255, 0.09);
    --btn-fn-bg: rgba(99, 102, 241, 0.12);
    --btn-fn-hover: rgba(99, 102, 241, 0.24);
    --btn-fn-text: #a5b4fc;
    --btn-op-bg: rgba(59, 130, 246, 0.16);
    --btn-op-hover: rgba(59, 130, 246, 0.28);
    --btn-op-text: #93c5fd;
    --btn-eq-bg: linear-gradient(135deg, #10b981 0%, #059669 100%);
    --btn-eq-hover: linear-gradient(135deg, #34d399 0%, #10b981 100%);
    --btn-eq-shadow: rgba(16, 185, 129, 0.35);
    --btn-clear-bg: rgba(239, 68, 68, 0.15);
    --btn-clear-hover: rgba(239, 68, 68, 0.25);
    --btn-clear-text: #fca5a5;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --accent: #6366f1;
    --accent-glow: rgba(99, 102, 241, 0.4);
    --radius-lg: 16px;
    --radius-md: 10px;
    --radius-sm: 6px;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
    -webkit-user-select: none;
  }

  body {
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 10px;
    min-height: 100vh;
    overflow-x: hidden;
  }

  .calc-wrapper {
    width: 100%;
    max-width: 820px;
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    position: relative;
  }

  /* Top Control Bar */
  .calc-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }

  .brand-group {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .brand-badge {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
  }

  .brand-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    letter-spacing: -0.2px;
  }

  .calc-status-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .mode-pill {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .mode-pill:hover {
    background: rgba(255, 255, 255, 0.12);
  }
  .mode-pill.active {
    background: rgba(99, 102, 241, 0.25);
    border-color: #6366f1;
    color: #c7d2fe;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
  }

  .icon-btn {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--text-secondary);
    font-size: 12px;
    padding: 5px 9px;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
  .icon-btn:hover {
    background: rgba(255, 255, 255, 0.12);
    color: var(--text-primary);
  }
  .icon-btn.active {
    color: #10b981;
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(16, 185, 129, 0.12);
  }

  .memory-indicator {
    font-size: 10px;
    font-weight: 700;
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.4);
    padding: 2px 6px;
    border-radius: 4px;
    display: none;
  }
  .memory-indicator.visible {
    display: inline-block;
  }

  /* Display Area */
  .calc-display {
    background: var(--display-bg);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
    position: relative;
    cursor: text;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .calc-display:focus-within {
    border-color: var(--accent);
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6), 0 0 0 1px var(--accent-glow);
  }

  .history-line {
    font-size: 13px;
    color: var(--text-secondary);
    min-height: 18px;
    text-align: right;
    font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    opacity: 0.85;
  }

  .input-container {
    position: relative;
    width: 100%;
    margin-top: 4px;
  }

  #calc-input {
    width: 100%;
    background: transparent;
    border: none;
    outline: none;
    font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
    font-size: 26px;
    font-weight: 500;
    color: #ffffff;
    text-align: right;
    letter-spacing: 0.5px;
    caret-color: #6366f1;
    user-select: text;
    -webkit-user-select: text;
  }

  .result-line-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
  }

  .preview-result {
    font-size: 13px;
    color: #64748b;
    font-family: "JetBrains Mono", Consolas, monospace;
    font-style: italic;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
  }

  .evaluated-result {
    font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
    font-size: 32px;
    font-weight: 700;
    color: #10b981;
    text-align: right;
    letter-spacing: -0.5px;
    min-height: 38px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
    transition: transform 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    white-space: nowrap;
  }
  .evaluated-result.pulse {
    transform: scale(1.02);
  }
  .evaluated-result.error {
    color: #f87171;
    font-size: 15px;
    font-weight: 500;
    letter-spacing: 0;
  }

  .copy-btn {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    font-size: 12px;
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .copy-btn:hover {
    background: rgba(255, 255, 255, 0.15);
    color: #ffffff;
  }

  /* Keyboard quick hint banner */
  .keyboard-pill-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    align-items: center;
    font-size: 11px;
    color: var(--text-secondary);
    padding: 6px 10px;
    background: rgba(0, 0, 0, 0.25);
    border-radius: var(--radius-sm);
    border: 1px solid rgba(255, 255, 255, 0.04);
  }
  .kbd-chip {
    background: rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 11px;
    border-bottom: 2px solid rgba(0, 0, 0, 0.4);
  }

  /* History Slide-out Drawer */
  .history-drawer {
    display: none;
    background: rgba(10, 14, 23, 0.98);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: var(--radius-md);
    padding: 14px;
    max-height: 220px;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  }
  .history-drawer.open {
    display: block;
    animation: fadeIn 0.2s ease forwards;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .history-drawer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }
  .history-drawer-title {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .history-item {
    padding: 7px 10px;
    border-radius: var(--radius-sm);
    background: rgba(255, 255, 255, 0.03);
    margin-bottom: 5px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .history-item:hover {
    background: rgba(99, 102, 241, 0.15);
    border-left: 3px solid #6366f1;
    transform: translateX(2px);
  }
  .history-item-expr {
    font-size: 13px;
    color: var(--text-secondary);
    font-family: monospace;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 60%;
  }
  .history-item-res {
    font-size: 14px;
    color: #10b981;
    font-weight: 600;
    font-family: monospace;
    text-align: right;
  }

  .history-empty {
    font-size: 12px;
    color: #64748b;
    text-align: center;
    padding: 20px 0;
  }

  /* 6-Column Keypad layout */
  .calc-keypad {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
  }

  .calc-btn {
    appearance: none;
    -webkit-appearance: none;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: var(--radius-md);
    padding: 13px 4px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.12s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-primary);
    background: var(--btn-num-bg);
    position: relative;
    overflow: hidden;
  }

  .calc-btn:hover {
    background: var(--btn-num-hover);
    border-color: rgba(255, 255, 255, 0.14);
    transform: translateY(-1px);
  }

  .calc-btn:active, .calc-btn.key-pressed {
    transform: translateY(1px);
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4);
    border-color: var(--accent);
  }

  /* Button styles by category */
  .btn-scientific {
    background: var(--btn-fn-bg);
    color: var(--btn-fn-text);
    border-color: rgba(99, 102, 241, 0.15);
    font-size: 14px;
  }
  .btn-scientific:hover {
    background: var(--btn-fn-hover);
    border-color: rgba(99, 102, 241, 0.35);
  }
  .btn-scientific.toggle-active {
    background: rgba(99, 102, 241, 0.35);
    border-color: #6366f1;
    color: #ffffff;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
  }

  .btn-operator {
    background: var(--btn-op-bg);
    color: var(--btn-op-text);
    border-color: rgba(59, 130, 246, 0.2);
    font-size: 18px;
    font-weight: 600;
  }
  .btn-operator:hover {
    background: var(--btn-op-hover);
    border-color: rgba(59, 130, 246, 0.4);
  }

  .btn-danger {
    background: var(--btn-clear-bg);
    color: var(--btn-clear-text);
    border-color: rgba(239, 68, 68, 0.2);
    font-weight: 600;
  }
  .btn-danger:hover {
    background: var(--btn-clear-hover);
    border-color: rgba(239, 68, 68, 0.4);
  }

  .btn-equals {
    background: var(--btn-eq-bg);
    color: #ffffff;
    font-weight: 700;
    font-size: 20px;
    border-color: transparent;
    box-shadow: 0 4px 14px var(--btn-eq-shadow);
  }
  .btn-equals:hover {
    background: var(--btn-eq-hover);
    box-shadow: 0 6px 18px var(--btn-eq-shadow);
  }

  .btn-mem {
    background: rgba(245, 158, 11, 0.08);
    color: #fcd34d;
    border-color: rgba(245, 158, 11, 0.15);
    font-size: 13px;
    font-weight: 600;
  }
  .btn-mem:hover {
    background: rgba(245, 158, 11, 0.16);
    border-color: rgba(245, 158, 11, 0.3);
  }

  /* Help Modal Dialog */
  .modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(8px);
    z-index: 200;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  .modal-overlay.open {
    display: flex;
    animation: fadeIn 0.2s ease forwards;
  }
  .modal-card {
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 540px;
    padding: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  }
  .modal-title {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .modal-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 12px;
  }
  .modal-table td {
    padding: 6px 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
  .modal-table td:first-child {
    font-family: monospace;
    color: #a5b4fc;
    font-weight: 600;
    width: 35%;
  }

  /* Toast Notification */
  .toast {
    position: absolute;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: rgba(16, 185, 129, 0.95);
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 20px;
    opacity: 0;
    pointer-events: none;
    transition: all 0.25s ease;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    z-index: 100;
  }
  .toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }

  @media (max-width: 700px) {
    .calc-keypad {
      gap: 5px;
    }
    .calc-btn {
      padding: 11px 2px;
      font-size: 13px;
    }
    #calc-input {
      font-size: 20px;
    }
    .evaluated-result {
      font-size: 24px;
    }
  }
</style>
</head>
<body>

<div class="calc-wrapper" id="calculator-app">
  <!-- Top Header Controls -->
  <div class="calc-header">
    <div class="brand-group">
      <span class="brand-badge">ASIF SADIQ</span>
      <span class="brand-title">Scientific FX</span>
      <span class="memory-indicator" id="mem-indicator">M</span>
    </div>

    <div class="calc-status-group">
      <button class="mode-pill active" id="btn-deg-toggle" title="Toggle Angle Mode (Shortcut: d)">DEG</button>
      <button class="icon-btn" id="btn-audio-toggle" title="Toggle Audio Haptics">🔊 Sound</button>
      <button class="icon-btn" id="btn-history-toggle" title="Toggle Calculation History">🕒 History</button>
      <button class="icon-btn" id="btn-theme-help" title="Keyboard Shortcuts Reference">⌨️ Shortcuts</button>
    </div>
  </div>

  <!-- Interactive Display Area (Autofocused, Persistent Cursor) -->
  <div class="calc-display" id="display-container">
    <div class="history-line" id="prev-expr-line"></div>
    <div class="input-container">
      <input
        type="text"
        id="calc-input"
        placeholder="0"
        autocomplete="off"
        spellcheck="false"
        autofocus
      />
    </div>
    <div class="result-line-container">
      <div class="preview-result" id="preview-line"></div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <button class="copy-btn" id="btn-copy" title="Copy result to clipboard">Copy</button>
        <div class="evaluated-result" id="eval-result">0</div>
      </div>
    </div>
  </div>

  <!-- Keyboard Shortcuts Tip Banner -->
  <div class="keyboard-pill-bar">
    <span>💡 Direct Typing:</span>
    <span class="kbd-chip">Enter / = : Calc</span>
    <span class="kbd-chip">Backspace : Delete</span>
    <span class="kbd-chip">Esc : AC</span>
    <span class="kbd-chip">s/c/t : sin/cos/tan</span>
    <span class="kbd-chip">l/L : ln/log</span>
    <span class="kbd-chip">p/e : π/e</span>
    <span class="kbd-chip">r : √</span>
    <span class="kbd-chip">d : DEG/RAD</span>
  </div>

  <!-- History Drawer -->
  <div class="history-drawer" id="history-drawer">
    <div class="history-drawer-header">
      <span class="history-drawer-title">Calculation Tape</span>
      <button class="copy-btn" id="btn-clear-history">Clear History</button>
    </div>
    <div id="history-list"></div>
  </div>

  <!-- Pure Scientific 6-Column Keypad -->
  <div class="calc-keypad" id="keypad">
    <!-- Row 1: 2nd Function Toggle, Trigonometry & Constants -->
    <button class="calc-btn btn-scientific" id="btn-2nd" data-val="2nd_toggle" title="Toggle 2nd Functions (sin⁻¹, cos⁻¹, tan⁻¹, etc.)">2nd</button>
    <button class="calc-btn btn-scientific" id="btn-sin" data-val="sin(">sin</button>
    <button class="calc-btn btn-scientific" id="btn-cos" data-val="cos(">cos</button>
    <button class="calc-btn btn-scientific" id="btn-tan" data-val="tan(">tan</button>
    <button class="calc-btn btn-scientific" data-val="π">π</button>
    <button class="calc-btn btn-scientific" data-val="e">e</button>

    <!-- Row 2: Powers, Roots & Logarithms -->
    <button class="calc-btn btn-scientific" id="btn-sqr" data-val="^2">x²</button>
    <button class="calc-btn btn-scientific" data-val="^">xʸ</button>
    <button class="calc-btn btn-scientific" id="btn-sqrt" data-val="sqrt(">√x</button>
    <button class="calc-btn btn-scientific" id="btn-ln" data-val="ln(">ln</button>
    <button class="calc-btn btn-scientific" id="btn-log" data-val="log(">log</button>
    <button class="calc-btn btn-scientific" id="btn-exp10" data-val="10^">10ˣ</button>

    <!-- Row 3: Memory Registers & Parentheses -->
    <button class="calc-btn btn-mem" data-val="MC">MC</button>
    <button class="calc-btn btn-mem" data-val="MR">MR</button>
    <button class="calc-btn btn-mem" data-val="M+">M+</button>
    <button class="calc-btn btn-mem" data-val="M-">M-</button>
    <button class="calc-btn btn-scientific" data-val="(">(</button>
    <button class="calc-btn btn-scientific" data-val=")">)</button>

    <!-- Row 4: Factorial, Reciprocal + Numpad 7-9 & Division -->
    <button class="calc-btn btn-scientific" data-val="!">n!</button>
    <button class="calc-btn btn-scientific" data-val="1/">1/x</button>
    <button class="calc-btn" data-val="7">7</button>
    <button class="calc-btn" data-val="8">8</button>
    <button class="calc-btn" data-val="9">9</button>
    <button class="calc-btn btn-operator" data-val="/">÷</button>

    <!-- Row 5: Absolute Value, Percent + Numpad 4-6 & Multiplication -->
    <button class="calc-btn btn-scientific" data-val="abs(">|x|</button>
    <button class="calc-btn btn-operator" data-val="%">%</button>
    <button class="calc-btn" data-val="4">4</button>
    <button class="calc-btn" data-val="5">5</button>
    <button class="calc-btn" data-val="6">6</button>
    <button class="calc-btn btn-operator" data-val="*">×</button>

    <!-- Row 6: Clear, Delete + Numpad 1-3 & Subtraction -->
    <button class="calc-btn btn-danger" data-val="AC">AC</button>
    <button class="calc-btn btn-danger" data-val="DEL">DEL</button>
    <button class="calc-btn" data-val="1">1</button>
    <button class="calc-btn" data-val="2">2</button>
    <button class="calc-btn" data-val="3">3</button>
    <button class="calc-btn btn-operator" data-val="-">−</button>

    <!-- Row 7: Ans, Negation, 0, Decimal, Addition & Equals -->
    <button class="calc-btn btn-scientific" data-val="Ans">Ans</button>
    <button class="calc-btn btn-scientific" data-val="+/-">±</button>
    <button class="calc-btn" data-val="0">0</button>
    <button class="calc-btn" data-val=".">.</button>
    <button class="calc-btn btn-operator" data-val="+">+</button>
    <button class="calc-btn btn-equals" data-val="=">=</button>
  </div>

  <!-- Help Modal -->
  <div class="modal-overlay" id="help-modal">
    <div class="modal-card">
      <div class="modal-title">
        <span>⌨️ Keyboard Shortcuts Reference</span>
        <button class="copy-btn" id="btn-close-help">✕ Close</button>
      </div>
      <p style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
        You can type directly anywhere on the screen! Unclosed brackets like <code>)</code> are automatically resolved upon calculation.
      </p>
      <table class="modal-table">
        <tr><td>Enter / =</td><td>Evaluate expression (auto-closes brackets)</td></tr>
        <tr><td>Backspace</td><td>Delete last character or multi-letter function</td></tr>
        <tr><td>Escape (Esc)</td><td>All Clear (AC) - Resets input display</td></tr>
        <tr><td>0 - 9, .</td><td>Direct digit and decimal entry</td></tr>
        <tr><td>+, -, *, /</td><td>Mathematical operators (+, −, ×, ÷)</td></tr>
        <tr><td>^, %</td><td>Exponentiation (xʸ) and Modulo / Percentage</td></tr>
        <tr><td>( and )</td><td>Parentheses grouping</td></tr>
        <tr><td>s / c / t</td><td>sin( , cos( , tan(</td></tr>
        <tr><td>l / L</td><td>Natural log ln( / Base-10 log(</td></tr>
        <tr><td>p / e</td><td>Constants π (pi) and e</td></tr>
        <tr><td>r or v</td><td>Square root sqrt(</td></tr>
        <tr><td>d</td><td>Toggle Angle Mode between DEG and RAD</td></tr>
        <tr><td>!</td><td>Factorial n!</td></tr>
      </table>
    </div>
  </div>

  <div class="toast" id="toast-msg">Copied!</div>
</div>

<script>
  // State
  let isDegMode = true;
  let is2ndMode = false;
  let memoryValue = 0;
  let lastAnswer = 0;
  let soundEnabled = true;
  let historyTape = [];
  let evaluatedJustNow = false;

  // Audio Synth (Web Audio API - No external assets)
  let audioCtx = null;
  function playClick(freq = 900, type = 'sine') {
    if (!soundEnabled) return;
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.04);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.04);
    } catch (e) {}
  }

  // Elements
  const calcInput = document.getElementById('calc-input');
  const prevExprLine = document.getElementById('prev-expr-line');
  const previewLine = document.getElementById('preview-line');
  const evalResult = document.getElementById('eval-result');
  const memIndicator = document.getElementById('mem-indicator');
  const btnDegToggle = document.getElementById('btn-deg-toggle');
  const btnAudioToggle = document.getElementById('btn-audio-toggle');
  const btnHistoryToggle = document.getElementById('btn-history-toggle');
  const historyDrawer = document.getElementById('history-drawer');
  const historyList = document.getElementById('history-list');
  const btnClearHistory = document.getElementById('btn-clear-history');
  const btnCopy = document.getElementById('btn-copy');
  const toastMsg = document.getElementById('toast-msg');
  const helpModal = document.getElementById('help-modal');
  const btnCloseHelp = document.getElementById('btn-close-help');
  const btn2nd = document.getElementById('btn-2nd');

  const btnSin = document.getElementById('btn-sin');
  const btnCos = document.getElementById('btn-cos');
  const btnTan = document.getElementById('btn-tan');
  const btnLn = document.getElementById('btn-ln');
  const btnLog = document.getElementById('btn-log');
  const btnSqrt = document.getElementById('btn-sqrt');
  const btnSqr = document.getElementById('btn-sqr');
  const btnExp10 = document.getElementById('btn-exp10');

  // Load persistence
  try {
    const savedHist = localStorage.getItem('calc_history');
    if (savedHist) historyTape = JSON.parse(savedHist);
    const savedMem = localStorage.getItem('calc_memory');
    if (savedMem) {
      memoryValue = parseFloat(savedMem) || 0;
      updateMemoryIndicator();
    }
  } catch(e) {}

  // Always retain focus and blinking cursor
  function ensureFocus() {
    if (document.activeElement !== calcInput) {
      calcInput.focus();
    }
  }

  window.addEventListener('DOMContentLoaded', () => {
    ensureFocus();
    renderHistory();
  });
  window.addEventListener('load', ensureFocus);
  document.addEventListener('click', (e) => {
    if (
      e.target !== calcInput &&
      !e.target.closest('.history-item') &&
      !e.target.closest('.copy-btn') &&
      !e.target.closest('.modal-card') &&
      !e.target.closest('.icon-btn')
    ) {
      setTimeout(ensureFocus, 10);
    }
  });

  // Toast feedback
  function showToast(text) {
    toastMsg.textContent = text;
    toastMsg.classList.add('show');
    setTimeout(() => toastMsg.classList.remove('show'), 1600);
  }

  function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied ${text}`);
      }).catch(() => {
        fallbackCopy(text);
      });
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast(`Copied ${text}`);
    } catch (e) {
      showToast('Copied to clipboard');
    }
  }

  function updateMemoryIndicator() {
    if (memoryValue !== 0) {
      memIndicator.classList.add('visible');
    } else {
      memIndicator.classList.remove('visible');
    }
    try {
      localStorage.setItem('calc_memory', memoryValue.toString());
    } catch(e) {}
  }

  // Toggle 2nd function key
  function toggle2nd() {
    is2ndMode = !is2ndMode;
    btn2nd.classList.toggle('toggle-active', is2ndMode);

    if (is2ndMode) {
      btnSin.textContent = 'sin⁻¹';
      btnSin.setAttribute('data-val', 'asin(');
      btnCos.textContent = 'cos⁻¹';
      btnCos.setAttribute('data-val', 'acos(');
      btnTan.textContent = 'tan⁻¹';
      btnTan.setAttribute('data-val', 'atan(');
      btnLn.textContent = 'eˣ';
      btnLn.setAttribute('data-val', 'exp(');
      btnLog.textContent = 'log₂';
      btnLog.setAttribute('data-val', 'log2(');
      btnSqrt.textContent = '³√x';
      btnSqrt.setAttribute('data-val', 'cbrt(');
      btnSqr.textContent = 'x³';
      btnSqr.setAttribute('data-val', '^3');
      btnExp10.textContent = '2ˣ';
      btnExp10.setAttribute('data-val', '2^(');
    } else {
      btnSin.textContent = 'sin';
      btnSin.setAttribute('data-val', 'sin(');
      btnCos.textContent = 'cos';
      btnCos.setAttribute('data-val', 'cos(');
      btnTan.textContent = 'tan';
      btnTan.setAttribute('data-val', 'tan(');
      btnLn.textContent = 'ln';
      btnLn.setAttribute('data-val', 'ln(');
      btnLog.textContent = 'log';
      btnLog.setAttribute('data-val', 'log(');
      btnSqrt.textContent = '√x';
      btnSqrt.setAttribute('data-val', 'sqrt(');
      btnSqr.textContent = 'x²';
      btnSqr.setAttribute('data-val', '^2');
      btnExp10.textContent = '10ˣ';
      btnExp10.setAttribute('data-val', '10^');
    }
    ensureFocus();
  }

  // Insert token at cursor position
  function insertToken(token) {
    ensureFocus();
    let currentVal = calcInput.value;
    const start = calcInput.selectionStart ?? currentVal.length;
    const end = calcInput.selectionEnd ?? currentVal.length;

    // If evaluated just now and user types an operator, continue with Ans
    if (evaluatedJustNow) {
      if (['+', '-', '*', '/', '^', '%'].includes(token)) {
        currentVal = 'Ans';
      } else if (!token.startsWith(')')) {
        currentVal = '';
      }
      evaluatedJustNow = false;
    }

    const newVal = currentVal.substring(0, start) + token + currentVal.substring(end);
    calcInput.value = newVal;

    const newCursor = start + token.length;
    calcInput.setSelectionRange(newCursor, newCursor);
    updatePreview();
  }

  // Smart Backspace
  function handleBackspace() {
    ensureFocus();
    let val = calcInput.value;
    const start = calcInput.selectionStart ?? val.length;
    const end = calcInput.selectionEnd ?? val.length;

    if (start !== end) {
      calcInput.value = val.substring(0, start) + val.substring(end);
      calcInput.setSelectionRange(start, start);
      updatePreview();
      return;
    }

    if (start === 0) return;

    // Multi-character function tokens
    const multiTokens = [
      'sin(', 'cos(', 'tan(',
      'asin(', 'acos(', 'atan(',
      'sinh(', 'cosh(', 'tanh(',
      'asinh(', 'acosh(', 'atanh(',
      'sqrt(', 'cbrt(', 'log(', 'log2(', 'ln(', 'abs(', 'exp(',
      '10^(', '1/(', '2^('
    ];

    let deleted = false;
    const beforeCursor = val.substring(0, start);
    for (const tok of multiTokens) {
      if (beforeCursor.endsWith(tok)) {
        const tokenStart = start - tok.length;
        calcInput.value = val.substring(0, tokenStart) + val.substring(start);
        calcInput.setSelectionRange(tokenStart, tokenStart);
        deleted = true;
        break;
      }
    }

    if (!deleted) {
      calcInput.value = val.substring(0, start - 1) + val.substring(start);
      calcInput.setSelectionRange(start - 1, start - 1);
    }

    updatePreview();
  }

  // All Clear (Escape)
  function clearAll() {
    calcInput.value = '';
    previewLine.textContent = '';
    evalResult.textContent = '0';
    evalResult.classList.remove('error');
    evaluatedJustNow = false;
    ensureFocus();
  }

  // Single Delete
  function deleteOne() {
    handleBackspace();
  }

  // DEG / RAD Toggle
  function toggleDegRad() {
    isDegMode = !isDegMode;
    btnDegToggle.textContent = isDegMode ? 'DEG' : 'RAD';
    btnDegToggle.title = isDegMode ? 'Angle Mode: Degrees (Shortcut: d)' : 'Angle Mode: Radians (Shortcut: d)';
    showToast(isDegMode ? 'Angle Mode: Degrees' : 'Angle Mode: Radians');
    updatePreview();
  }

  // Negate current number / expression
  function toggleSign() {
    let val = calcInput.value.trim();
    if (evaluatedJustNow) {
      val = lastAnswer.toString();
      evaluatedJustNow = false;
    }
    if (!val) {
      insertToken('-');
      return;
    }

    // If simple number, invert sign directly
    if (/^-?\d+(\.\d+)?([eE][+-]?\d+)?$/.test(val)) {
      if (val.startsWith('-')) {
        calcInput.value = val.substring(1);
      } else {
        calcInput.value = '-' + val;
      }
    } else if (val.startsWith('-(') && val.endsWith(')')) {
      calcInput.value = val.substring(2, val.length - 1);
    } else {
      calcInput.value = `-(${val})`;
    }
    updatePreview();
  }

  // Memory Handlers
  function handleMemory(action) {
    const currentNum = evaluateExpression(calcInput.value || evalResult.textContent);
    if (action === 'MC') {
      memoryValue = 0;
      showToast('Memory Cleared');
    } else if (action === 'MR') {
      insertToken(memoryValue.toString());
      showToast(`Recalled Memory: ${memoryValue}`);
    } else if (action === 'M+') {
      if (typeof currentNum === 'number' && !isNaN(currentNum)) {
        memoryValue += currentNum;
        showToast(`Memory +: ${memoryValue}`);
      }
    } else if (action === 'M-') {
      if (typeof currentNum === 'number' && !isNaN(currentNum)) {
        memoryValue -= currentNum;
        showToast(`Memory -: ${memoryValue}`);
      }
    }
    updateMemoryIndicator();
  }

  // History Tape UI (Using safe replaceChildren, createElement, textContent)
  function addHistory(expr, result) {
    historyTape.unshift({
      expr: expr,
      result: result,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
    if (historyTape.length > 50) historyTape.pop();
    try {
      localStorage.setItem('calc_history', JSON.stringify(historyTape));
    } catch(e) {}
    renderHistory();
  }

  function renderHistory() {
    historyList.replaceChildren();
    if (historyTape.length === 0) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'history-empty';
      emptyDiv.textContent = 'No calculation history yet.';
      historyList.appendChild(emptyDiv);
      return;
    }

    historyTape.forEach((item) => {
      const card = document.createElement('div');
      card.className = 'history-item';

      const exprSpan = document.createElement('span');
      exprSpan.className = 'history-item-expr';
      exprSpan.textContent = item.expr;

      const resSpan = document.createElement('span');
      resSpan.className = 'history-item-res';
      resSpan.textContent = '= ' + item.result;

      card.appendChild(exprSpan);
      card.appendChild(resSpan);

      card.addEventListener('click', () => {
        calcInput.value = item.result.toString();
        evalResult.textContent = item.result.toString();
        evalResult.classList.remove('error');
        ensureFocus();
        playClick(1000);
      });

      historyList.appendChild(card);
    });
  }

  // Factorial with safe bounds
  function factorial(n) {
    if (n < 0 || Math.floor(n) !== n) throw new Error('Factorial requires non-negative integer');
    if (n === 0 || n === 1) return 1;
    if (n > 170) throw new Error('Factorial overflow (max n=170)');
    let res = 1;
    for (let i = 2; i <= n; i++) res *= i;
    return res;
  }

  // Robust Tokenizer
  function tokenize(str) {
    let s = str
      .replace(/×/g, '*')
      .replace(/÷/g, '/')
      .replace(/−/g, '-');

    const tokens = [];
    let i = 0;

    while (i < s.length) {
      const ch = s[i];

      if (/\s/.test(ch)) {
        i++;
        continue;
      }

      // Numbers with decimal and scientific notation (e.g. 1.2e5, 3.14, .5)
      const numMatch = s.slice(i).match(/^([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?/);
      if (numMatch) {
        tokens.push({ type: 'NUM', val: parseFloat(numMatch[0]) });
        i += numMatch[0].length;
        continue;
      }

      // Mathematical constant π (pi)
      if (ch === 'π') {
        tokens.push({ type: 'NUM', val: Math.PI });
        i++;
        continue;
      }

      // Identifiers / Constants / Functions
      if (/[a-zA-Z_]/.test(ch)) {
        let idStr = '';
        while (i < s.length && /[a-zA-Z0-9_]/.test(s[i])) {
          idStr += s[i];
          i++;
        }
        const lowerId = idStr.toLowerCase();

        if (lowerId === 'pi') {
          tokens.push({ type: 'NUM', val: Math.PI });
        } else if (lowerId === 'e') {
          tokens.push({ type: 'NUM', val: Math.E });
        } else if (lowerId === 'ans') {
          tokens.push({ type: 'NUM', val: lastAnswer });
        } else {
          tokens.push({ type: 'FUNC', val: lowerId });
        }
        continue;
      }

      // Operators and Parentheses
      if (['+', '-', '*', '/', '^', '%', '!', '(', ')'].includes(ch)) {
        const prev = tokens[tokens.length - 1];

        // Unary plus detection: skip/ignore unary plus
        if (ch === '+') {
          if (!prev || prev.type === 'OP' || prev.type === 'UNARY_MINUS' || (prev.type === 'PUNCT' && prev.val === '(')) {
            i++;
            continue;
          }
        }

        // Unary minus detection
        if (ch === '-') {
          if (!prev || prev.type === 'OP' || prev.type === 'UNARY_MINUS' || (prev.type === 'PUNCT' && prev.val === '(')) {
            tokens.push({ type: 'UNARY_MINUS', val: 'u-' });
            i++;
            continue;
          }
        }

        if (ch === '(' || ch === ')') {
          tokens.push({ type: 'PUNCT', val: ch });
        } else if (ch === '!') {
          tokens.push({ type: 'POSTFIX', val: '!' });
        } else if (ch === '%') {
          // If followed by an expression, treat as modulo operator; otherwise postfix percent (divide by 100)
          const nextChar = s.slice(i + 1).trim()[0];
          if (nextChar && /[0-9a-zA-Z_(]/.test(nextChar)) {
            tokens.push({ type: 'OP', val: '%' });
          } else {
            tokens.push({ type: 'POSTFIX', val: '%' });
          }
        } else {
          tokens.push({ type: 'OP', val: ch });
        }
        i++;
        continue;
      }

      i++;
    }

    // Insert implicit multiplication: e.g. 2(3), 2π, ) (, (2)sin(30), 2Ans
    const expanded = [];
    for (let j = 0; j < tokens.length; j++) {
      expanded.push(tokens[j]);
      if (j < tokens.length - 1) {
        const curr = tokens[j];
        const next = tokens[j + 1];
        const currCanMult = (curr.type === 'NUM' || curr.type === 'POSTFIX' || (curr.type === 'PUNCT' && curr.val === ')'));
        const nextCanMult = (next.type === 'NUM' || next.type === 'FUNC' || (next.type === 'PUNCT' && next.val === '('));
        if (currCanMult && nextCanMult) {
          expanded.push({ type: 'OP', val: '*' });
        }
      }
    }
    return expanded;
  }

  // Shunting-Yard AST Builder and RPN Evaluator (Pure mathematical parser, No eval)
  function evaluateTokens(tokens) {
    const output = [];
    const opStack = [];

    const prec = {
      '+': 1, '-': 1,
      '*': 2, '/': 2, '%': 2,
      'u-': 3,
      '^': 4
    };

    const isRightAssoc = (op) => op === '^' || op === 'u-';

    for (const tok of tokens) {
      if (tok.type === 'NUM') {
        output.push(tok.val);
      } else if (tok.type === 'POSTFIX') {
        output.push(tok);
      } else if (tok.type === 'FUNC') {
        opStack.push(tok);
      } else if (tok.type === 'OP' || tok.type === 'UNARY_MINUS') {
        const o1 = tok.val;
        while (opStack.length > 0) {
          const top = opStack[opStack.length - 1];
          if (top.type === 'FUNC') {
            output.push(opStack.pop());
            continue;
          }
          if (top.type === 'OP' || top.type === 'UNARY_MINUS') {
            const o2 = top.val;
            const p1 = prec[o1] || 0;
            const p2 = prec[o2] || 0;
            if ((!isRightAssoc(o1) && p1 <= p2) || (isRightAssoc(o1) && p1 < p2)) {
              output.push(opStack.pop());
              continue;
            }
          }
          break;
        }
        opStack.push(tok);
      } else if (tok.type === 'PUNCT' && tok.val === '(') {
        opStack.push(tok);
      } else if (tok.type === 'PUNCT' && tok.val === ')') {
        let foundLeft = false;
        while (opStack.length > 0) {
          const top = opStack.pop();
          if (top.type === 'PUNCT' && top.val === '(') {
            foundLeft = true;
            break;
          }
          output.push(top);
        }
        if (opStack.length > 0 && opStack[opStack.length - 1].type === 'FUNC') {
          output.push(opStack.pop());
        }
      }
    }

    while (opStack.length > 0) {
      const top = opStack.pop();
      if (top.type === 'PUNCT' && top.val === '(') {
        if (opStack.length > 0 && opStack[opStack.length - 1].type === 'FUNC') {
          output.push(opStack.pop());
        }
        continue;
      }
      output.push(top);
    }

    // Evaluate RPN
    const evalStack = [];
    const degToRad = Math.PI / 180;
    const radToDeg = 180 / Math.PI;

    for (const item of output) {
      if (typeof item === 'number') {
        evalStack.push(item);
      } else if (item.type === 'POSTFIX') {
        if (evalStack.length < 1) throw new Error('Syntax error before ' + item.val);
        const val = evalStack.pop();
        if (item.val === '!') {
          evalStack.push(factorial(val));
        } else if (item.val === '%') {
          evalStack.push(val / 100);
        }
      } else if (item.type === 'UNARY_MINUS') {
        if (evalStack.length < 1) throw new Error('Syntax error');
        evalStack.push(-evalStack.pop());
      } else if (item.type === 'OP') {
        if (evalStack.length < 2) throw new Error('Syntax error');
        const b = evalStack.pop();
        const a = evalStack.pop();
        let r = 0;
        switch (item.val) {
          case '+': r = a + b; break;
          case '-': r = a - b; break;
          case '*': r = a * b; break;
          case '/':
            if (Math.abs(b) < 1e-15) throw new Error('Cannot divide by zero');
            r = a / b;
            break;
          case '%': r = a % b; break;
          case '^':
            r = Math.pow(a, b);
            if (isNaN(r)) throw new Error('Non-real result');
            if (!isFinite(r)) throw new Error('Result overflow');
            break;
        }
        evalStack.push(r);
      } else if (item.type === 'FUNC') {
        if (evalStack.length < 1) throw new Error('Syntax error');
        let x = evalStack.pop();
        let r = 0;

        switch (item.val) {
          case 'sin':
            r = Math.sin(isDegMode ? x * degToRad : x);
            break;
          case 'cos':
            r = Math.cos(isDegMode ? x * degToRad : x);
            break;
          case 'tan':
            if (isDegMode) {
              if (Math.abs(Math.cos(x * degToRad)) < 1e-12) throw new Error('Tangent undefined');
              r = Math.tan(x * degToRad);
            } else {
              if (Math.abs(Math.cos(x)) < 1e-12) throw new Error('Tangent undefined');
              r = Math.tan(x);
            }
            break;
          case 'asin':
            if (x < -1 || x > 1) throw new Error('Domain error for asin: [-1, 1]');
            r = Math.asin(x);
            if (isDegMode) r = r * radToDeg;
            break;
          case 'acos':
            if (x < -1 || x > 1) throw new Error('Domain error for acos: [-1, 1]');
            r = Math.acos(x);
            if (isDegMode) r = r * radToDeg;
            break;
          case 'atan':
            r = Math.atan(x);
            if (isDegMode) r = r * radToDeg;
            break;
          case 'sinh': r = Math.sinh(x); break;
          case 'cosh': r = Math.cosh(x); break;
          case 'tanh': r = Math.tanh(x); break;
          case 'asinh': r = Math.asinh(x); break;
          case 'acosh':
            if (x < 1) throw new Error('Domain error for acosh: [1, ∞)');
            r = Math.acosh(x);
            break;
          case 'atanh':
            if (x <= -1 || x >= 1) throw new Error('Domain error for atanh: (-1, 1)');
            r = Math.atanh(x);
            break;
          case 'sqrt':
            if (x < 0) throw new Error('Cannot take square root of negative');
            r = Math.sqrt(x);
            break;
          case 'cbrt': r = Math.cbrt(x); break;
          case 'exp': r = Math.exp(x); break;
          case 'ln':
            if (x <= 0) throw new Error('Domain error for ln: > 0');
            r = Math.log(x);
            break;
          case 'log':
          case 'log10':
            if (x <= 0) throw new Error('Domain error for log: > 0');
            r = Math.log10(x);
            break;
          case 'log2':
            if (x <= 0) throw new Error('Domain error for log2: > 0');
            r = Math.log2(x);
            break;
          case 'abs': r = Math.abs(x); break;
          default:
            throw new Error(`Unknown function: ${item.val}`);
        }
        evalStack.push(r);
      }
    }

    if (evalStack.length !== 1) throw new Error('Syntax error');
    let finalRes = evalStack[0];

    // Clean floating point rounding noise (e.g. 0.1 + 0.2 = 0.3)
    if (typeof finalRes === 'number' && !isNaN(finalRes)) {
      if (Math.abs(finalRes) < 1e-14) finalRes = 0;
      else finalRes = parseFloat(finalRes.toPrecision(12));
    }
    return finalRes;
  }

  // Automatically close any unclosed opening parentheses
  function autoCloseParentheses(str) {
    if (!str) return '';
    let openCount = 0;
    for (let i = 0; i < str.length; i++) {
      if (str[i] === '(') {
        openCount++;
      } else if (str[i] === ')') {
        if (openCount > 0) openCount--;
      }
    }
    return str + ')'.repeat(openCount);
  }

  function evaluateExpression(exprStr) {
    if (!exprStr || !exprStr.trim()) return 0;
    const closedExpr = autoCloseParentheses(exprStr.trim());
    const tokens = tokenize(closedExpr);
    return evaluateTokens(tokens);
  }

  function updatePreview() {
    const text = calcInput.value.trim();
    if (!text) {
      previewLine.textContent = '';
      return;
    }
    try {
      const res = evaluateExpression(text);
      if (typeof res === 'number' && !isNaN(res)) {
        previewLine.textContent = '≈ ' + res.toLocaleString('en-US', { maximumFractionDigits: 8 });
      } else {
        previewLine.textContent = '';
      }
    } catch (e) {
      previewLine.textContent = '';
    }
  }

  // Execute Calculation (Enter / =)
  function executeCalculation() {
    const expr = calcInput.value.trim();
    if (!expr) return;

    playClick(1200, 'triangle');

    try {
      const normalizedExpr = autoCloseParentheses(expr);
      const result = evaluateExpression(normalizedExpr);
      if (typeof result !== 'number' || isNaN(result)) {
        throw new Error('Calculation error');
      }

      lastAnswer = result;
      prevExprLine.textContent = normalizedExpr + ' =';

      evalResult.classList.remove('error');
      evalResult.textContent = result.toLocaleString('en-US', { maximumFractionDigits: 10 });
      evalResult.classList.add('pulse');
      setTimeout(() => evalResult.classList.remove('pulse'), 200);

      addHistory(normalizedExpr, result);
      evaluatedJustNow = true;
      previewLine.textContent = '';
    } catch (err) {
      evalResult.classList.add('error');
      evalResult.textContent = err.message || 'Error';
      playClick(300, 'sawtooth');
    }
    ensureFocus();
  }

  // Physical Keyboard Listener
  calcInput.addEventListener('keydown', (e) => {
    highlightKey(e.key);

    if (e.key === 'Enter' || e.key === '=') {
      e.preventDefault();
      executeCalculation();
      return;
    }

    if (e.key === 'Escape') {
      e.preventDefault();
      clearAll();
      playClick(500);
      return;
    }

    if (e.key === 'Backspace') {
      e.preventDefault();
      handleBackspace();
      playClick(700);
      return;
    }

    // If evaluated just now, handle operator vs new operand typing
    if (evaluatedJustNow) {
      if (['+', '-', '*', '/', '^', '%'].includes(e.key)) {
        calcInput.value = 'Ans';
      } else if (!['Control', 'Shift', 'Alt', 'Meta', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
        calcInput.value = '';
      }
      evaluatedJustNow = false;
    }

    // Keyboard scientific shortcuts
    if (!e.ctrlKey && !e.metaKey && !e.altKey) {
      if (e.key === 's') { e.preventDefault(); insertToken('sin('); playClick(); return; }
      if (e.key === 'c') { e.preventDefault(); insertToken('cos('); playClick(); return; }
      if (e.key === 't') { e.preventDefault(); insertToken('tan('); playClick(); return; }
      if (e.key === 'l') { e.preventDefault(); insertToken('ln('); playClick(); return; }
      if (e.key === 'L') { e.preventDefault(); insertToken('log('); playClick(); return; }
      if (e.key === 'p' || e.key === 'P') { e.preventDefault(); insertToken('π'); playClick(); return; }
      if (e.key === 'r' || e.key === 'v') { e.preventDefault(); insertToken('sqrt('); playClick(); return; }
      if (e.key === 'd' || e.key === 'D') { e.preventDefault(); toggleDegRad(); playClick(); return; }
    }

    playClick(850);
    setTimeout(updatePreview, 10);
  });

  calcInput.addEventListener('input', updatePreview);

  // Global window keyboard listener to capture keystrokes even if focus shifted
  window.addEventListener('keydown', (e) => {
    if (document.activeElement !== calcInput && !helpModal.classList.contains('open')) {
      ensureFocus();
    }
  });

  // Visual button keypress highlight
  function highlightKey(key) {
    let selector = '';
    if (key === 'Enter' || key === '=') selector = 'button[data-val="="]';
    else if (key === 'Escape') selector = 'button[data-val="AC"]';
    else if (key === 'Backspace') selector = 'button[data-val="DEL"]';
    else if (['+', '-', '*', '/', '%', '(', ')', '^', '.'].includes(key)) selector = `button[data-val="${key}"]`;
    else if (/[0-9]/.test(key)) selector = `button[data-val="${key}"]`;

    if (selector) {
      const btn = document.querySelector(selector);
      if (btn) {
        btn.classList.add('key-pressed');
        setTimeout(() => btn.classList.remove('key-pressed'), 120);
      }
    }
  }

  // Keypad click handler
  document.getElementById('keypad').addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;

    const val = btn.getAttribute('data-val');
    playClick(900);

    if (val === '=') {
      executeCalculation();
    } else if (val === 'AC') {
      clearAll();
    } else if (val === 'DEL') {
      deleteOne();
    } else if (val === 'deg_toggle') {
      toggleDegRad();
    } else if (val === '2nd_toggle') {
      toggle2nd();
    } else if (val === '+/-') {
      toggleSign();
    } else if (['MC', 'MR', 'M+', 'M-'].includes(val)) {
      handleMemory(val);
    } else if (val === '1/') {
      insertToken('1/(');
    } else if (val === '10^') {
      insertToken('10^(');
    } else {
      insertToken(val);
    }

    ensureFocus();
  });

  // Control buttons
  btnDegToggle.addEventListener('click', () => {
    toggleDegRad();
    playClick();
  });

  btnAudioToggle.addEventListener('click', () => {
    soundEnabled = !soundEnabled;
    btnAudioToggle.textContent = soundEnabled ? '🔊 Sound' : '🔇 Muted';
    btnAudioToggle.classList.toggle('active', soundEnabled);
    showToast(soundEnabled ? 'Audio feedback ON' : 'Audio feedback MUTED');
    ensureFocus();
  });

  btnHistoryToggle.addEventListener('click', () => {
    historyDrawer.classList.toggle('open');
    btnHistoryToggle.classList.toggle('active', historyDrawer.classList.contains('open'));
    ensureFocus();
  });

  btnClearHistory.addEventListener('click', () => {
    historyTape = [];
    try { localStorage.removeItem('calc_history'); } catch(e) {}
    renderHistory();
    showToast('History Cleared');
    ensureFocus();
  });

  btnCopy.addEventListener('click', () => {
    const textToCopy = evalResult.textContent;
    if (textToCopy && textToCopy !== 'Error' && textToCopy !== '0') {
      copyToClipboard(textToCopy);
    } else if (calcInput.value) {
      copyToClipboard(calcInput.value);
    }
    ensureFocus();
  });

  // Keyboard Help Modal Toggle
  document.getElementById('btn-theme-help').addEventListener('click', () => {
    helpModal.classList.add('open');
  });

  btnCloseHelp.addEventListener('click', () => {
    helpModal.classList.remove('open');
    ensureFocus();
  });

  helpModal.addEventListener('click', (e) => {
    if (e.target === helpModal) {
      helpModal.classList.remove('open');
      ensureFocus();
    }
  });
</script>
</body>
</html>
"""

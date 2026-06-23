"""
AHP Decision Tool - Streamlit Web App
======================================
A friendly, step-by-step decision-making tool based on the
Analytic Hierarchy Process (AHP) by Thomas Saaty.
"""

import csv
import io

import numpy as np
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────
# Page config (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Decision Maker · AHP Tool",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --ink:       #1a1a2e;
  --slate:     #3d405b;
  --steel:     #6b7280;
  --fog:       #e8eaf0;
  --snow:      #f9f9fb;
  --white:     #ffffff;
  --teal:      #0d9488;
  --teal-lt:   #ccfbf1;
  --amber:     #d97706;
  --amber-lt:  #fef3c7;
  --red-lt:    #fee2e2;
  --red:       #dc2626;
  --radius:    10px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { max-width: 860px; padding: 2rem 2rem 4rem; }

.hero {
  background: linear-gradient(135deg, var(--ink) 0%, var(--slate) 100%);
  border-radius: 16px;
  padding: 2.6rem 2.4rem 2.2rem;
  margin-bottom: 2rem;
  color: var(--white);
}
.hero-eyebrow {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--teal-lt);
  margin-bottom: 0.5rem;
}
.hero h1 {
  font-family: 'DM Serif Display', serif;
  font-size: clamp(1.9rem, 4vw, 2.8rem);
  font-weight: 400;
  line-height: 1.15;
  margin: 0 0 0.85rem;
}
.hero p {
  font-size: 1rem;
  font-weight: 300;
  line-height: 1.65;
  color: rgba(255,255,255,0.82);
  max-width: 540px;
  margin: 0;
}

.step-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.8rem; }
.step-pill {
  display: inline-flex; align-items: center; gap: 0.42rem;
  padding: 0.35rem 0.9rem; border-radius: 99px; font-size: 0.78rem;
  font-weight: 500; border: 1.5px solid var(--fog);
  color: var(--steel); background: var(--snow);
}
.step-pill.active { background: var(--ink); color: var(--white); border-color: var(--ink); }
.step-pill.done   { background: var(--teal-lt); color: var(--teal); border-color: var(--teal); }

.card {
  background: var(--white); border: 1.5px solid var(--fog);
  border-radius: var(--radius); padding: 1.5rem 1.6rem; margin-bottom: 1.2rem;
}
.card-title {
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--steel); margin-bottom: 0.7rem;
}
.card h3 {
  font-family: 'DM Serif Display', serif; font-size: 1.25rem;
  font-weight: 400; color: var(--ink); margin: 0 0 0.5rem;
}

.scale-strip { display: flex; gap: 0.3rem; flex-wrap: wrap; margin: 0.6rem 0 1.2rem; }
.scale-chip {
  padding: 0.22rem 0.6rem; border-radius: 6px; font-size: 0.72rem;
  font-family: 'JetBrains Mono', monospace; font-weight: 600;
  background: var(--fog); color: var(--slate);
}
.scale-chip.hi { background: var(--ink); color: var(--white); }

.compare-box {
  background: var(--snow); border: 1.5px solid var(--fog);
  border-radius: var(--radius); padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.compare-label {
  font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--steel); margin-bottom: 0.35rem;
}
.compare-vs { font-size: 1rem; font-weight: 500; color: var(--ink); }

.banner {
  padding: 0.8rem 1.1rem; border-radius: 0;
  font-size: 0.88rem; font-weight: 500; margin: 0.6rem 0;
  border-left: 4px solid;
}
.banner.ok   { background: var(--teal-lt);  color: #065f46; border-color: var(--teal); }
.banner.warn { background: var(--amber-lt); color: #92400e; border-color: var(--amber); }
.banner.err  { background: var(--red-lt);   color: #7f1d1d; border-color: var(--red); }

.result-row {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.85rem 1.1rem; border-radius: var(--radius);
  border: 1.5px solid var(--fog); margin-bottom: 0.6rem; background: var(--white);
}
.result-row.winner { border-color: var(--teal); background: var(--teal-lt); }
.rank-badge {
  width: 2rem; height: 2rem; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
  font-weight: 600; flex-shrink: 0; background: var(--fog); color: var(--slate);
}
.rank-badge.gold { background: #fbbf24; color: var(--white); }
.result-name { font-weight: 600; color: var(--ink); flex: 1; }
.result-bar-wrap { flex: 2; }
.result-bar-bg { height: 8px; background: var(--fog); border-radius: 99px; overflow: hidden; }
.result-bar-fill { height: 100%; border-radius: 99px; background: var(--teal); }
.result-pct {
  font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
  font-weight: 600; color: var(--ink); width: 4rem; text-align: right;
}

div[data-testid="stNumberInput"] > label,
div[data-testid="stSelectbox"] > label,
div[data-testid="stSlider"] > label { font-weight: 500; color: var(--ink); font-size: 0.88rem; }
div[data-testid="stButton"] > button {
  border-radius: 8px; font-weight: 600; font-size: 0.9rem; padding: 0.5rem 1.4rem;
}
div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--ink); border: none; color: var(--white);
}
div[data-testid="stButton"] > button[kind="primary"]:hover { background: var(--slate); }
hr { border-color: var(--fog); margin: 1.4rem 0; }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# AHP math (pure, no I/O)
# ─────────────────────────────────────────────
RI_TABLE = {
    1: 0.00, 2: 0.00, 3: 0.58,  4: 0.90,  5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41,  9: 1.45, 10: 1.49,
   11: 1.51,12: 1.48,13: 1.56, 14: 1.57, 15: 1.59,
}

SCALE_LABELS = {
    1: "Equal",           2: "Equal–Moderate",      3: "Moderate",
    4: "Moderate–Strong", 5: "Strong",               6: "Strong–Very Strong",
    7: "Very Strong",     8: "Very Strong–Extreme",  9: "Extreme",
}

PLACEHOLDER = "— select one —"


def random_index(n: int) -> float:
    return RI_TABLE.get(n, 1.98 * (n - 2) / n)


def build_matrix(n: int, upper: dict) -> np.ndarray:
    m = np.ones((n, n), dtype=float)
    for (i, j), v in upper.items():
        m[i, j] = v
        m[j, i] = 1.0 / v
    return m


def priority_vector(matrix: np.ndarray):
    vals, vecs = np.linalg.eig(matrix)
    idx = int(np.argmax(np.abs(vals)))
    lmax = float(vals[idx].real)
    w = np.abs(vecs[:, idx].real)
    w /= w.sum()
    return w, lmax


def cr_stats(n: int, lmax: float):
    if n <= 2:
        return 0.0, 0.0, 0.0
    ci = max(0.0, (lmax - n) / (n - 1))
    ri = random_index(n)
    cr = ci / ri if ri else 0.0
    return ci, ri, cr


# ─────────────────────────────────────────────
# Session-state bootstrap
# ─────────────────────────────────────────────
STEPS = ["Setup", "Your Options", "Your Factors", "Rank Factors", "Rank Options", "Results"]

defaults = dict(
    step=0,
    n_criteria=2,
    n_alts=2,
    criteria=[],
    alternatives=[],
    criteria_weights=None,
    alt_weight_matrix=None,
    final_scores=None,
    criteria_cr=None,
    alt_crs=None,
    current_alt_criterion=0,
)
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def go(step: int):
    st.session_state.step = step


# ─────────────────────────────────────────────
# Reusable UI helpers
# ─────────────────────────────────────────────
def render_hero():
    st.markdown(
        """
<div class="hero">
  <div class="hero-eyebrow">Structured Decision-Making</div>
  <h1>Which option is best<br>for your situation?</h1>
  <p>Answer a few simple comparison questions and this tool
     calculates a ranked score for each of your options —
     grounded in logic, not gut feel.</p>
</div>
""",
        unsafe_allow_html=True,
    )


def render_steps(current: int):
    pills = ""
    for i, label in enumerate(STEPS):
        if i < current:
            cls, icon = "done", "✓"
        elif i == current:
            cls, icon = "active", str(i + 1)
        else:
            cls, icon = "", str(i + 1)
        pills += f'<span class="step-pill {cls}">{icon} {label}</span>'
    st.markdown(f'<div class="step-row">{pills}</div>', unsafe_allow_html=True)


def cr_banner(cr: float) -> str:
    if cr <= 0.05:
        return '<div class="banner ok">✓ Your choices are logically consistent — no contradictions detected.</div>'
    if cr <= 0.10:
        return '<div class="banner warn">⚠ Minor tension in your choices — they are mostly consistent but may have a small contradiction. You can still proceed.</div>'
    return '<div class="banner err">✗ Your choices appear to contradict each other — for example, preferring A over B, B over C, but also C over A. Consider going back and reviewing your answers.</div>'


def scale_strip():
    chips = "".join(
        f'<span class="scale-chip {"hi" if k in (1, 5, 9) else ""}">{k} – {v}</span>'
        for k, v in SCALE_LABELS.items()
    )
    st.markdown(
        f'<div class="card-title" style="margin-top:0.6rem">Strength scale</div>'
        f'<div class="scale-strip">{chips}</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# STEP 0 — Setup
# ─────────────────────────────────────────────
def step_setup():
    render_hero()
    render_steps(0)

    st.markdown(
        """
<div class="card">
  <div class="card-title">How it works</div>
  <h3>Three easy phases</h3>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
<div class="card">
  <div class="card-title">Phase 1</div>
  <strong>Name your options</strong>
  <p style="font-size:0.88rem;color:#6b7280;margin-top:0.4rem">
    Add all the choices you are deciding between — e.g. Vendor A, Option B.
  </p>
</div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
<div class="card">
  <div class="card-title">Phase 2</div>
  <strong>Set your factors</strong>
  <p style="font-size:0.88rem;color:#6b7280;margin-top:0.4rem">
    Name the things that matter most to you — cost, quality, speed, etc.
  </p>
</div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
<div class="card">
  <div class="card-title">Phase 3</div>
  <strong>Answer comparisons</strong>
  <p style="font-size:0.88rem;color:#6b7280;margin-top:0.4rem">
    Pick which is more important, and by how much. We do the math.
  </p>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Options on the LEFT, factors on the RIGHT
    c1, c2 = st.columns(2)
    with c1:
        n_alts_input = st.number_input(
            "How many things are you choosing between?",
            min_value=2,
            max_value=20,
            value=st.session_state.n_alts,
            step=1,
            help="These are the actual choices you want to rank — e.g. Vendor A, Option B, doing it in-house.",
        )
        st.caption("These are the actual choices you want to rank.")
    with c2:
        n_crit_input = st.number_input(
            "How many factors will you judge them on?",
            min_value=2,
            max_value=15,
            value=st.session_state.n_criteria,
            step=1,
            help="These are the things that matter to you — e.g. Cost, Quality, Speed, Ease of use.",
        )
        st.caption("These are the things that matter to you, e.g. cost, quality, speed.")

    st.markdown("<br>", unsafe_allow_html=True)

    ready = n_alts_input >= 2 and n_crit_input >= 2

    if st.button("Let's start →", type="primary", disabled=not ready):
        st.session_state.n_alts = int(n_alts_input)
        st.session_state.n_criteria = int(n_crit_input)
        st.session_state.criteria = []
        st.session_state.alternatives = []
        st.session_state.criteria_weights = None
        st.session_state.alt_weight_matrix = None
        st.session_state.final_scores = None
        st.session_state.criteria_cr = None
        st.session_state.alt_crs = None
        st.session_state.current_alt_criterion = 0
        go(1)
        st.rerun()


# ─────────────────────────────────────────────
# STEP 1 — Name options (alternatives) — FIRST
# ─────────────────────────────────────────────
def step_name_alternatives():
    render_steps(1)
    st.markdown(
        """
<div class="card">
  <div class="card-title">Step 1 of 4</div>
  <h3>What are you choosing between?</h3>
  <p style="color:#6b7280;font-size:0.9rem;margin:0">
    Name each option you are deciding between.
    <em>Examples: Vendor A, In-house build, Option C.</em>
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    n = st.session_state.n_alts
    alts = []
    for i in range(n):
        default = st.session_state.alternatives[i] if i < len(st.session_state.alternatives) else ""
        val = st.text_input(
            f"Option {i + 1}",
            value=default,
            placeholder=f"e.g. Option {chr(65 + i) if i < 26 else f'Option {i+1}'}",
            key=f"alt_input_{i}",
        )
        alts.append(val.strip())

    all_filled = all(alts) and len(set(alts)) == n
    if not all_filled and any(alts):
        st.warning("Please fill in all options with unique names before continuing.")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            go(0); st.rerun()
    with col2:
        if st.button("Next →", type="primary", disabled=not all_filled):
            st.session_state.alternatives = alts
            go(2); st.rerun()


# ─────────────────────────────────────────────
# STEP 2 — Name factors (criteria) — SECOND
# ─────────────────────────────────────────────
def step_name_criteria():
    render_steps(2)
    st.markdown(
        """
<div class="card">
  <div class="card-title">Step 2 of 4</div>
  <h3>What factors will you judge your options on?</h3>
  <p style="color:#6b7280;font-size:0.9rem;margin:0">
    Name each factor that matters to you when making this decision.
    <em>Examples: Cost, Quality, Speed, Sustainability, Ease of use.</em>
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    placeholders = ["Cost", "Quality", "Speed", "Reliability", "Ease of use",
                    "Flexibility", "Support", "Scalability", "Risk", "Time to implement"]
    n = st.session_state.n_criteria
    criteria = []
    for i in range(n):
        default = st.session_state.criteria[i] if i < len(st.session_state.criteria) else ""
        val = st.text_input(
            f"Factor {i + 1}",
            value=default,
            placeholder=f"e.g. {placeholders[i] if i < len(placeholders) else f'Factor {i+1}'}",
            key=f"crit_input_{i}",
        )
        criteria.append(val.strip())

    all_filled = all(criteria) and len(set(criteria)) == n
    if not all_filled and any(criteria):
        st.warning("Please fill in all factors with unique names before continuing.")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            go(1); st.rerun()
    with col2:
        if st.button("Next →", type="primary", disabled=not all_filled):
            st.session_state.criteria = criteria
            go(3); st.rerun()


# ─────────────────────────────────────────────
# STEP 3 — Rank factors (criteria)
# ─────────────────────────────────────────────
def step_rank_criteria():
    render_steps(3)
    criteria = st.session_state.criteria
    n = len(criteria)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]

    st.markdown(
        f"""
<div class="card">
  <div class="card-title">Step 3 of 4 · {len(pairs)} comparison{"s" if len(pairs) != 1 else ""}</div>
  <h3>Which factors matter more to you?</h3>
  <p style="color:#6b7280;font-size:0.9rem;margin:0">
    For each pair below, pick which factor is more important to you — and how much more.
    If they matter equally, choose "They matter equally."
  </p>
</div>
""",
        unsafe_allow_html=True,
    )
    scale_strip()

    upper = {}
    all_answered = True
    for i, j in pairs:
        left, right = criteria[i], criteria[j]
        with st.container():
            st.markdown(
                f'<div class="compare-box"><div class="compare-label">Comparison</div>'
                f'<div class="compare-vs">⚖️ <strong>{left}</strong> vs <strong>{right}</strong></div></div>',
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                winner = st.selectbox(
                    "Which matters more?",
                    options=[PLACEHOLDER, "They matter equally", left, right],
                    index=0,
                    key=f"crit_winner_{i}_{j}",
                )
            with c2:
                strength = st.select_slider(
                    "How much more?",
                    options=list(range(1, 10)),
                    value=1,
                    key=f"crit_strength_{i}_{j}",
                    disabled=(winner in (PLACEHOLDER, "They matter equally")),
                )

            if winner == PLACEHOLDER:
                all_answered = False
            elif winner == "They matter equally":
                upper[(i, j)] = 1.0
            elif winner == left:
                upper[(i, j)] = float(strength)
            else:
                upper[(i, j)] = 1.0 / float(strength)

    # Only show consistency banner once all pairs are answered
    if all_answered and len(upper) == len(pairs):
        matrix = build_matrix(n, upper)
        weights, lmax = priority_vector(matrix)
        ci, ri, cr = cr_stats(n, lmax)
        st.markdown(cr_banner(cr), unsafe_allow_html=True)
        with st.expander("See how your factors were weighted"):
            df = pd.DataFrame({"Factor": criteria, "Weight": [f"{w*100:.1f}%" for w in weights]})
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        matrix, weights, lmax, cr = None, None, None, None

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            go(2); st.rerun()  # goes back to step 2: name factors
    with col2:
        if st.button("Save & continue →", type="primary", disabled=not all_answered):
            if weights is not None:
                st.session_state.criteria_weights = weights
                st.session_state.criteria_cr = cr
                st.session_state.current_alt_criterion = 0
                st.session_state.alt_weight_matrix = np.zeros((st.session_state.n_alts, n))
                go(4)
                st.rerun()


# ─────────────────────────────────────────────
# STEP 4 — Rank options per factor
# ─────────────────────────────────────────────
def step_rank_alternatives():
    render_steps(4)
    criteria = st.session_state.criteria
    alternatives = st.session_state.alternatives
    n_alts = len(alternatives)
    n_crit = len(criteria)
    c_idx = st.session_state.current_alt_criterion
    criterion = criteria[c_idx]

    pairs = [(i, j) for i in range(n_alts) for j in range(i + 1, n_alts)]

    st.markdown(
        f"""
<div class="card">
  <div class="card-title">Step 4 of 4 · Factor {c_idx+1} of {n_crit}</div>
  <h3>Comparing your options for: <em>{criterion}</em></h3>
  <p style="color:#6b7280;font-size:0.9rem;margin:0">
    For each pair of options, decide which one performs better when it comes to
    <strong>{criterion}</strong>, and by how much.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )
    scale_strip()

    upper = {}
    all_answered = True
    for i, j in pairs:
        left, right = alternatives[i], alternatives[j]
        with st.container():
            st.markdown(
                f'<div class="compare-box"><div class="compare-label">For: {criterion}</div>'
                f'<div class="compare-vs">⚖️ <strong>{left}</strong> vs <strong>{right}</strong></div></div>',
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                winner = st.selectbox(
                    "Which performs better?",
                    options=[PLACEHOLDER, "They perform equally", left, right],
                    index=0,
                    key=f"alt_winner_{c_idx}_{i}_{j}",
                )
            with c2:
                strength = st.select_slider(
                    "How much better?",
                    options=list(range(1, 10)),
                    value=1,
                    key=f"alt_strength_{c_idx}_{i}_{j}",
                    disabled=(winner in (PLACEHOLDER, "They perform equally")),
                )

            if winner == PLACEHOLDER:
                all_answered = False
            elif winner == "They perform equally":
                upper[(i, j)] = 1.0
            elif winner == left:
                upper[(i, j)] = float(strength)
            else:
                upper[(i, j)] = 1.0 / float(strength)

    # Only show consistency banner once all pairs are answered
    if all_answered and len(upper) == len(pairs):
        matrix = build_matrix(n_alts, upper)
        weights, lmax = priority_vector(matrix)
        ci, ri, cr = cr_stats(n_alts, lmax)
        st.markdown(cr_banner(cr), unsafe_allow_html=True)
    else:
        matrix, weights, lmax, cr = None, None, None, None

    is_last = c_idx == n_crit - 1
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            if c_idx == 0:
                go(3)
            else:
                st.session_state.current_alt_criterion -= 1
            st.rerun()
    with col2:
        label = "Calculate results →" if is_last else f"Next factor ({c_idx+2}/{n_crit}) →"
        if st.button(label, type="primary", disabled=not all_answered):
            if weights is not None:
                st.session_state.alt_weight_matrix[:, c_idx] = weights
                if st.session_state.alt_crs is None:
                    st.session_state.alt_crs = {}
                st.session_state.alt_crs[c_idx] = cr
                if is_last:
                    final = st.session_state.alt_weight_matrix @ st.session_state.criteria_weights
                    st.session_state.final_scores = final
                    go(5)
                else:
                    st.session_state.current_alt_criterion += 1
                st.rerun()


# ─────────────────────────────────────────────
# STEP 5 — Results
# ─────────────────────────────────────────────
def step_results():
    render_steps(5)
    alternatives = st.session_state.alternatives
    criteria = st.session_state.criteria
    criteria_weights = st.session_state.criteria_weights
    alt_matrix = st.session_state.alt_weight_matrix
    scores = st.session_state.final_scores

    ranked_idx = np.argsort(-scores)
    winner = alternatives[ranked_idx[0]]
    winner_score = scores[ranked_idx[0]]

    st.markdown(
        f"""
<div class="card" style="border-color:#0d9488;background:#f0fdf9">
  <div class="card-title" style="color:#0d9488">Recommendation</div>
  <h3 style="font-size:1.6rem;margin-bottom:0.2rem">🏆 {winner}</h3>
  <p style="color:#065f46;font-size:0.9rem;margin:0">
    Scored highest overall at <strong>{winner_score*100:.1f}%</strong>
    across all your factors and their weights.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("#### All options, ranked")
    max_score = scores.max()
    for rank, idx in enumerate(ranked_idx):
        alt = alternatives[idx]
        sc = scores[idx]
        bar_pct = int(sc / max_score * 100) if max_score else 0
        row_cls = "result-row winner" if rank == 0 else "result-row"
        badge_cls = "rank-badge gold" if rank == 0 else "rank-badge"
        st.markdown(
            f"""
<div class="{row_cls}">
  <div class="{badge_cls}">{rank+1}</div>
  <div class="result-name">{alt}</div>
  <div class="result-bar-wrap">
    <div class="result-bar-bg">
      <div class="result-bar-fill" style="width:{bar_pct}%"></div>
    </div>
  </div>
  <div class="result-pct">{sc*100:.1f}%</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    with st.expander("📊 How much each factor was weighted"):
        df_crit = pd.DataFrame({
            "Factor": criteria,
            "Weight": [f"{w*100:.1f}%" for w in criteria_weights],
        })
        st.dataframe(df_crit, use_container_width=True, hide_index=True)

    with st.expander("📋 Full score breakdown per factor"):
        data = {c: [f"{alt_matrix[i, j]*100:.1f}%" for i in range(len(alternatives))]
                for j, c in enumerate(criteria)}
        data["Final Score"] = [f"{scores[i]*100:.1f}%" for i in range(len(alternatives))]
        df_full = pd.DataFrame(data, index=alternatives)
        st.dataframe(df_full, use_container_width=True)

    with st.expander("🔍 Logical consistency summary"):
        cr_crit = st.session_state.criteria_cr or 0
        rows = [{
            "Phase": "Factor comparisons",
            "Status": "✓ Consistent" if cr_crit <= 0.10 else "⚠ Contradictions detected",
        }]
        for c_idx, criterion in enumerate(criteria):
            cr_val = (st.session_state.alt_crs or {}).get(c_idx, 0)
            rows.append({
                "Phase": f"Options on: {criterion}",
                "Status": "✓ Consistent" if cr_val <= 0.10 else "⚠ Contradictions detected",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Download results")
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["AHP Decision Results"])
    writer.writerow([])
    writer.writerow(["Factor", "Weight (%)"])
    for c, w in zip(criteria, criteria_weights):
        writer.writerow([c, f"{w*100:.2f}"])
    writer.writerow([])
    header = ["Option"] + [f"{c} (%)" for c in criteria] + ["Final Score (%)", "Rank"]
    writer.writerow(header)
    rank_map = {idx: r + 1 for r, idx in enumerate(ranked_idx)}
    for i, alt in enumerate(alternatives):
        row = (
            [alt]
            + [f"{alt_matrix[i, j]*100:.2f}" for j in range(len(criteria))]
            + [f"{scores[i]*100:.2f}", rank_map[i]]
        )
        writer.writerow(row)

    st.download_button(
        "⬇ Download CSV",
        data=buf.getvalue(),
        file_name="ahp_results.csv",
        mime="text/csv",
        type="primary",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start a new decision"):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()


# ─────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────
STEP_FNS = [
    step_setup,
    step_name_alternatives,  # Step 1: name your options first
    step_name_criteria,      # Step 2: name your factors
    step_rank_criteria,      # Step 3: rank factors
    step_rank_alternatives,  # Step 4: rank options per factor
    step_results,
]

STEP_FNS[st.session_state.step]()

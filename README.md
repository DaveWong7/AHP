# ⚖️ AHP Decision Maker

A clean, interactive web app that walks you through the **Analytic Hierarchy Process (AHP)** — a proven structured decision-making method — without any jargon or math.

Built with [Streamlit](https://streamlit.io).

---

## What it does

1. **Name your criteria** — the things that matter to you (cost, quality, speed…)
2. **Name your options** — the choices you're deciding between (2–5 options)
3. **Answer pairwise comparisons** — simple "which is better and by how much?" questions
4. **Get a ranked result** — with a consistency check and full score breakdown

---

## Run locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ahp-decision-tool.git
cd ahp-decision-tool

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deploy to Streamlit Community Cloud (free)

1. Push this repo to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set **Main file path** to `app.py`
4. Click **Deploy** — your app will be live in ~60 seconds

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | The entire Streamlit application |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

---

## Method

This tool implements Saaty's AHP using the **principal eigenvector method** for priority weights and the standard **Consistency Ratio (CR)** check (threshold: 10%). The math is identical to the reference implementation — only the interface has changed.

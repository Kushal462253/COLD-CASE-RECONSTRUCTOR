import streamlit as st
import os
import random
import json
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, "groq_api.env"))

from chains import run_pipeline, analyse_personal_theory

HISTORY_FILE = os.path.join(base_dir, "history.json")

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)
    except:
        pass

st.set_page_config(
    page_title="Cold Case Reconstructor",
    page_icon="🕵️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0a;
    color: #e8e8e8;
}
.main { background-color: #0a0a0a; }
.block-container { padding: 2rem 2rem 2rem 2rem; }
h1 {
    font-family: 'Playfair Display', serif;
    color: #c9a84c;
    font-size: 2.2rem;
    letter-spacing: 4px;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 0;
}
.subtitle {
    font-family: 'Share Tech Mono', monospace;
    color: #555;
    text-align: center;
    font-size: 0.7rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.divider { border: none; border-top: 1px solid #c9a84c22; margin: 1rem 0; }
.panel {
    background: #111;
    border: 1px solid #c9a84c22;
    border-left: 2px solid #c9a84c;
    padding: 1rem;
    margin-bottom: 1rem;
}
.panel-title {
    font-family: 'Share Tech Mono', monospace;
    color: #c9a84c;
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.history-item {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    color: #555;
    padding: 0.35rem 0;
    border-bottom: 1px solid #c9a84c11;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.facts-box {
    background: #0f0f0f;
    border-left: 2px solid #c9a84c;
    padding: 0.75rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #666;
    line-height: 1.7;
    margin-bottom: 1rem;
}
.section-title {
    font-family: 'Share Tech Mono', monospace;
    color: #c9a84c;
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.theory-card {
    background: #111;
    border: 1px solid #c9a84c22;
    border-top: 2px solid #c9a84c;
    padding: 0.75rem;
}
.theory-num {
    font-family: 'Share Tech Mono', monospace;
    color: #c9a84c;
    font-size: 0.6rem;
    letter-spacing: 2px;
}
.theory-score {
    font-family: 'Playfair Display', serif;
    color: #c9a84c;
    font-size: 1.6rem;
    font-weight: 700;
}
.theory-bar-bg { height: 3px; background: #222; margin: 0.4rem 0; }
.verdict-box {
    background: #111;
    border: 1px solid #c9a84c;
    padding: 1.25rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: #888;
    line-height: 1.8;
}
.await-box {
    height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #c9a84c11;
    background: #0a0a0a;
    flex-direction: column;
    gap: 1rem;
}
.await-icon { font-size: 3rem; opacity: 0.15; }
.await-text {
    font-family: 'Share Tech Mono', monospace;
    color: #2a2a2a;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-align: center;
}
.await-sub {
    font-family: 'Share Tech Mono', monospace;
    color: #1a1a1a;
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-align: center;
}
.stButton > button {
    background: transparent;
    border: 1px solid #c9a84c;
    color: #c9a84c;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0.6rem;
    font-size: 0.7rem;
    width: 100%;
    transition: all 0.2s ease;
}
.stButton > button:hover { background: #c9a84c; color: #0a0a0a; }
.stTextArea textarea {
    background-color: #0f0f0f;
    border: 1px solid #c9a84c33;
    color: #e8e8e8;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
}
.stTextArea textarea:focus {
    border-color: #c9a84c;
    box-shadow: 0 0 0 1px #c9a84c;
}
.stTextArea label {
    font-family: 'Share Tech Mono', monospace;
    color: #c9a84c;
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.stExpander { background: #0f0f0f; border: 1px solid #c9a84c22; }
</style>
""", unsafe_allow_html=True)

FAMOUS_CASES = [
    "D.B. Cooper hijacking 1971",
    "Subhas Chandra Bose disappearance 1945",
    "Jack the Ripper murders London 1888",
    "Zodiac Killer San Francisco 1960s",
    "Amelia Earhart disappearance 1937",
    "Black Dahlia murder Los Angeles 1947",
    "Bermuda Triangle disappearances",
    "Tamam Shud mystery Australia 1948",
]

if "history" not in st.session_state:
    st.session_state["history"] = load_history()
if "prefill" not in st.session_state:
    st.session_state["prefill"] = ""

st.markdown("<h1>🕵️ Cold Case Reconstructor</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Investigative Intelligence System</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown('<div class="panel-title">Case Input</div>', unsafe_allow_html=True)

    case_input = st.text_area(
        "",
        value=st.session_state["prefill"],
        placeholder="Enter details of an unsolved or historical case...",
        height=140,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        reconstruct_btn = st.button("⚡ Reconstruct")
    with col_b:
        if st.button("🎲 Random"):
            st.session_state["prefill"] = random.choice(FAMOUS_CASES)
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Famous Unsolved Cases</div>', unsafe_allow_html=True)

    for case in FAMOUS_CASES:
        if st.button(case, key=f"btn_{case}"):
            st.session_state["prefill"] = case
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Recent Cases</div>', unsafe_allow_html=True)
    if st.session_state.get("history"):
        for item in reversed(st.session_state["history"][-3:]):
            st.markdown(f'<div class="history-item">▸ {item}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="history-item" style="color:#222">No cases reconstructed yet</div>', unsafe_allow_html=True)

with right_col:
    if reconstruct_btn:
        if not case_input.strip():
            st.warning("Please enter case details.")
        else:
            try:
                with st.spinner("Retrieving evidence and reconstructing case..."):
                    result = run_pipeline(case_input)
            except Exception as e:
                st.error(f"⚠️ {str(e)}")
                st.stop()

            st.session_state["result"] = result
            st.session_state["case_input"] = case_input
            if case_input not in st.session_state["history"]:
                st.session_state["history"].append(case_input)
                save_history(st.session_state["history"])
            st.session_state["prefill"] = ""

    if "result" in st.session_state:
        result = st.session_state["result"]
        scores = result["scores"]
        score_list = list(scores.values())
        theories_list = result.get("theories_list", [])
        evidence_list = result.get("evidence_list", [])
        narratives_list = result.get("narratives_list", [])

        # ── FULL THEORY VIEW ─────────────────────────────
        if "active_theory" in st.session_state:
            i = st.session_state["active_theory"]

            st.markdown('<div style="padding: 0 1rem;">', unsafe_allow_html=True)

            if st.button("← Back to Case Overview"):
                del st.session_state["active_theory"]
                st.rerun()

            st.markdown(f'<div class="section-title">Theory 0{i+1} — Full Analysis</div>', unsafe_allow_html=True)
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            st.markdown("**THEORY**")
            st.write(theories_list[i] if i < len(theories_list) else result["theories"])

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("**EVIDENCE MAPPING**")
            st.write(evidence_list[i] if i < len(evidence_list) else result["evidence"])

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("**NARRATIVE**")
            st.write(narratives_list[i] if i < len(narratives_list) else result["narratives"])

            st.markdown('</div>', unsafe_allow_html=True)

        # ── MAIN OVERVIEW ────────────────────────────────
        else:
            st.markdown('<div class="section-title">📁 Retrieved Intelligence</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="facts-box">{result["retrieved_facts"]}</div>', unsafe_allow_html=True)
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            st.markdown('<div class="section-title">🧠 Reconstructed Theories</div>', unsafe_allow_html=True)
            t1, t2, t3 = st.columns(3)

            for i, col in enumerate([t1, t2, t3]):
                score = score_list[i]
                with col:
                    st.markdown(f'''
                    <div class="theory-card">
                        <div class="theory-num">Theory 0{i+1}</div>
                        <div class="theory-score">{score}<span style="font-size:0.8rem;color:#444">/100</span></div>
                        <div class="theory-bar-bg">
                            <div style="height:3px;background:#c9a84c;width:{int(score)}%"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    if st.button(f"Open Theory {i+1}", key=f"open_{i}"):
                        st.session_state["active_theory"] = i
                        st.rerun()

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⚖️ Final Verdict</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-box">{result["verdict"]}</div>', unsafe_allow_html=True)

            st.markdown('<br>', unsafe_allow_html=True)

            # PDF Download
            from utils import generate_pdf
            pdf_bytes = generate_pdf(st.session_state["case_input"], result)
            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_bytes,
                file_name="cold_case_report.pdf",
                mime="application/pdf"
            )
            

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🧠 Personal Theory Analyser</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family: Share Tech Mono, monospace; color: #555; font-size: 0.7rem; margin-bottom: 0.75rem;">Submit your own theory and let the AI evaluate it against retrieved facts</div>', unsafe_allow_html=True)

        user_theory = st.text_area(
            "",
            placeholder="Enter your own theory about what happened...",
            height=100,
            key="user_theory_input"
        )

        if st.button("⚡ Analyse My Theory", key="analyse_theory"):
            if not user_theory.strip():
                st.warning("Please enter your theory first.")
            else:
                try:
                    with st.spinner("Analysing your theory..."):
                        analysis = analyse_personal_theory(
                            st.session_state["case_input"],
                            user_theory,
                            result["retrieved_facts"],
                            result["theories"]
                        )
                    st.session_state["theory_analysis"] = analysis
                except Exception as e:
                    st.error(f"⚠️ {str(e)}")

        if "theory_analysis" in st.session_state:
            st.markdown(f'<div class="verdict-box">{st.session_state["theory_analysis"]}</div>', unsafe_allow_html=True)
            if st.button("↺ New Case"):
                st.session_state.pop("result", None)
                st.session_state.pop("case_input", None)
                st.session_state.pop("active_theory", None)
                st.session_state["prefill"] = ""
                st.rerun()

    else:
        st.markdown('''
        <div class="await-box">
            <div class="await-icon">🕵️</div>
            <div class="await-text">AWAITING CASE INPUT</div>
            <div class="await-sub">Select a case from the left or enter your own</div>
        </div>
        ''', unsafe_allow_html=True)
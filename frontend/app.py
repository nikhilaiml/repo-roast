import streamlit as st
import requests
import time
import os

# --- BACKEND URL FIX (Render wala) ---
try:
    BACKEND_URL = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))
except:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="RepoRoast — 【entity-GitHub¦canonical_name=GitHub】 Analyzer", page_icon="🔥", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #0d1117; color: #e6edf3; }
#MainMenu, footer, header { visibility: hidden; }
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
}
.card:hover { border-color: #484f58; }
.card-title { font-size: 13px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: #8b949e; margin-bottom: 12px; }
.metric-value { font-size: 28px; font-weight: 700; color: #e6edf3; }
.metric-label { font-size: 12px; color: #8b949e; margin-top: 4px; }
div[data-baseweb="input"] { background: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
div[data-baseweb="input"]:focus-within { border-color: #1f6feb !important; box-shadow: 0 0 0 3px rgba(31,111,235,0.3) !important; }
.stButton>button {
    background: #f5f5f5; color: #0d1117; border: 1px solid #30363d;
    border-radius: 8px; padding: 8px 20px; font-weight: 600; font-size: 14px;
}
.stButton>button:hover { background: #ffffff; border-color: #8b949e; }
.roast {
    border-left: 3px solid #f97316;
    background: #161b22;
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    font-size: 15px; line-height: 1.6;
}
.safe { border-color: #238636 !important; }
.risk { border-color: #da3633 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="max-width: 1100px; margin: 0 auto; padding: 32px 0 24px 0; border-bottom: 1px solid #21262d;">
    <div style="display:flex; align-items:center; justify-content:space-between;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:32px; height:32px; background:#fff; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#000; font-weight:800;">R</div>
            <span style="font-weight:700; font-size:18px;">RepoRoast</span>
            <span style="background:#21262d; border:1px solid #30363d; padding:2px 8px; border-radius:20px; font-size:11px; color:#8b949e; margin-left:8px;">BETA</span>
        </div>
        <div style="font-size:13px; color:#8b949e;">We roast your code, so your interviewer doesn't have to.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="max-width: 1100px; margin: 0 auto; padding-top: 32px;">', unsafe_allow_html=True)

c1, c2 = st.columns([4, 1])
with c1:
    repo_url = st.text_input("repo", placeholder="https://github.com/username/repository", label_visibility="collapsed")
with c2:
    roast_btn = st.button("Analyze →", use_container_width=True, type="primary")

st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)

if roast_btn and repo_url:
    try:
        with st.status("Analyzing repository...", expanded=False) as status:
            st.write("Fetching files from 【entity-GitHub¦canonical_name=GitHub】...")
            time.sleep(0.5)
            st.write("Running radon, lizard, security scan...")
            res = requests.get(f"{BACKEND_URL}/analyze?repo_url={repo_url}", timeout=90)
            data = res.json()
            status.update(label="Analysis complete", state="complete", expanded=False)

        if "detail" in data:
            st.error(data["detail"])
        else:
            score = data.get("score", data.get("health_score", 0))
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="card"><div class="card-title">Health Score</div><div class="metric-value">{score}/100</div><div class="metric-label">{"Excellent" if score>=80 else "Needs work" if score<50 else "Good"}</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="card"><div class="card-title">Stars</div><div class="metric-value">{data.get("stars",0)}</div><div class="metric-label">【entity-GitHub¦canonical_name=GitHub】</div></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="card"><div class="card-title">Files</div><div class="metric-value">{data.get("file_count",0)}</div><div class="metric-label">Python files</div></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="card"><div class="card-title">Lines</div><div class="metric-value">{data.get("total_lines",0)}</div><div class="metric-label">Total LOC</div></div>', unsafe_allow_html=True)

            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            repo_name = data.get("repo", repo_url.replace("https://github.com/", ""))
            roast_text = data.get("roast", {}).get("one_liner", "") if isinstance(data.get("roast"), dict) else str(data.get("roast",""))
            st.markdown(f'<div class="card"><div class="card-title">Roast — {repo_name}</div><div class="roast">{roast_text}</div></div>', unsafe_allow_html=True)
            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

            left, right = st.columns(2)
            with left:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Issues</div>', unsafe_allow_html=True)
                for i in data.get("issues", [])[:6] or ["No major issues"]:
                    st.markdown(f"<div style='font-size:13px; padding:6px 0; border-bottom:1px solid #21262d; color:#c9d1d9;'>• {i}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Bug Risks</div>', unsafe_allow_html=True)
                for b in data.get("bug_risks", [])[:6] or ["Low risk"]:
                    st.markdown(f"<div style='font-size:13px; padding:6px 0; border-bottom:1px solid #21262d; color:#c9d1d9;'>• {b}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                sec = data.get("security_report", [])
                is_safe = len(sec)==1 and "No major" in sec[0]
                sec_class = "safe" if is_safe else "risk" if len(sec)>0 and not is_safe else ""
                st.markdown(f'<div class="card {sec_class}">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">🔒 Security Scan — Phase 2</div>', unsafe_allow_html=True)
                for s in sec:
                    color = "#3fb950" if is_safe else "#f85149"
                    st.markdown(f"<div style='font-size:13px; padding:6px 0; border-bottom:1px solid #21262d; color:{color};'>• {s}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Improvements — AI</div>', unsafe_allow_html=True)
                tips = data.get("roast", {}).get("improvements", []) if isinstance(data.get("roast"), dict) else []
                for t in tips:
                    st.markdown(f"<div style='font-size:13px; padding:6px 0; border-bottom:1px solid #21262d; color:#c9d1d9;'>↳ {t}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Fixed Example</div>', unsafe_allow_html=True)
                fixed = data.get("roast", {}).get("fixed_example", "") if isinstance(data.get("roast"), dict) else ""
                st.code(fixed, language="python")
                st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Backend not running: {e}")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""
<div style="max-width:1100px; margin: 48px auto 0 auto; padding: 20px 0; border-top:1px solid #21262d; display:flex; justify-content:space-between; font-size:12px; color:#484f58;">
    <div>© 2026 RepoRoast — Python • FastAPI • Flint • Radon • Bandit</div>
    <div>Phase 1 Base Roaster • Phase 2 Security Scanner</div>
</div>
""", unsafe_allow_html=True)
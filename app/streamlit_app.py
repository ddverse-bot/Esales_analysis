import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import streamlit.components.v1 as components

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="E-Sales AI", layout="wide")

# -----------------------------
# 💎 PREMIUM THEME
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0b1020, #05070f);
    color: #e5e7eb;
}

h1, h2, h3 {
    color: #e0f2fe;
    text-shadow: 0 0 10px rgba(6,182,212,0.3);
}

label {
    color: #ffffff !important;
    font-weight: 500 !important;
}

input, textarea {
    color: #111827 !important;
    background-color: #ffffff !important;
    border-radius: 8px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1224, #060913);
}

.stButton > button {
    background: linear-gradient(90deg, #06b6d4, #8b5cf6);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    transform: scale(1.02);
    transition: 0.2s;
}

.feature-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(12px);
}

.feature-title {
    font-size: 18px;
    font-weight: 600;
    color: #e0f2fe;
}

.feature-text {
    font-size: 14px;
    color: rgba(255,255,255,0.7);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "logs" not in st.session_state:
    st.session_state["logs"] = pd.DataFrame(columns=[
        "timestamp", "price", "freight_value",
        "weight", "hour", "probability", "risk_level"
    ])

# -----------------------------
# LOAD MODEL + DATA
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/delivery_delay_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/esales_clean.csv")

model = load_model()
df = load_data()

# -----------------------------
# 🌐 ORB (FIXED + FULL WORKING)
# -----------------------------
particle_orb_html = """
<style>
#orb-container {
    position: relative;
    width: 100%;
    height: 760px;
    display: flex;
    justify-content: center;
    align-items: center;
}

canvas {
    width: 700px !important;
    height: 700px !important;
    opacity: 0.65;
    filter: drop-shadow(0 0 25px rgba(34,211,238,0.9))
            drop-shadow(0 0 60px rgba(139,92,246,0.4));
}
</style>

<div id="orb-container">
<canvas id="orb" width="700" height="700"></canvas>
</div>

<script>
const canvas = document.getElementById("orb");
const ctx = canvas.getContext("2d");

let time = 0;
const particles = [];
const numParticles = 1200;
const radius = 190;

for (let i = 0; i < numParticles; i++) {
    particles.push({
        theta: Math.acos(1 - 2 * (i / numParticles)),
        phi: Math.PI * (1 + Math.sqrt(5)) * i,
        baseR: radius
    });
}

function render() {
    time += 0.008;
    ctx.clearRect(0, 0, 700, 700);

    const cx = 350;
    const cy = 350;

    const rotationX = time * 0.15;
    const rotationY = time * 0.25;

    let rendered = particles.map(p => {
        let wave1 = Math.sin(p.theta * 4 + time * 2) * 12;
        let wave2 = Math.cos(p.phi * 2 + time * 1.5) * 10;
        let r = p.baseR + wave1 + wave2;

        let x = r * Math.sin(p.theta) * Math.cos(p.phi);
        let y = r * Math.sin(p.theta) * Math.sin(p.phi);
        let z = r * Math.cos(p.theta);

        let y1 = y * Math.cos(rotationX) - z * Math.sin(rotationX);
        let z1 = y * Math.sin(rotationX) + z * Math.cos(rotationX);

        let x2 = x * Math.cos(rotationY) + z1 * Math.sin(rotationY);
        let z2 = -x * Math.sin(rotationY) + z1 * Math.cos(rotationY);

        return {x: x2, y: y1, z: z2};
    });

    rendered.sort((a,b) => a.z - b.z);

    rendered.forEach(p => {
        let perspective = 800 / (800 - p.z);
        let sx = cx + p.x * perspective;
        let sy = cy + p.y * perspective;

        let size = Math.max(0.6, 1.8 * perspective);

        ctx.fillStyle = "#22d3ee";
        ctx.shadowBlur = 20;
        ctx.shadowColor = "#22d3ee";

        ctx.beginPath();
        ctx.arc(sx, sy, size, 0, Math.PI * 2);
        ctx.fill();
    });

    requestAnimationFrame(render);
}

render();
</script>
"""

def render_orb():
    components.html(particle_orb_html, height=800)

# -----------------------------
# HOME
# -----------------------------
if st.session_state.page == "home":

    st.markdown("<h1 style='text-align:center;'>🚀 E-Sales AI Intelligence System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>AI-powered delivery prediction & analytics</h4>", unsafe_allow_html=True)

    render_orb()

    st.markdown("## 🌟 Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""<div class="feature-card">
            <div class="feature-title">🔮 AI Prediction</div>
            <div class="feature-text">Predict delivery delay risk using ML models</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="feature-card">
            <div class="feature-title">📡 Real-Time Logging</div>
            <div class="feature-text">Track predictions instantly</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div class="feature-card">
            <div class="feature-title">📊 Smart Insights</div>
            <div class="feature-text">Visual analytics for decision making</div>
        </div>""", unsafe_allow_html=True)

    if st.button("👉 Enter Dashboard", key="go_dashboard"):
        st.session_state.page = "dashboard"

# -----------------------------
# DASHBOARD
# -----------------------------
if st.session_state.page == "dashboard":

    st.title("📦 E-Sales Delivery Intelligence System")

    tab1, tab2 = st.tabs(["🔮 Prediction", "📊 Insights"])

    # -------------------------
    # PREDICTION TAB
    # -------------------------
    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            price = st.number_input("Price", 10.0, 10000.0, 150.0, key="price")
            freight_value = st.number_input("Freight Value", 0.0, 500.0, 20.0, key="freight")
            product_weight = st.number_input("Weight", 100.0, 5000.0, 500.0, key="weight")
            product_length = st.number_input("Length", 5.0, 100.0, 30.0, key="length")
            product_width = st.number_input("Width", 5.0, 100.0, 20.0, key="width")
            purchase_hour = st.slider("Purchase Hour", 0, 23, 14, key="hour")

        with col2:
            purchase_day = st.slider("Day of Week", 0, 6, 2, key="day")
            est_days = st.number_input("Estimated Days", 1, 30, 7, key="est")
            installments = st.number_input("Installments", 1, 12, 1, key="inst")
            approval_delay = st.number_input("Approval Delay", 0.0, 100.0, 3.0, key="delay")
            order_total = st.number_input("Order Total", 10.0, 10000.0, 170.0, key="total")
            items_per_order = st.number_input("Items per Order", 1, 10, 1, key="items")

        if st.button("🚀 Predict", key="predict"):

            freight_price_ratio = freight_value / (price + 1)
            slow_approval = 1 if approval_delay > 24 else 0

            input_data = pd.DataFrame([[ 
                price, freight_value, product_weight,
                product_length, product_width,
                purchase_hour, purchase_day,
                est_days, installments,
                approval_delay, order_total,
                items_per_order,
                freight_price_ratio, slow_approval
            ]], columns=[
                "price","freight_value","product_weight_g",
                "product_length_cm","product_width_cm",
                "purchase_hour","purchase_dayofweek",
                "estimated_delivery_days","payment_installments",
                "approval_delay_hours","order_total",
                "items_per_order",
                "freight_price_ratio","slow_approval"
            ])

            prob = model.predict_proba(input_data)[0][1]
            risk = "High Risk" if prob >= 0.3 else "Low Risk"

            if prob >= 0.3:
                st.error(f"⚠️ High Delay Risk ({prob:.2f})")
            else:
                st.success(f"✅ Likely On-Time ({prob:.2f})")

            st.progress(float(prob))

            st.session_state["logs"] = pd.concat([
                st.session_state["logs"],
                pd.DataFrame([{
                    "timestamp": pd.Timestamp.now(),
                    "price": price,
                    "freight_value": freight_value,
                    "weight": product_weight,
                    "hour": purchase_hour,
                    "probability": prob,
                    "risk_level": risk
                }])
            ], ignore_index=True)

    # -------------------------
    # INSIGHTS TAB
    # -------------------------
    with tab2:

        st.subheader("📊 Smart Insights")

        hour_filter = st.selectbox("Filter Hour", sorted(df["purchase_hour"].unique()), key="hf")

        price_range = st.slider(
            "Price Range",
            float(df["price"].min()),
            float(df["price"].max()),
            (float(df["price"].quantile(0.25)), float(df["price"].quantile(0.75))),
            key="pr"
        )

        filtered_df = df[
            (df["purchase_hour"] == hour_filter) &
            (df["price"].between(price_range[0], price_range[1]))
        ]

        if filtered_df.empty:
            filtered_df = df.copy()

        st.metric("Overall Delay", round(df["delivery_delay"].mean(), 2))
        st.metric("Filtered Delay", round(filtered_df["delivery_delay"].mean(), 2))

        fig1 = px.histogram(df, x="price", nbins=30, template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True, key="hist")

        fig2 = px.scatter(filtered_df, x="freight_value", y="delivery_delay", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True, key="scatter")

        full_trend = df.groupby("purchase_hour", as_index=False)["delivery_delay"].mean()
        filt_trend = filtered_df.groupby("purchase_hour", as_index=False)["delivery_delay"].mean()

        fig3 = px.line(full_trend, x="purchase_hour", y="delivery_delay", template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True, key="trend_full")

        fig4 = px.line(filt_trend, x="purchase_hour", y="delivery_delay", template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True, key="trend_filt")

        st.subheader("📡 Logs")

        logs = st.session_state["logs"]

        if logs.empty:
            st.info("No predictions yet 🚀")
        else:
            st.dataframe(logs)

            st.metric("Avg Risk Score", round(logs["probability"].mean(), 3))

            if st.button("🧹 Clear Logs", key="clear"):
                st.session_state["logs"] = pd.DataFrame(columns=logs.columns)
                st.rerun()

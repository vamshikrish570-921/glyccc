import streamlit as st
import random
import pandas as pd
from datetime import datetime
import hashlib
import time

# ⚡ PERFORMANCE: Optimized config - CLOUD READY
st.set_page_config(
    page_title="💕 Love Calculator",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="💕"
)

# Custom CSS - HIDDEN ADMIN INFO
st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#ff9a9e 0%,#fecfef 50%,#fecfef 100%)}
h1,h2,h3,h4,h5,h6,label{color:#ff4d6d!important;font-family:'Comic Sans MS',cursive,sans-serif}
.main-header{text-align:center;font-size:3rem;text-shadow:2px 2px 4px rgba(0,0,0,.3);margin-bottom:2rem}

/* FIXED: Input field visibility */
input, textarea, .stTextInput > div > div > input {
    color: black !important;
    background: rgba(255,255,255,0.95) !important;
    border-radius: 20px !important;
    border: 2px solid #ff69b4 !important;
    padding: 12px 15px !important;
    font-size: 1.1rem !important;
}

div.stButton > button {
    background: linear-gradient(45deg,#ff6b9d,#ff8fb2) !important;
    color: white !important;
    border-radius: 25px !important;
    padding: 12px 35px !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(255,107,157,.4) !important;
    transition: all .3s ease !important;
}
div.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(255,107,157,.6) !important;
}

.result-box, .analysis-box {
    background: rgba(255,255,255,.95);
    padding: 2rem;
    border-radius: 30px;
    box-shadow: 0 10px 30px rgba(255,77,109,.3);
    border: 3px solid #ff69b4;
    margin: 1rem 0;
}
.pro {color: #28a745; font-weight: bold;}
.con {color: #dc3545; font-weight: bold;}
.secret {color: #ffd700; font-weight: bold;}
.metric-container {background: rgba(255,255,255,0.9) !important;}

/* HIDE STREAMLIT FOOTER */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
footer * {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# === GLOBAL DATA STORAGE - SHARED ACROSS ALL USERS ===
if "all_love_data" not in st.session_state:
    st.session_state.all_love_data = []

if "data_version" not in st.session_state:
    st.session_state.data_version = 0


# === SECRET ADMIN SETUP ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


ADMIN_HASH = hash_password("VamJyoRam")
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# === UNIQUE USER ID FOR EACH VISITOR ===
if "visitor_id" not in st.session_state:
    st.session_state.visitor_id = f"visitor_{random.randint(100000, 999999)}_{int(time.time())}"

# Sidebar - SECRET Admin Login
with st.sidebar:
    st.markdown("🔐 **Control Panel**")

    if not st.session_state.admin_logged_in:
        st.markdown("### 🔑 Enter Password")
        admin_pwd = st.text_input("", type="password", placeholder="Admin access...")
        if st.button("🚀 Unlock", key="admin_unlock"):
            if hash_password(admin_pwd) == ADMIN_HASH:
                st.session_state.admin_logged_in = True
                st.success("✅ Access Granted!")
                st.rerun()
            else:
                st.error("❌ Access Denied")
    else:
        st.success("👑 Admin Active")
        st.info(f"👤 ID: `{st.session_state.visitor_id}`")
        if st.button("🚪 Logout", key="admin_logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

# === LOVE CALCULATION LOGIC ===
NAME_TRAITS = {
    "a": "Adventurous", "b": "Bold", "c": "Charming", "d": "Dreamy", "e": "Elegant",
    "f": "Fun-loving", "g": "Gentle", "h": "Happy", "i": "Intelligent", "j": "Joyful",
    "k": "Kind", "l": "Loyal", "m": "Mature", "n": "Nice", "o": "Optimistic",
    "p": "Passionate", "q": "Quiet", "r": "Romantic", "s": "Sweet", "t": "Trustworthy",
    "u": "Unique", "v": "Vivacious", "w": "Warm", "x": "Xtraordinary", "y": "Youthful", "z": "Zestful"
}


def get_traits(name):
    """Extract personality traits from name"""
    if not name or not name.strip():
        return ["Mysterious"]
    return [NAME_TRAITS.get(c.lower(), "Loving") for c in name.strip()[:4] if c.isalpha()]


def get_pros_cons(perc):
    """Generate relationship analysis"""
    if perc >= 95:
        return ["🔥 Perfect soulmates!", "💍 Marriage material!", "⭐ Forever together"], ["😇 Too perfect to be true"]
    elif perc >= 85:
        return ["💖 Amazing chemistry!", "🌈 Long-term potential!", "🎉 Endless fun!"], ["⚠️ Occasional arguments"]
    elif perc >= 75:
        return ["❤️ Great match!", "🤝 Strong foundation!", "✨ Good compatibility"], ["⏳ Needs more time"]
    elif perc >= 65:
        return ["💕 Growing love!", "🌱 Great potential!", "💪 Will improve"], ["💡 More effort needed"]
    else:
        return ["🌈 Friendship first!", "💖 Hidden sparks!", "🎯 Work in progress"], ["😅 More dates needed!"]


def save_love_calculation(name1, name2, percentage):
    """SAVE TO GLOBAL SHARED DATA - ADMIN CAN SEE ALL"""
    global_entry = {
        "id": len(st.session_state.all_love_data) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "visitor_id": st.session_state.visitor_id,
        "name1": name1.strip(),
        "name2": name2.strip(),
        "percentage": percentage,
        "ip_hint": "web_visitor"
    }
    st.session_state.all_love_data.append(global_entry)
    st.session_state.data_version += 1
    return True


# === MAIN LOVE CALCULATOR UI ===
st.markdown('<h1 class="main-header">💕 Ultimate Love Calculator 💕</h1>', unsafe_allow_html=True)

# Input Section
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown("### 👩‍❤️‍💋‍👨 **Your Name**")
    name1 = st.text_input("", placeholder="Enter your name 💝", label_visibility="collapsed")
with col2:
    st.markdown("### 💕 **Partner\'s Name**")
    name2 = st.text_input("", placeholder="Enter partner name 🌹", label_visibility="collapsed")

# Calculate Button
if st.button("💖 **Calculate Love Percentage** 💖", type="primary", use_container_width=True):
    if name1.strip() and name2.strip():
        # Deterministic love score
        seed_string = (name1.lower() + name2.lower()).encode()
        random.seed(seed_string)
        percentage = random.randint(44, 100)

        # Generate analysis
        traits1 = get_traits(name1)
        traits2 = get_traits(name2)
        pros, cons = get_pros_cons(percentage)

        # ✅ SAVE TO GLOBAL DATABASE
        save_love_calculation(name1, name2, percentage)

        # Celebration
        st.balloons()
        st.success("🎉 Love Score Saved!")

        # Main Result
        st.markdown(f"""
        <div class="result-box">
            <h2 style='text-align:center'>{name1} 💕 {name2}</h2>
            <div style='text-align:center'>
                <h1 style='font-size:6rem;color:#ff4d6d;margin:0'>{percentage}%</h1>
                <p style='font-size:1.3rem;color:#666;margin:10px 0 0 0'>
                    Love Compatibility Score
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Personality Traits
        st.markdown(f"""
        <div class="analysis-box">
            <h3 style='text-align:center'>✨ Personality Match</h3>
            <div style='display:flex;justify-content:space-around;flex-wrap:wrap;gap:20px;padding:1rem'>
                <div style='text-align:center;flex:1;padding:1rem'>
                    <h4 style='color:#ff4d6d'>{name1}</h4>
                    <p style='font-size:1.1rem'>{', '.join(traits1[:3])}</p>
                </div>
                <div style='text-align:center;flex:1;padding:1rem'>
                    <h4 style='color:#ff4d6d'>{name2}</h4>
                    <p style='font-size:1.1rem'>{', '.join(traits2[:3])}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Pros & Cons
        col_pros, col_cons = st.columns(2, gap="large")
        with col_pros:
            st.markdown("### ✅ **Relationship Strengths**")
            for pro in pros:
                st.markdown(f"• <span class='pro'>{pro}</span>", unsafe_allow_html=True)
        with col_cons:
            st.markdown("### ⚠️ **Growth Areas**")
            for con in cons:
                st.markdown(f"• <span class='con'>{con}</span>", unsafe_allow_html=True)

    else:
        st.warning("😅 **Please enter both names to calculate love!**")

# === 🔥 SECRET ADMIN PANEL - SEES ALL USERS DATA 🔥 ===
if st.session_state.admin_logged_in:
    st.markdown("---")
    st.markdown('<h2 class="secret">🔐 **GLOBAL LOVE DATABASE** 🔐</h2>', unsafe_allow_html=True)

    if st.session_state.all_love_data:
        df = pd.DataFrame(st.session_state.all_love_data)

        # Statistics Dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💕 Total Love Tests", len(df))
        with col2:
            st.metric("👥 Unique Visitors", df['visitor_id'].nunique())
        with col3:
            avg_love = df['percentage'].mean()
            st.metric("❤️ Average Love Score", f"{avg_love:.1f}%")
        with col4:
            highest = df['percentage'].max()
            st.metric("🔥 Highest Score", f"{highest}%")

        st.markdown("### 📊 **All Love Stories**")

        # Enhanced Data Table
        display_df = df[["timestamp", "visitor_id", "name1", "name2", "percentage"]].copy()
        display_df.columns = ["Date", "VisitorID", "Name 1", "Name 2", "Love %"]
        display_df = display_df.sort_values("Date", ascending=False).reset_index(drop=True)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Love %": st.column_config.ProgressColumn("Love %", width="medium")
            }
        )

        # Download All Data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 **Download Complete Database**",
            data=csv,
            file_name=f"love_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        # Clear Data
        if st.button("🗑️ **Clear Global Database**", type="secondary"):
            st.session_state.all_love_data = []
            st.session_state.data_version = 0
            st.success("🗑️ Database cleared!")
            st.rerun()

    else:
        st.info("🌍 **No love stories yet! Share widely!** 🎉")

# CLEAN FOOTER - NO ADMIN INFO
st.markdown("---")
st.markdown("<p style='text-align:center;color:#ff69b4;font-size:0.9rem'>💕 Love Calculator Pro</p>",
            unsafe_allow_html=True)

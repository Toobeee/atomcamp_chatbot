# app.py
import streamlit as st
from atomcamp_bot import qa, casual_responses, fallback_responses
import random
from datetime import datetime

st.set_page_config(page_title="Atom AI Chatbot", page_icon="🤖", layout="wide")

# -------------------------------
# Session state
# -------------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Floating toggle button
# -------------------------------
toggle_clicked = st.button("💬", key="chat_toggle")
if toggle_clicked:
    st.session_state.chat_open = not st.session_state.chat_open

# -------------------------------
# CSS Styling (modern UI)
# -------------------------------
st.markdown(
    """
<style>
/* Floating toggle bubble */
.stButton > button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  font-size: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg,#34d399,#059669);
  color: white;
  border: none;
  box-shadow: 0 6px 18px rgba(0,0,0,0.18);
  z-index: 99999;
}

/* Popup container */
#chat-popup {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 360px;
  max-height: 75vh;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.18);
  font-family: "Segoe UI", sans-serif;
  z-index: 99998;
  overflow: hidden;
}

/* Header */
#chat-popup .header {
  background: linear-gradient(135deg,#34d399,#059669);
  color: white;
  padding: 12px;
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Messages */
#chat-popup .messages {
  padding: 12px;
  flex: 1;
  overflow-y: auto;
  background: linear-gradient(180deg,#fbfefc,#f7f9f8);
}

/* Bubbles */
.user-msg, .bot-msg {
  padding: 10px 14px;
  margin: 8px 0;
  border-radius: 18px;
  max-width: 78%;
  font-size: 14px;
  line-height: 1.45;
  word-wrap: break-word;
  display: inline-block;
}
.user-msg {
  background: linear-gradient(135deg,#34d399,#059669);
  color: white;
  float: right;
  clear: both;
}
.bot-msg {
  background: linear-gradient(135deg,#f3f4f6,#e6e9ee);
  color: #111;
  float: left;
  clear: both;
  display: flex;
  align-items: center;
  gap: 8px;
}
.bot-msg img.avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
}

/* Input area */
#chat-popup .input-area {
  padding: 10px;
  border-top: 1px solid #eee;
  background: white;
}

/* Responsive */
@media (max-width: 640px) {
  #chat-popup {
    right: 10px;
    left: 10px;
    width: auto;
    bottom: 80px;
    max-height: 82vh;
  }
  .stButton > button {
    right: 12px;
    bottom: 12px;
  }
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------
# Chat Popup
# -------------------------------
if st.session_state.chat_open:
    st.markdown('<div id="chat-popup">', unsafe_allow_html=True)

    # Header
    st.markdown(
        '<div class="header">🤖 Atom AI <span style="cursor:pointer;" onclick="document.getElementById(\'chat-popup\').style.display=\'none\'">✕</span></div>',
        unsafe_allow_html=True,
    )

    # Input comes FIRST (so no lag in responses)
    user_input = st.chat_input("Type your message...")
    if user_input:
        ts = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": user_input, "time": ts})

        try:
            if user_input.lower() in casual_responses:
                response = casual_responses[user_input.lower()]
            else:
                result = qa.invoke({"question": user_input})
                if isinstance(result, dict):
                    response = result.get("answer", "") or result.get("output_text", "") or str(result)
                else:
                    response = str(result)
                response = response.strip()
                if not response:
                    response = random.choice(fallback_responses)
        except Exception:
            response = "⚠️ Sorry, I'm having trouble right now."

        st.session_state.messages.append(
            {"role": "bot", "content": response, "time": datetime.now().strftime("%H:%M")}
        )

    # Messages area
    st.markdown('<div class="messages" id="chat-box">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="user-msg">
                  {msg['content']}
                  <div style="font-size:10px;color:#999;margin-top:6px;text-align:right;">{msg.get("time","")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="bot-msg">
                  <img class="avatar" src="https://img.icons8.com/fluency/48/robot-2.png"/>
                  <div>{msg['content']}
                    <div style="font-size:10px;color:#666;margin-top:6px;">{msg.get("time","")}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # Close main div
    st.markdown("</div>", unsafe_allow_html=True)

    # Auto scroll
    st.markdown(
        """
        <script>
        const el = document.getElementById('chat-box');
        if (el) { el.scrollTop = el.scrollHeight; }
        </script>
        """,
        unsafe_allow_html=True,
    )

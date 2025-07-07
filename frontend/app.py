
import streamlit as st
import requests

st.title("📅 Calendar Booking Assistant")


if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_123"
if "event_created" not in st.session_state:
    st.session_state.event_created = False
if "calendar_link" not in st.session_state:
    st.session_state.calendar_link = ""


if len(st.session_state.conversation) == 0 and not st.session_state.event_created:
    res = requests.post("http://127.0.0.1:8000/chat", json={
        "user_id": st.session_state.user_id,
        "message": ""  
    })
    bot_reply = res.json()["response"]
    st.session_state.conversation.append({"role": "Bot", "text": bot_reply})


if st.session_state.event_created:
    st.success(" Your event has been scheduled!")
    st.markdown(f"**[ View your event in Google Calendar]({st.session_state.calendar_link})**", unsafe_allow_html=True)
else:

    for chat in st.session_state.conversation:
        st.markdown(f"**{chat['role']}**: {chat['text']}")

    with st.form(key=f"form_{len(st.session_state.conversation)}"):
        user_input = st.text_input("Your reply:", key=f"input_{len(st.session_state.conversation)}")
        submit = st.form_submit_button("Send")

    if submit and user_input.strip():
        
        st.session_state.conversation.append({"role": "You", "text": user_input})

        
        res = requests.post("http://127.0.0.1:8000/chat", json={
            "user_id": st.session_state.user_id,
            "message": user_input
        })
        bot_reply = res.json()["response"]

        
        if "calendar.google.com" in bot_reply:
            st.session_state.event_created = True
            st.session_state.calendar_link = bot_reply
            st.experimental_rerun()
        else:
            # Append bot reply
            st.session_state.conversation.append({"role": "Bot", "text": bot_reply})
            st.rerun()

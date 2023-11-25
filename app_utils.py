import streamlit as st
def reset_start_stop():
 	st.session_state.start = 0
 	st.session_state.stop = st.session_state.start


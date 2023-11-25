import streamlit as st

def reset_start_stop():
 	st.session_state.start = 0
 	st.session_state.stop = st.session_state.start

# Function to generate HTML with JavaScript to open URLs
def generate_open_urls_script(url):
    script = """
    <script>
        function openURL(url) {
            window.open(url, '_blank');
        }
    </script>
    """

    script += f'<script>openURL("{url}");</script>'

    return script

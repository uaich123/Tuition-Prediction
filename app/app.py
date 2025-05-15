import streamlit as st

home_page = st.Page("home.py", title="Home", icon=":material/home:")
tuition_page = st.Page("tuition.py", title="Tuition Predictor", icon=":material/attach_money:")
about_page = st.Page("about.py", title="About", icon=":material/help:")
pg = st.navigation([home_page, tuition_page, about_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()



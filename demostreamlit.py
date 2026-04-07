import streamlit as ag

ag.title("Welcome to Akshaya patra ~ Sharma's kitchen art")

name = ag.text_input("Enter your name")

if ag.button("Warm welcome to our kitchen"):
    # Everything below this is indented by 4 spaces
    if name:
        ag.success(f"Hello {name}, Welcome to our kitchen")
    else: 
        ag.warning("Please enter your name")
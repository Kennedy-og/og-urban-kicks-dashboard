import os
import streamlit as st

print("Current folder:")
print(os.getcwd())

print("\nMySQL host Python is reading:")
print(st.secrets["mysql"]["host"])

print("\nMySQL port Python is reading:")
print(st.secrets["mysql"]["port"])

print("\nCA file exists?")
print(os.path.exists(st.secrets["mysql"]["ssl_ca"]))
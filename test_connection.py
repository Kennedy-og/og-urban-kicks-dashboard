import streamlit as st
import mysql.connector

config = st.secrets["mysql"]

conn = mysql.connector.connect(
    host=config["host"],
    port=config["port"],
    user=config["user"],
    password=config["password"],
    database=config["database"],
    ssl_ca=config["ssl_ca"]
)

cursor = conn.cursor()
cursor.execute("SELECT VERSION();")
version = cursor.fetchone()

print("Connected successfully!")
print("MySQL version:", version[0])

cursor.close()
conn.close()
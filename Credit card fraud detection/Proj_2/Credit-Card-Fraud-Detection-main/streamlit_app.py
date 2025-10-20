import streamlit as st
import json
import requests as re

def check_api_status():
    try:
        response = re.get("http://localhost:8000")
        if response.status_code == 200:
            return True
    except re.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    return False

st.title("Credit Card Fraud Detection Web App")
st.image("image.png")
st.write("Created By Mrunal")

if check_api_status():
    st.success("API is running. You can access the API documentation at [Swagger UI Docs](http://localhost:8000/docs) or [ReDoc](http://localhost:8000/redoc).")
else:
    st.error("API is not running. Please start the API and try again.")
    st.stop()

st.sidebar.header('Input Features of The Transaction')
sender_name = st.sidebar.text_input("Input Sender ID")
receiver_name = st.sidebar.text_input("Input Receiver ID")
step = st.sidebar.slider("Number of Hours it took the Transaction to complete: ", min_value=0, max_value=24)
types = st.sidebar.selectbox("Enter Type of Transfer Made:", (0, 1, 2, 3, 4), format_func=lambda x: ["Cash In", "Cash Out", "Debit", "Payment", "Transfer"][x])
amount = st.sidebar.number_input("Amount in $", min_value=0, max_value=110000)
oldbalanceorg = st.sidebar.number_input("Sender Balance Before Transaction was made", min_value=0, max_value=110000)
newbalanceorg = st.sidebar.number_input("Sender Balance After Transaction was made", min_value=0, max_value=110000)
oldbalancedest = st.sidebar.number_input("Recipient Balance Before Transaction was made", min_value=0, max_value=110000)
newbalancedest = st.sidebar.number_input("Recipient Balance After Transaction was made", min_value=0, max_value=110000)
isflaggedfraud = 1 if amount >= 200000 else 0

if st.button("Detection Result"):
    values = {
        "step": step,
        "types": types,
        "amount": amount,
        "oldbalanceorig": oldbalanceorg,
        "newbalanceorig": newbalanceorg,
        "oldbalancedest": oldbalancedest,
        "newbalancedest": newbalancedest,
        "isflaggedfraud": isflaggedfraud
    }

    st.write(f"""### These are the transaction details:
    Sender ID: {sender_name}
    Receiver ID: {receiver_name}
    1. Number of Hours it took to complete: {step}
    2. Type of Transaction: {types}
    3. Amount Sent: {amount}$
    4. Sender Balance Before Transaction: {oldbalanceorg}$
    5. Sender Balance After Transaction: {newbalanceorg}$
    6. Recipient Balance Before Transaction: {oldbalancedest}$
    7. Recipient Balance After Transaction: {newbalancedest}$
    8. System Flag Fraud Status (Transaction amount greater than $200000): {isflaggedfraud}
    """)

    res = re.post("http://localhost:8000/predict", json=values)
    try:
        resp = res.json()
        if sender_name == '' or receiver_name == '':
            st.write("Error! Please input Transaction ID or Names of Sender and Receiver!")
        else:
            st.write(f"""### The '{types}' transaction that took place between {sender_name} and {receiver_name} is {resp[0]}.""")
    except json.JSONDecodeError as e:
        st.error(f"Failed to decode JSON: {e}")
        st.error(f"Response text: {res.text}")

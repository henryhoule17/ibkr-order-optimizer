from ib_interface import create_orders
import streamlit as st

# Streamlit UI for Contract and Order details

st.title("Contract and Order Form")

# Form for Contract details
st.header("Contract Details")
contract_symbol = st.text_input("Symbol", "TSM")
contract_secType = st.selectbox("Security Type", ["STK", "OPT", "FUT", "CASH", "IND", "CFD", "BOND", "FOP", "WAR", "IOPT", "FUND", "CMDTY", "NEWS", "SPR", "BAG", "KNOWS", "TBOND", "TBILL"])
contract_exchange = st.text_input("Exchange", "SMART")
contract_currency = st.text_input("Currency", "USD")

# Form for Order details
st.header("Order Details")
order_action = st.selectbox("Action", ["BUY", "SELL"])
order_totalQuantity = st.number_input("Total Quantity", value=10, step=1)
order_orderType = st.selectbox("Order Type", ["LMT", "MKT", "STP", "STP LMT", "TRAIL", "TRAIL LMT"])
order_highestPrice = st.number_input("Highest Price", value=160.90, step=0.01)
order_lowestPrice = st.number_input("Lowest Price", value=160.90, step=0.01)

# Submit button
if st.button("Submit"):
    create_orders(
        symbol=contract_symbol, 
        secType=contract_secType, 
        exchange=contract_exchange, 
        currency=contract_currency, 
        action=order_action, 
        totalQuantity=order_totalQuantity, 
        orderType=order_orderType, 
        highestPrice=order_highestPrice,
        lowestPrice = order_lowestPrice
    )


from concurrent.futures import ThreadPoolExecutor
import math
import streamlit as st
import random
import time
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
from ib_async import Contract, Order, IB, Stock

ORDER_SEGMENTS = 10
CLIENT_ID = 4

if 'validated' not in st.session_state:
    st.session_state.validated = False

def create_orders(
    symbol: str, 
    secType: str, 
    exchange: str, 
    currency: str, 
    action: str, 
    totalQuantity: int, 
    orderType: str, 
    highestPrice: float,
    lowestPrice: float
):
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=CLIENT_ID)

    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency

    orders = []

    for _ in range(ORDER_SEGMENTS):
        diff = highestPrice - lowestPrice
        multiple = random.random()
        lmtPrice = lowestPrice + diff * multiple

        order = Order()
        order.action = action
        order.totalQuantity = round(totalQuantity / ORDER_SEGMENTS)
        order.orderType = orderType
        order.lmtPrice = round(lmtPrice, 2)
        orders.append(order)

    time.sleep(1)
    for o in orders:
        ib.placeOrder(contract, o)
    time.sleep(5)
    ib.disconnect()

def run_async_task(coroutine):
    loop = asyncio.get_event_loop()
    future = asyncio.run_coroutine_threadsafe(coroutine, loop)
    return future.result()

def main():
    # Streamlit UI for Contract and Order details
    st.title("Contract and Order Form")

    # Form for Contract details
    st.header("Contract Details")
    contract_symbol = st.text_input("Symbol", "AAPL")
    contract_secType = st.selectbox("Security Type", ["STK", "OPT", "FUT", "CASH", "IND", "CFD", "BOND", "FOP", "WAR", "IOPT", "FUND", "CMDTY", "NEWS", "SPR", "BAG", "KNOWS", "TBOND", "TBILL"])
    contract_exchange = st.text_input("Exchange", "SMART")
    contract_currency = st.text_input("Currency", "USD")

    if st.button("Validate"):
        ib = IB()
        try:
            ib.connect('127.0.0.1', 7497, clientId=CLIENT_ID, timeout=10)
        except RuntimeError as re:
            st.error("Connection to TWS failed, try restarting both this app and TWS.")
            return
        st.session_state.validated = True
        print("Connected to TWS")
        stock = Stock(contract_symbol, contract_exchange, contract_currency)
        ib.qualifyContracts(stock)
        print("Contract Qualified")
        ticker = ib.reqMktData(stock, "", False, False)
        print("Ticker Requested")
        time.sleep(2)
        print("Ticker Type: ", type(ticker))
        print("Bid: ", ticker.bid)
        print("Bid Type: ", type(ticker.bid))  
        print("Ask: ", ticker.ask)
        print("Next: ", ticker.close)
        st.session_state.ticker = ticker
        ib.disconnect()

    if st.session_state.validated:
        st.header("Order Details")
        ticker = st.session_state.ticker
        order_action = st.selectbox("Action", ["BUY", "SELL"])
        if ticker and ticker.bid and ticker.ask and not math.isnan(ticker.bid) and not math.isnan(ticker.ask):
            if order_action == "BUY":
                orders_range = st.slider("Range", value=[ticker.bid*0.95, ticker.bid], step=0.01)
            elif order_action == "SELL":
                orders_range = st.slider("Range", value=[ticker.ask, ticker.ask*1.05], step=0.01)
        else:
            order_highestPrice = st.number_input("Highest Price", step=0.01, value=None)
            order_lowestPrice = st.number_input("Lowest Price", step=0.01, value=None)
            orders_range = (order_lowestPrice, order_highestPrice)

        order_totalQuantity = st.number_input("Total Quantity", value=100, step=1)
        order_type = "LMT"

        # Submit button
        if st.button("Submit"):
            print("Contract Details:")
            create_orders(
                symbol=contract_symbol, 
                secType=contract_secType, 
                exchange=contract_exchange, 
                currency=contract_currency, 
                action=order_action, 
                totalQuantity=order_totalQuantity, 
                orderType=order_type, 
                highestPrice=orders_range[1],
                lowestPrice = orders_range[0]
            )
        if st.button("Reset"):
            st.session_state.validated = False
            st.session_state.ticker = None
            st.rerun()


main()


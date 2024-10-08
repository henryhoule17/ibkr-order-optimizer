import logging
import random
import time
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
from ib_async import Contract, Order, IB

ORDER_SEGMENTS = 10

async def create_orders(
    ib: IB, 
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
    

    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency

    orders = []

    for i in range(ORDER_SEGMENTS):
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
    for i, o in enumerate(orders):
        # print("Next ID: ", client.nextOrderId())
        ib.placeOrder(contract, o)
        # client.openOrder(i+140, contract, o, orderState=None)
    time.sleep(5)
    ib.disconnect()


# class IBClient(EWrapper, EClient):
    
#     nextValidOrderId = None

#     def __init__(self, host, port, client_id):
#         EClient.__init__(self, self) 
        
#         self.connect(host, port, client_id)

#         thread = Thread(target=self.run)
#         thread.start()


#     def error(self, req_id, code, msg, misc=None):
#         if code in [2104, 2106, 2158]:
#             print(msg)
#         else:
#             print('Error {}: {}'.format(code, msg))


#     def historicalData(self, req_id, bar):
#         print(bar)


#     # callback when all historical data has been received
#     def historicalDataEnd(self, reqId, start, end):
#         print(f"end of data {start} {end}")

#     def nextOrderId(self):
#         oid = self.nextValidOrderId
#         self.nextValidOrderId += 1
#         return oid
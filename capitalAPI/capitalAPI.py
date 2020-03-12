import os
import comtypes.client
from SKReplyLibEvent import SKReplyLibEvent
from SKOrderLibEvent import SKOrderLibEvent
from SKCenterLibEvent import SKCenterLibEvent
from SKQuoteLibEvents import SKQuoteLibEvents
from datetime import datetime

comtypes.client.GetModule(os.path.split(os.path.realpath(__file__))[0] + r"/x64/SKCOM.dll")
import comtypes.gen.SKCOMLib as sk

skC = comtypes.client.CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
skOOQ = comtypes.client.CreateObject(sk.SKOOQuoteLib, interface=sk.ISKOOQuoteLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib, interface=sk.ISKOrderLib)
skOSQ = comtypes.client.CreateObject(sk.SKOSQuoteLib, interface=sk.ISKOSQuoteLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)

# comtypes使用此方式註冊callback
SKReplyEvent = SKReplyLibEvent()
SKReplyLibEventHandler = comtypes.client.GetEvents(skR, SKReplyEvent)

# comtypes使用此方式註冊callback
SKOrderEvent = SKOrderLibEvent()
SKOrderLibEventHandler = comtypes.client.GetEvents(skO, SKOrderEvent)

# comtypes使用此方式註冊callback
SKCenterEvent = SKCenterLibEvent()
SKCenterLibEventHandler = comtypes.client.GetEvents(skC, SKCenterEvent)

SKQuoteEvent=SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)

class CapitalAPI:
  def __init__(self):
    self.config = {
      "id": "",
      "account": "",
      "symbol": "MTX00",
      "quantity_limit": "10", # quantity and order num / sec
    }

  def set_account(self, account):
    self.config['account'] = account

  def login(self, id, password):
    skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Reply")
    m_nCode = skC.SKCenterLib_Login(id, password)
    skC.SKCenterLib_Debug(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Reply")
    if (m_nCode == 0):
      print("Login success: " + id)
      self.config['id'] = id
    elif m_nCode == 151:
      print("Wrong password")
    else:
      print("Login fail: " + str(m_nCode))

  def init_order(self):
    self.initialize_SKOrderLib()
    self.read_cert()
    self.get_user_account()
    self.set_order_limit()

  def init_reply_server(self):
    nErrorCode = skR.SKReplyLib_ConnectByID(self.config['id'])
    self.write_message("Reply", nErrorCode, "SKReplyLib_Connect")

  def init_quote_server(self):
    m_nCode = skQ.SKQuoteLib_EnterMonitor()
    self.write_message("Quote", m_nCode, "SKQuoteLib_EnterMonitor")

  def initialize_SKOrderLib(self):
    print("Initializing SKOrderLib")
    m_nCode = skO.SKOrderLib_Initialize()
    self.write_message("Order", m_nCode, "SKOrderLib_Initialize")

  def read_cert(self):
    print("Read cert...")
    m_nCode = skO.ReadCertByID(self.config['id'])
    self.write_message("Order", m_nCode, "ReadCertByID")

  def get_user_account(self):
    try:
      m_nCode = skO.GetUserAccount()
      self.write_message("Order", m_nCode, "GetUserAccount")
    except Exception as e:
      print("error！" + str(e))

  def set_order_limit(self, limit=10):
    try:
      print("Set order limit to " + str(limit))
      # 1 == Future
      self.config['quantity_limit'] = limit
      nMarketType = 1
      m_nCode = skO.SetMaxQty(nMarketType, self.config['quantity_limit'])
      self.write_message("Order", m_nCode, "SetMaxQty")
      m_nCode = skO.SetMaxCount(nMarketType, self.config['quantity_limit'])
      self.write_message("Order", m_nCode, "SetMaxCount")
    except Exception as e:
      print("error！" + str(e))

  def unlock_order_limit(self):
    try:
      # 1 == Future
      nMarketType = 1
      m_nCode = skO.UnlockOrder(nMarketType)
      self.write_message("Order", m_nCode, "UnlockOrder")
    except Exception as e:
      print ("error！" + str(e))

  '''
    sBuySell: sell(1), buy(0)
    sTradeType: ROD(0), IOC(1), FOK(2)
    sDayTrade: true(1), false(0)
  '''
  def send_future_order(self, sBuySell, sTradeType, sDayTrade, quantity, bstrPrice="M", bAsyncOrder=False):
    try:
      oOrder = sk.FUTUREORDER()
      oOrder.bstrFullAccount = self.config['account']
      oOrder.bstrStockNo = self.config['symbol']
      oOrder.sBuySell = sBuySell
      oOrder.sTradeType = sTradeType
      oOrder.sDayTrade = sDayTrade
      oOrder.bstrPrice = bstrPrice
      oOrder.nQty = quantity
      oOrder.sNewClose = 2  # AUTO
      oOrder.sReserved = 0  # T&&T+1

      message, m_nCode = skO.SendFutureOrder(self.config['id'], bAsyncOrder, oOrder)
      self.write_message("Order", m_nCode, "SendFutureOrder")
    except Exception as e:
      print("error！" + str(e))

  def buy_at_market(self, quantity=1):
    print("{}\tBuy {} at market".format(datetime.now(), quantity))
    self.send_future_order(0, 1, 0, quantity)

  def sell_at_market(self, quantity=1):
    print("{}\tSell {} at market".format(datetime.now(), quantity))
    self.send_future_order(1, 1, 0, quantity)

  def get_open_interest(self):
    try:
      m_nCode = skO.GetOpenInterest(self.config['id'], self.config['account'])
      self.write_message("Order", m_nCode, "GetOpenInterest")
    except Exception as e:
      print("error！" + str(e))

  '''
    nCoinType: ALL(0), NTD(1), RMB(2)
  '''
  def get_rights(self):
    try:
      nCoinType = 1
      m_nCode = skO.GetFutureRights(self.config['id'], self.config['account'], nCoinType)
      self.write_message("Order", m_nCode, "GetFutureRights")
    except Exception as e:
      print("Error！" + str(e))

  def write_message(self, str_type, nCode, str_message):
    str_info = ""
    if (nCode != 0):
      str_info = "【" + skC.SKCenterLib_GetLastLogInfo() + "】"
    print("【" + str_type + "】【" + str_message + "】【"
          + skC.SKCenterLib_GetReturnCodeMessage(nCode) + "】" + str_info)

if __name__ == "__main__":
  import pythoncom
  import  time
  from config import config
  id = config['id']
  password = config['password']
  account = config['account']

  api = CapitalAPI()
  api.login(id, password)
  api.set_account(account)
  api.init_reply_server()
  api.init_quote_server()
  api.init_order()
  #api.buy_at_market()
  #api.sell_at_market(2)
  api.get_open_interest()
  api.get_rights()

  for i in range(15):
    time.sleep(1)
    pythoncom.PumpWaitingMessages()


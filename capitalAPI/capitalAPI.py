import os
import comtypes.client
from .events import SKReplyLibEvent
from .events import SKOrderLibEvent
from .events import SKCenterLibEvent
from datetime import datetime

class CapitalAPI:
  def __init__(self):
    comtypes.client.GetModule(os.path.split(os.path.realpath(__file__))[0] + r"/SKCOM.dll")
    import comtypes.gen.SKCOMLib as sk
    self.skC = comtypes.client.CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
    self.skOOQ = comtypes.client.CreateObject(sk.SKOOQuoteLib, interface=sk.ISKOOQuoteLib)
    self.skO = comtypes.client.CreateObject(sk.SKOrderLib, interface=sk.ISKOrderLib)
    self.skOSQ = comtypes.client.CreateObject(sk.SKOSQuoteLib, interface=sk.ISKOSQuoteLib)
    self.skQ = comtypes.client.CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
    self.skR = comtypes.client.CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)

    # comtypes使用此方式註冊callback
    SKReplyEvent = SKReplyLibEvent()
    SKReplyLibEventHandler = comtypes.client.GetEvents(self.skR, SKReplyEvent)

    # comtypes使用此方式註冊callback
    SKOrderEvent = SKOrderLibEvent()
    SKOrderLibEventHandler = comtypes.client.GetEvents(self.skO, SKOrderEvent)

    # comtypes使用此方式註冊callback
    SKCenterEvent = SKCenterLibEvent()
    SKCenterLibEventHandler = comtypes.client.GetEvents(self.skC, SKCenterEvent)

    self.config = {
      "id": "",
      "account": "",
      "symbol": "MXF01",
      "quantity_limit": "10", # quantity and order num / sec
    }

  def set_account(self, account):
    self.config['account'] = account

  def login(self, id, password):
    try:
      self.skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Reply")
      m_nCode = self.skC.SKCenterLib_Login(id, password)
      self.skC.SKCenterLib_Debug(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Reply")
      if (m_nCode == 0):
        print("Login success: " + id)
        self.config['id'] = id
      elif m_nCode == 151:
        print("Wrong password")
      else:
        print("Login fail: " + m_nCode)
    except Exception as e:
      print("Error: " + e)

  def init_order(self):
    self.initialize_SKOrderLib()
    self.read_cert()
    self.set_order_limit()

  def initialize_SKOrderLib(self):
    try:
      print("Initializing SKOrderLib")
      m_nCode = self.skO.SKOrderLib_Initialize()
      self.write_message("Order", m_nCode, "SKOrderLib_Initialize")
    except Exception as e:
      print("error！" + e)

  def read_cert(self):
    try:
      print("Read cert...")
      m_nCode = self.skO.ReadCertByID(self.config['id'])
      self.write_message("Order", m_nCode, "ReadCertByID")
    except Exception as e:
      print("error！" + e)

  def set_order_limit(self, limit=10):
    try:
      print("Set order limit to " + limit)
      # 1 == Future
      self.config['quantity_limit'] = limit
      nMarketType = 1
      m_nCode = self.skO.SetMaxQty(nMarketType, self.config['quantity_limit'])
      self.write_message("Order", m_nCode, "SetMaxQty")
      m_nCode = self.skO.SetMaxCount(nMarketType, self.config['quantity_limit'])
      self.write_message("Order", m_nCode, "SetMaxCount")
    except Exception as e:
      print("error！" + e)

  def unlock_order_limit(self):
    try:
      # 1 == Future
      nMarketType = 1
      m_nCode = self.skO.UnlockOrder(nMarketType)
      self.write_message("Order", m_nCode, "UnlockOrder")
    except Exception as e:
      print ("error！" + e)

  '''
    sBuySell: sell(0), buy(1)
    sTradeType: ROD(0), IOC(1), FOK(2)
    sDayTrade: true(1), false(0)
  '''
  def send_future_order(self, sBuySell, sTradeType, sDayTrade, quantity, bstrPrice="M", bAsyncOrder=False):
    try:
      oOrder = self.sk.FUTUREORDER()
      oOrder.bstrFullAccount = self.config['account']
      oOrder.bstrStockNo = self.config['symbol']
      oOrder.sBuySell = sBuySell
      oOrder.sTradeType = sTradeType
      oOrder.sDayTrade = sDayTrade
      oOrder.bstrPrice = bstrPrice
      oOrder.nQty = quantity
      oOrder.sNewClose = 2  # AUTO
      oOrder.sReserved = 0  # T&&T+1

      message, m_nCode = self.skO.SendFutureOrder(self.config['id'], bAsyncOrder, oOrder)
      self.write_message("Order", m_nCode, "SendFutureOrder", self.__dOrder[''])
    except Exception as e:
      print("error！" + e)

  def buy_at_market(self, quantity=1):
    print("{}\tBuy {} at market".format(datetime.now(), quantity))
    self.send_future_order(1, 1, 0, quantity)

  def sell_at_market(self, quantity=1):
    print("{}\tSell {} at market".format(datetime.now(), quantity))
    self.send_future_order(0, 1, 0, quantity)

  def get_open_interest(self):
    try:
      m_nCode = self.skO.GetOpenInterest(self.config['id'], self.config['account'])
      self.write_message("Order", m_nCode, "GetOpenInterest")
    except Exception as e:
      print("error！" + e)

  def write_message(self, str_type, nCode, str_message):
    str_info = ""
    if (nCode != 0):
      str_info = "【" + self.skC.SKCenterLib_GetLastLogInfo() + "】"
    print("【" + str_type + "】【" + str_message + "】【"
          + self.skC.SKCenterLib_GetReturnCodeMessage(nCode) + "】" + str_info)

if __name__ == "__main__":
  import  time;
  id = ""
  password = ""
  account = ""
  api = CapitalAPI()
  api.login()
  api.set_account(account)
  api.initialize_SKOrderLib()
  api.buy_at_market()
  api.sell_at_market(2)
  for i in range(30):
    api.get_open_interest()
    time.sleep(1)



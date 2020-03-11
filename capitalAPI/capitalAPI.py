import os
import comtypes.client

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

    self.config = {
      "id": "",
      "account": "",
      "quantity_limit": "10", # quantity and order num / sec
    }


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

  def initialize_SKOrderLib(self):
    try:
      m_nCode = self.skO.SKOrderLib_Initialize()
      self.write_message("Order", m_nCode, "SKOrderLib_Initialize")
    except Exception as e:
      print("error！" + e)

  def read_cert(self):
    try:
      m_nCode = self.skO.ReadCertByID(self.config['id'])
      self.write_message("Order", m_nCode, "ReadCertByID")
    except Exception as e:
      print(("error！" + e)

  def set_order_limit(self):
    try:
      # 1 == Future
      nMarketType = 1
      m_nCode = self.skO.SetMaxQty(nMarketType, self.config['quantity_limit'])
      self.write_message("Order", m_nCode, "SetMaxQty")
      m_nCode = self.skO.SetMaxCount(nMarketType, self.config['quantity_limit'])
      self.write_message("Order", m_nCode, "SetMaxCount")
    except Exception as e:
      print("error！" + e)





  def write_message(self, str_type, nCode, str_message):
    str_info = ""
    if (nCode != 0):
      str_info = "【" + self.skC.SKCenterLib_GetLastLogInfo() + "】"
    print("【" + str_type + "】【" + str_message + "】【"
          + self.skC.SKCenterLib_GetReturnCodeMessage(nCode) + "】" + str_info)


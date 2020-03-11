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


  def login(self, id, password):
    try:
      self.skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Reply")
      m_nCode = self.skC.SKCenterLib_Login(id, password)
      self.skC.SKCenterLib_Debug(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Reply")
      if (m_nCode == 0):
        print("Login success: " + id)
      elif m_nCode == 151:
        print("Wrong password")
      else:
        print("Login fail: " + m_nCode)
    except Exception as e:
      print("Error: " + e)
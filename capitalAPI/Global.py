import os
import comtypes.client
comtypes.client.GetModule(os.path.split(os.path.realpath(__file__))[0] + r'\x64\SKCOM.dll')
import comtypes.gen.SKCOMLib as sk


def set_id(id):
    global GLOBAL_ID
    GLOBAL_ID = id


global GLOBAL_SERVER_TIME
GLOBAL_SERVER_TIME = None

global LOGGER_SYS
LOGGER_SYS = None

global skO, skC, skQ, skR, skOSQ, skOOQ

skO = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib)

skC = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)

skQ = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)

skR = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib)

skOSQ = comtypes.client.CreateObject(sk.SKOSQuoteLib,interface=sk.ISKOSQuoteLib)

skOOQ = comtypes.client.CreateObject(sk.SKOOQuoteLib,interface=sk.ISKOOQuoteLib)


import SKReplyLibEvent
import SKQuoteLibEvent
# comtypes使用此方式註冊callback
SKReplyEvent = SKReplyLibEvent.SKReplyLibEvent()
SKReplyLibEventHandler = comtypes.client.GetEvents(skR, SKReplyEvent)


# SKQuoteLibEventHandler = win32com.client.WithEvents(SKQuoteLib, SKQuoteLibEvents)
SKQuoteEvent = SKQuoteLibEvent.SKQuoteLibEvent()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)
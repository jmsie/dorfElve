import Global
skC = Global.skC

class MessageControl():
    def __init__(self, listInformation):
        self.listInformation = listInformation
        return

    # 顯示各功能狀態用的function
    def WriteMessage(self, strMsg):
        self.listInformation.insert('end', strMsg)
        self.listInformation.see('end')

    def SendReturnMessage(self, strType, nCode, strMessage):
        strInfo = ""
        if (nCode != 0):
            strInfo = "【" + skC.SKCenterLib_GetLastLogInfo() + "】"
        self.WriteMessage("【" + strType + "】【" + strMessage + "】【" + skC.SKCenterLib_GetReturnCodeMessage(nCode) + "】" + strInfo)

import Global


class SKOrderLibEvent():
    __account_list = dict(
        stock=[],
        future=[],
        sea_future=[],
        foreign_stock=[],
    )


    def OnAccount(self, bstrLogInID, bstrAccountData):
        strValues = bstrAccountData.split(',')
        strAccount = strValues[1] + strValues[3]
        if strValues[0] == 'TS':
            SKOrderLibEvent.__account_list['stock'].append(strAccount)
        elif strValues[0] == 'TF':
            SKOrderLibEvent.__account_list['future'].append(strAccount)
        elif strValues[0] == 'OF':
            SKOrderLibEvent.__account_list['sea_future'].append(strAccount)
        elif strValues[0] == 'OS':
            SKOrderLibEvent.__account_list['foreign_stock'].append(strAccount)
        Global.LOGGER_SYS.WriteMessage(SKOrderLibEvent.__account_list)

    def OnOpenInterest(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnFutureRights(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnAsyncOrder(self, nThreadID, nCode, bstrMessage):
        Global.LOGGER_SYS.WriteMessage("ThreadID:" + str(nThreadID) + "_Code:" + str(nCode) + "_Message:" + bstrMessage)


    def OnOverseaFutureOpenInterest(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnOverSeaFutureRight(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnOverseaFuture(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnOverseaOption(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnRealBalanceReport(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnBalanceQuery(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnRequestProfitReport(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnMarginPurchaseAmountLimit(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnAsyncOrderOLID(self, nThreadID, nCode, bstrMessage, bstrOrderLinkedID):
        strMsg = "Message: " + bstrMessage + " " + bstrOrderLinkedID
        Global.LOGGER_SYS.WriteMessage("ThreadID:" + str(nThreadID) + "_Code:" + str(nCode) + "_Message:" + strMsg)


    def OnStopLossReport(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)

    def OnTSSmartStrategyReport(self, bstrData):
        Global.LOGGER_SYS.WriteMessage(bstrData)
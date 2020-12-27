import Global

class SKQuoteLibEvent:

    def OnConnection(self, nKind, nCode):
        if (nKind == 3001):
            strMsg = "Connected!"
        elif (nKind == 3002):
            strMsg = "DisConnected!"
        elif (nKind == 3003):
            strMsg = "Stocks ready!"
        elif (nKind == 3021):
            strMsg = "Connect Error!"
        Global.LOGGER_SYS.WriteMessage(strMsg)

    def OnNotifyQuote(self, sMarketNo, sStockidx):
        pStock = Global.sk.SKSTOCK()
        m_nCode = Global.skQ.SKQuoteLib_GetStockByIndex(sMarketNo, sStockidx, pStock)
        strMsg = '代碼:',pStock.bstrStockNo,'--名稱:',pStock.bstrStockName,'--開盤價:',pStock.nOpen/math.pow(10,pStock.sDecimal),'--最高:',pStock.nHigh/math.pow(10,pStock.sDecimal),'--最低:',pStock.nLow/math.pow(10,pStock.sDecimal),'--成交價:',pStock.nClose/math.pow(10,pStock.sDecimal),'--總量:',pStock.nTQty
        Global.LOGGER_SYS.WriteMessage(strMsg)

    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        strMsg = "[OnNotifyHistoryTicks]", sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate
        Global.LOGGER_SYS.WriteMessage(strMsg)

    def OnNotifyTicks(self,sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        strMsg = "[OnNotifyTicks]", sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate
        Global.LOGGER_SYS.WriteMessage(strMsg)

    def OnNotifyServerTime(self,sHour,sMinute,sSecond,nTotal):
        strMsg = "%02d" % sHour,":","%02d" % sMinute,":","%02d" % sSecond
        Global.GLOBAL_SERVER_TIME['text'] = strMsg

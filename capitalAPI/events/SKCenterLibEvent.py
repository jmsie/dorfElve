class SKCenterLibEvent():
    #定時Timer通知
    def OnTimer(self,nTime):
        nTime = str(nTime).zfill(6)
        strMsg = "OnTime： " + nTime[0:2] + ":" + nTime[2:4] + ":" + nTime[4:]
        print(strMsg)

    #同意書未簽署通知
    def OnShowAgreement(self,bstrData):
        print(bstrData)

    #SGX API DMA專線下單連線狀態。
    def OnNotifySGXAPIOrderStatus(self,nStatus,bstrOFAccount):
        if nStatus == 3026:
            strMsg = (bstrOFAccount+"SGX_API專線建立完成")
        elif nStatus == 3002:
            strMsg = (bstrOFAccount+"SGX_API專線斷線")
        else:
            strMsg = (bstrOFAccount+"SGX_API登入失敗")
        print(strMsg)


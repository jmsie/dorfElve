class SKReplyLibEvent():

    def OnConnect(self, btrUserID, nErrorCode):
        if nErrorCode == 0:
            strMsg = btrUserID,"Connected!"
        else :
            strMsg = btrUserID,"Connect Error!"
        print(strMsg)

    def OnDisconnect(self, btrUserID, nErrorCode):
        if nErrorCode == 3002:
            strMsg = "OnDisconnect 您已經斷線囉~~~"
        else:
            strMsg = nErrorCode
        print(strMsg)

    def OnReplyMessage(self,bstrUserID, bstrMessages):
        sConfirmCode = -1
        print(bstrUserID + ": " + bstrMessages)
        return sConfirmCode

    def OnNewData(self,btrUserID,bstrData):
        cutData = bstrData.split(',')
        #strMsg = {" 委託序號 ": cutData[0] , " 委託種類 " : cutData[2] , " 委託狀態 " : cutData[3] ," 商品代碼 " : cutData[8] ,
        # " 委託書號 " : cutData[10]," 價格 " : cutData[11] , " 數量 " : cutData[20] ,
        #" 日期&時間 " : cutData[23] + " " +cutData[24] , "錯誤訊息" : cutData[-4] + " " + cutData[-3]}
        #WriteMessage( strMsg,ReplyInformation)
        print("OnNewData"+"\n"+cutData)

    def OnSolaceReplyDisconnect(self,btrUserID, nErrorCode):
        if nErrorCode == 3002:
            strMsg = "OnSolaceReplyDisconnect SK_SUBJECT_CONNECTION_DISCONNECT"
        else:
            strMsg = nErrorCode
        print(strMsg)

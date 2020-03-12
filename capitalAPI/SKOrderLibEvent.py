class SKOrderLibEvent():
    __account_list = dict(
        stock = [],
        future = [],
        sea_future = [],
        foreign_stock = [],
    )

    def OnAccount(self, bstrLogInID, bstrAccountData):
        print("OnAccount:")
        print(bstrLogInID)
        print(bstrAccountData)

    def OnOpenInterest(self,bstrData):
        print("OnOpenInterest: " + bstrData)

    def OnFutureRights(self,bstrData):
        print(bstrData);

    def OnAsyncOrder(self,nThreadID,nCode,bstrMessage):
        print("ThreadID:"+str(nThreadID)+"_Code:"+str(nCode)+"_Message:"+bstrMessage)


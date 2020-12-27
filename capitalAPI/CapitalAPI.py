# 先把API com元件初始化
import os, time
import comtypes.client

comtypes.client.GetModule(os.path.split(os.path.realpath(__file__))[0] + r"/x64/SKCOM.dll")
import Global

skC = Global.skC
skO = Global.skO
skR = Global.skR
skQ = Global.skQ
skOSQ = Global.skOSQ
skOOQ = Global.skOOQ

# 畫視窗用物件
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

# 數學計算用物件
import math

# 載入其他物件
import MessageControl
import Config
import Helpers

# ----------------------------------------------------------------------------------------------------------------------------------------------------

# 上半部登入框
class FrameLogin(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.group = LabelFrame(master, text="Login", style="Pink.TLabelframe")
        self.group.grid(column=0, row=0, padx=5, pady=5, sticky='W')

        self.create_widget()
        self.logger_sys = MessageControl.MessageControl(self.system_log)

        Global.LOGGER_SYS = self.logger_sys



    def create_widget(self):
        frame = Frame(self.group, style="Pink.TFrame")
        frame.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        frame.grid_columnconfigure(6, minsize=530)
        frame.grid_rowconfigure(1, minsize=40)
        # 帳號
        Label(frame, style="Pink.TLabel", text="帳號：").grid(column=0, row=0)
        # 輸入框
        self.user_name = StringVar()
        self.text_ID = Entry(frame, width=20, textvariable=self.user_name)
        self.text_ID["width"] = 50
        self.text_ID.grid(column=1, row=0)
        self.user_name.set(Helpers.get_user_name())

        # 密碼4
        Label(frame, style="Pink.TLabel", text="密碼：").grid(column=0, row=1)
        # 輸入框
        self.password = StringVar()
        self.text_password = Entry(frame, width=20, textvariable=self.password)
        self.text_password["width"] = 50
        self.text_password['show'] = '*'
        self.text_password.grid(column=1, row=1)
        self.password.set(Helpers.get_password())

        # 伺服器
        # 模擬平台
        self.__ResetServer = IntVar()
        Checkbutton(frame, style="Pink.TCheckbutton", text='模擬平台', variable=self.__ResetServer, onvalue=1,
                    offvalue=0).grid(column=3, row=0, padx=10)

        # 擬真平台
        self.__LoginOrderM = IntVar()
        Checkbutton(frame, style="Pink.TCheckbutton", text='擬真平台', variable=self.__LoginOrderM, onvalue=1,
                    offvalue=0).grid(column=4, row=0, padx=10)

        # SGX 專線屬性
        self.__SGXAuthority = IntVar()
        Checkbutton(frame, style="Pink.TCheckbutton", text="不連SGX專線", variable=self.__SGXAuthority, onvalue=1,
                    offvalue=0).grid(column=5, row=0, padx=10, sticky="w")

        # Login Button
        Button(frame, style="Pink.TButton", text="登入", command=self.click_login).grid(column=3, row=1, padx=10)

        # ID
        self.user_id = Label(frame, style="Pink.TLabel", text="<<ID>>")
        self.user_id.grid(column=4, row=1)

        self.server_time = Label(frame, style="Pink.TLabel", text="00:00:00")
        self.server_time.grid(column=5, row=1)

        Global.GLOBAL_SERVER_TIME = self.server_time

        # 訊息欄
        self.system_log = Listbox(frame, height=30, width=80)
        self.system_log.grid(column=0, row=2, columnspan=8, sticky='ew')

        sb = Scrollbar(frame, orient='vertical')
        sb.config(command=self.system_log.yview)
        sb.grid(column=9, row=2, columnspan=8, sticky='ew')

    def click_login(self):
        try:
            platform = ""
            user_name = self.text_ID.get().replace(' ', '')
            password = self.text_password.get().replace(' ', '')
            # 設置路徑
            m_nCode = skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Order")
            # Debug
            m_nCode = skC.SKCenterLib_Debug(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Order")
            # 模擬平台登入
            if self.__ResetServer.get() == 1:
                # skC.SKCenterLib_ResetServer("morder1.capital.com.tw")
                m_nCode = skC.SKCenterLib_ResetServer("morder1.capital.com.tw")
                m_nCode = skC.SKCenterLib_login(user_name, password)
                platform = "模擬平台登"
            # 擬真平台登入
            elif self.__LoginOrderM.get() == 1:
                m_nCode = skC.SKCenterLib_LoginOrderM(user_name, password)
                platform = "擬真平台"
            # 平台登入
            else:
                # 判定SGX開啟或關閉
                if self.__SGXAuthority.get() == 1:
                    m_nCode = skC.SKCenterLib_SetAuthority(0)
                else:
                    m_nCode = skC.SKCenterLib_SetAuthority(1)

                m_nCode = skC.SKCenterLib_login(user_name, password)
            # Login result
            if (m_nCode == 0):
                self.user_id["text"] = self.text_ID.get().replace(' ', '')
                Global.set_id(self.user_id["text"])
                self.logger_sys.WriteMessage(f"【 {platform}登入成功 】")
                # Launch quote, order, reply server
                self.launch()
            else:
                self.logger_sys.SendReturnMessage("Login", m_nCode, "Login")

        except Exception as e:
            messagebox.showerror("error！", e)

    def launch(self):
        self.connect_to_quote_server()
        self.get_server_time()
        self.initiate_order_lib()
        self.read_cert()
        self.get_account()
        self.set_max_order_quantity(Config.MAX_ORDER_QUANTITY)
        self.set_max_order_count(Config.MAX_ORDER_COUNT)
        self.unlock_order()


    def connect_to_quote_server(self):
        try:
           m_nCode = skQ.SKQuoteLib_EnterMonitor()
           Global.LOGGER_SYS.SendReturnMessage("Quote", m_nCode, "SKQuoteLib_EnterMonitor")
        except Exception as e:
            messagebox.showerror("error！",e)

    def disconnect_from_quote_server(self):
        try:
            m_nCode = skQ.SKQuoteLib_LeaveMonitor()
            if (m_nCode != 0):
                strMsg = "SKQuoteLib_LeaveMonitor failed!", skC.SKCenterLib_GetReturnCodeMessage(m_nCode)
                Global.LOGGER_SYS.WriteMessage(strMsg)
            else:
                Global.LOGGER_SYS.SendReturnMessage("Quote", m_nCode, "SKQuoteLib_LeaveMonitor")
        except Exception as e:
            messagebox.showerror("error！",e)

    def get_server_time(self):
        try:
           m_nCode = skQ.SKQuoteLib_RequestServerTime()
           Global.LOGGER_SYS.SendReturnMessage("Quote", m_nCode, "SKQuoteLib_RequestServerTime")
        except Exception as e:
            messagebox.showerror("error！",e)

    # 下單function
    # 1.下單物件初始
    def initiate_order_lib(self):
        try:
            m_nCode = skO.SKOrderLib_Initialize()
            Global.LOGGER_SYS.SendReturnMessage("Order", m_nCode, "SKOrderLib_Initialize")
        except Exception as e:
            messagebox.showerror("error！", e)


    # 2.讀取憑證
    def read_cert(self):
        try:
            m_nCode = skO.ReadCertByID(Global.GLOBAL_ID)
            Global.LOGGER_SYS.SendReturnMessage("Order", m_nCode, "ReadCertByID")
        except Exception as e:
            messagebox.showerror("error！", e)

    # 3.取得下單帳號
    def get_account(self):
        try:
            m_nCode = skO.GetUserAccount()
            Global.LOGGER_SYS.SendReturnMessage("Order", m_nCode, "GetUserAccount")
        except Exception as e:
            messagebox.showerror("error！", e)

    #5.限制委託量
    def set_max_order_quantity(self, max_quantity: int):
        try:
            # Future
            nMarketType = 1
            m_nCode = skO.SetMaxQty(nMarketType, max_quantity)
            Global.LOGGER_SYS.SendReturnMessage("Order", m_nCode, f"SetMaxQty: {max_quantity}")
        except Exception as e:
            messagebox.showerror("error！", e)


    # 6.限制委託筆數
    def set_max_order_count(self, max_count: int):
        try:
            nMarketType = 1
            m_nCode = skO.SetMaxCount(nMarketType, max_count)
            Global.LOGGER_SYS.SendReturnMessage("Order", m_nCode, f"SetMaxCount {max_count}")
        except Exception as e:
            messagebox.showerror("error！", e)

    #7.帳號解鎖
    def unlock_order(self):
        try:
            nMarketType = 1
            m_nCode = skO.UnlockOrder(nMarketType)
            Global.LOGGER_SYS.SendReturnMessage("Order", m_nCode, "UnlockOrder")
        except Exception as e:
            messagebox.showerror("error！", e)




if __name__ == '__main__':
    root = Tk()
    root.title("DORF ELVES")


    # Center
    FrameLogin(master=root)

    # OrderTab
    root.TabControl = Notebook(root)
    root.TabControl.grid(column=0, row=1, sticky='ew', padx=10, pady=5)

    root.mainloop()

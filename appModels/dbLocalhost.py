# -*- coding: UTF-8 -*-
import os
import time
import json
from flask import Flask, redirect, session


app = Flask(__name__)


class SysDataPath:
    adminData = os.getcwd()+"\\appData\\"

class Data:

    def __init__(self):
        self.refreshData()
        self.nowTime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    # 現有資料
    def getData(self):
        return self.data_


    # 更新資料
    def refreshData(self):
        self.data_ = self.loadUserData_()
        return self.data_


    # 判斷資料存在
    def loadUserData_(self):
        adminList = os.listdir(SysDataPath.adminData)
        data = {}
        for email in adminList:
            if email.find('.json') != -1:
                n, d = self.loadJSON(SysDataPath.adminData+email)
                data[n] = d
        return data


    # 讀取json檔
    def loadJSON(self, path):
        try:
            with open(path, "r") as f:
                newData = json.loads(f.read())
                print(newData)
                return newData['email'], newData
        except Exception as e:
            print(e)


    # 寫入json檔
    def writeData_(self, data):
        try:
            with open(SysDataPath.adminData + data['email'] + '.json', "w") as f:
                newData = json.dump(data, f, ensure_ascii=False)
                print("寫入json檔", newData)
        except Exception as e:
            print(e)


    # 註冊驗證
    def register(self, mail, name, password, passwordCheck):
        # 載入資料
        admin = self.data_
        try:
            # 驗證資料不得空白
            if(mail == "" or name == "" or password == "" or passwordCheck == ""):
                print("資料輸入不完整")
                return redirect("/?msg=資料輸入不完整")

            # 驗證密碼與再次輸入密碼是否一致
            if (password != passwordCheck):
                print("密碼兩次輸入不一致")
                return redirect("/?msg=密碼兩次輸入不一致")
            # 驗證信箱是否已被註冊
            if mail in admin:
                print("信箱已被註冊")
                return redirect("/?msg=信箱已被註冊")
                # return redirect(url_for('index.html', msg="信箱已被註冊", action="post"))
            # 註冊資料
            newData = {
                "email": mail,
                "name": name,
                "password": password,
                "type": "register",
                "time": self.nowTime
            }

            # 寫入json檔
            self.writeData_(newData)

            # 更新資料
            self.refreshData()

            print("註冊成功")
            return redirect("/?msg=註冊成功")

        except Exception as e:
            print(e)


    # 登入驗證
    def signin(self, mail, password):
        # 載入資料
        # admin = self.loadJSON()
        # 檢查登入帳號密碼是否在資料內
        try:
            if (mail in self.data_ and password == self.data_[mail]['password']):
                print("認證成功")
                # 權限控管
                session["adminEmail"] = mail
                # print('session["adminEmail"]為', session["adminEmail"])
                return redirect("/adminBoard?msg=歡迎進入網站內容管理系統")
            return redirect("/?msg=帳號或密碼輸入錯誤")

        except Exception as e:
            print(e)


if __name__ == "__main__":
    admin = Data()
    admin.register("admin5@admin.com", "admin5", "password5", "password5")
    # admin.loadJSON()
    # admin.login("admin5@admin.com", "admin5")
    # admin.register("admin1@admin.com", "admin1", "password1", "password1")
    # print(admin.getData())
    # path = os.getcwd()+"\\appData\\admin1@admin.com.json"
    # print(admin.loadJSON(path))

# -*- coding: UTF-8 -*-
import os
from base64 import b64encode
import time
from datetime import timedelta
from flask import *
from flask_cors import CORS
from appModels.dbLocalhost import Data
from appModels.model import DataBase


# # 設置日誌：時間戳、日誌層級、應用程序名稱、執行緒、日誌訊息。
# import logging
# logging.basicConfig(filename=os.getcwd()+"\\appData\\logging.log",level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
""" 改heroku logs """


# 初始化Flask伺服器
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)
app.config['SECRET_KEY'] = os.urandom(24)
# print("app.config['SECRET_KEY']",b64encode(app.config['SECRET_KEY']).decode('utf-8'))
# 設置密碼效期為7天，如果沒有設置則預設為瀏覽器關閉後即自動結束，需再設定開啟
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config["JSON_AS_ASCII"] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"


# 路由設置
# 首頁(註冊、登入)
@app.route("/")
def index():
    msg = request.args.get("msg", "")
    return render_template("index.html", msg=msg)


# 註冊
@app.route("/adminSignUp", methods=["POST"])
def adminSignUp():
    adminEmail = request.form.get("adminEmail")
    adminName = request.form.get("adminName")
    adminPassword = request.form.get("adminPassword")
    adminPasswordCheck = request.form.get("adminPasswordCheck")
    # 先在本地端測試，尚未串接資料庫
    admin = Data()
    return admin.register(adminEmail, adminName, adminPassword, adminPasswordCheck)


# 登入
@app.route("/adminSignin", methods=["POST"])
def adminSignin():
    adminEmail = request.form.get("adminEmail")
    adminPassword = request.form.get("adminPassword")
    # print(adminEmail,adminPassword)
    admin = Data()
    return admin.signin(adminEmail, adminPassword)


# 登出
@app.route("/adminSignout")
def adminSignout():
    # 移除session中的會員資訊
    del session["SECRET_KEY"]
    return redirect("/")


# 訊息公告
@app.route("/adminBoard")
def admin():
    if "SECRET_KEY" in session:
        msg = request.args.get("msg", "歡迎進入網站內容管理系統")
        return render_template("adminBoard.html", msg=msg)
    else:
        return redirect("/")


# 商品管理
@app.route("/adminProduct")
def adminProduct():
    if "SECRET_KEY" in session:
        return render_template("adminProduct.html")
    else:
        return redirect("/")


# 庫存管理
@app.route("/adminInventory")
def adminInventory():
    if "SECRET_KEY" in session:
        return render_template("adminInventory.html")
    else:
        return redirect("/")


# 進貨管理
@app.route("/adminPurchase")
def adminPurchase():
    if "SECRET_KEY" in session:
        return render_template("adminPurchase.html")
    else:
        return redirect("/")


# 訂單管理
@app.route("/adminOrder")
def adminOrder():
    if "SECRET_KEY" in session:
        return render_template("adminOrder.html")
    else:
        return redirect("/")


"""
原redirect()改API設置，
將前端另外獨立檔案實作，
前端js以ajax串接py，
appStart.py仍為路由設置
dbMongo.py為寫入讀取修改資料庫方法
model.py為串接前端和資料庫主要運算邏輯
"""
# 跨來源資源共享設置
CORS(app) #此為權限全開，不建議，註解
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# API測試
@app.route("/api/test", methods=["POST"])
def apiTest():
    # 取得前端傳過來的數值
    insertValues = request.get_json()
    print(insertValues)
    return jsonify({
        "test": "API_OK"
    })


# setCookie測試
@app.route("/api/setCookie", methods=["POST"])
def setcookie():
    resp = make_response('Setting cookie!')
    resp.set_cookie(key='userID', value='user', expires=time.time()+6*60)
    print("setCookie測試",resp)
    return resp


# getCookie測試
@app.route("/api/getCookie", methods=["POST"])
def getcookie():
    resp = request.cookies.get('userID')
    print("getCookie測試",resp)
    return resp


# 檢查header是否帶token測試
@app.route("/api/getToken", methods=["POST"])
def getToken():
    # print(request.headers)
    resp = request.headers.get('Authorization')
    print(resp)
    # inputValues = request.get_json()
    # print(inputValues)
    return resp


@app.errorhandler(404)
def error_404(error):
    """這個handler可以catch住所有abort(404)以及找不到對應router的處理请求"""
    response = dict(status=404, message="404 Not Found")
    return jsonify(response), 404

# @app.errorhandler(Exception)
# def error_500(error):
#     """这个handler可以catch住所有的abort(500)和raise exeception."""
#     response = dict(status=400, message="500 Error")
#     return jsonify(response), 400


# API註冊
# API-admin/singup
@app.route("/api/admin/singup", methods=["POST"])
def apiAdminSingup():
    # 取得前端傳過來的資訊
    inputValues = request.get_json()
    print(inputValues)
    # 命令實體函數驗證註冊資料並回傳
    admin = DataBase()
    msg = admin.register(inputValues)
    print("回傳訊息",msg)
    response = dict(status=msg['status'], message=msg['message'])
    response = make_response(jsonify(response), msg['status'])
    return response


# API登入
# API-admin/singin
@app.route("/api/admin/signin", methods=["POST"])
def apiAdminSingin():
    # 取得前端傳過來的資訊
    inputValues = request.get_json()
    print(inputValues)
    # 命令實體函數驗證資料並回傳
    admin = DataBase()
    msg = admin.signin(inputValues)
    response = dict(status=200, message="登入成功",token=msg)
    response = make_response(jsonify(response), 200)
    response.headers["Authorization"] = msg
    return response



# 登出
@app.route("/api/admin/signout", methods=["POST"])
def apiAdminSignout():
    # 移除資料庫的Authorization和tokenTime
    token = request.headers.get('Authorization')
    msg = admin.delSession(token)
    return jsonify(msg)




if __name__ == '__main__':
    admin = DataBase()
    # Flask的預設配置不允許外部訪問，若要配置在產品的伺服器中，要加上"0.0.0.0"
    # debug=True為開啟debug模式，程式碼的任何修改，儲存後會立即生效，又稱為熱部屬功能
    # app.run("0.0.0.0", debug=True, port=3000)
    # app.run(debug=True)
    # 部屬改為debug=False
    # app.run(host='0.0.0.0', port=3000, debug=True)

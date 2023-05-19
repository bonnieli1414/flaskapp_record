# -*- coding: UTF-8 -*-
import os
from base64 import b64encode
import time
from datetime import timedelta
from flask import *
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from appModels.dbLocalhost import Data
from appModels.model import DataBase
from appModels.dbMongo import MongoData


# 初始化Flask伺服器
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config["JSON_AS_ASCII"] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"


# 跨來源資源共享設置
# CORS(app)
CORS(app, resources={
    r"/api/*": {
        "origins": "*"
    }
})


# 自定義的json錯誤處理
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "status": e.code,
        "message": e.name,
        "description": e.description
    })
    response.content_type = "application/json"
    return response


"""
API路由設置-會員相關(後台管理員)
"""


# 1.[POST]註冊 /api/admin/signup
@app.route("/api/admin/signup", methods=["POST"])
def apiAdminSignup():
    try:
        inputValues = request.get_json()
        admin = DataBase()
        msg = admin.register(inputValues, "adminMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 400,
            "message": f"Bad Request {str(e)}"
        }
        return jsonify(response)


# 2.[POST]登入 /api/admin/signin
@app.route("/api/admin/signin", methods=["POST"])
def apiAdminSignin():
    try:
        inputValues = request.get_json()
        admin = DataBase()
        msg = admin.signin(inputValues, "adminMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 3.[PUT]變更資料 /api/admin/changeInfo
@app.route("/api/admin/changeInfo", methods=["PUT"])
def apiAdminChangeInfo():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 變更資料
    try:
        inputValues = request.get_json()
        msg = admin.changeInfo(
            inputValues, tokenMsg["message"][0]["no"], "adminMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 4.[POST]登出 /api/admin/signout
@app.route("/api/admin/signout", methods=["POST"])
def apiAdminSignout():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    try:
        admin = DataBase()
        inputToken = request.headers['Authorization']
        msg = admin.delToken(
            inputToken, tokenMsg["message"][0]["no"], "adminMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


"""
API路由設置-產品相關(後台管理員)
"""


# 1.[POST]新增產品資料 /api/admin/product
@app.route("/api/admin/product", methods=["POST"])
def apiAdminProduct():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 新增資料
    try:
        inputValues = request.get_json()
        msg = admin.addData(inputValues, "product")
        return jsonify(msg)
    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 2.[GET]取得"全部"產品資料 /api/admin/products/all
@app.route("/api/admin/products/all", methods=["GET"])
def apiAdminProductsAll():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 查詢產品資料
    try:
        product = MongoData()
        msg = product._collection_find("product")
        response = {
            "status": 200,
            "message": msg
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 3.[GET]取得"單一"產品資料 /api/admin/product/<id>
# 4.[PUT]修改"單一"產品資料 /api/admin/product/<id>
# 5.[DELETE]刪除"單一"產品資料 /api/admin/product/<id>
@app.route("/api/admin/product/<id>", methods=["GET", "PUT", "DELETE"])
# id是指商品編號
def apiAdminProductId(id):
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    try:
        product = MongoData()
        queryObjData = {"no": id}
        # [GET]取得"單一"產品資料
        if (request.method == "GET"):
            msg = product._MongoData__collection_find_one(
                queryObjData, "product")

        # [PUT]修改"單一"產品資料
        elif(request.method == "PUT"):
            inputValues = request.get_json()
            sysInfo = {"updateTime": time.time()}
            inputValues.update(sysInfo)
            msg = product._MongoData__collection_update_one(
                "$set", queryObjData, inputValues, "product")

        # [DELETE]刪除"單一"產品資料
        elif(request.method == "DELETE"):
            msg = product._MongoData__collection_delete_one(
                queryObjData, "product")

        response = {
            "status": 200,
            "message": msg
        }
        print("response", response)
        return jsonify(response)

    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


"""
API路由設置-物料清單相關(後台管理員)
"""


# 1.[POST]新增物料清單資料 /api/admin/BOM
@app.route("/api/admin/BOM", methods=["POST"])
def apiAdminBOM():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 新增資料
    try:
        inputValues = request.get_json()
        msg = admin.addData(inputValues, "material")
        return jsonify(msg)
    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 2.[GET]取得"全部"物料清單資料 /api/admin/BOM/all
@app.route("/api/admin/BOM/all", methods=["GET"])
def apiAdminBOMAll():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 查詢物料資料
    try:
        material = MongoData()
        msg = material._collection_find("material")
        response = {
            "status": 200,
            "message": msg
        }
        return jsonify(response)

    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 3.[GET]取得"單一"物料清單資料 /api/admin/BOM/<id>
# 4.[PUT]修改"單一"物料清單資料 /api/admin/BOM/<id>
# 5.[DELETE]刪除"單一"物料清單資料 /api/admin/BOM/<id>
@app.route("/api/admin/BOM/<id>", methods=["GET", "PUT", "DELETE"])
def apiAdminBOMId(id):
    # id是指物料編號
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    try:
        material = MongoData()
        queryObjData = {"no": id}
        # [GET]取得"單一"物料清單資料
        if (request.method == "GET"):
            msg = material._MongoData__collection_find_one(
                queryObjData, "material")

        # [PUT]修改"單一"物料清單資料
        elif(request.method == "PUT"):
            inputValues = request.get_json()
            sysInfo = {"updateTime": time.time()}
            inputValues.update(sysInfo)
            msg = material._MongoData__collection_update_one(
                "$set", queryObjData, inputValues, "material")

        # [DELETE]刪除"單一"物料清單資料
        elif(request.method == "DELETE"):
            msg = material._MongoData__collection_delete_one(
                queryObjData, "material")

        response = {
            "status": 200,
            "message": msg
        }
        print(response)
        return jsonify(response)

    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


"""
API路由設置-供應商相關(後台管理員)
"""


# 1.[POST]新增供應商資料 /api/admin/supplier
@app.route("/api/admin/supplier", methods=["POST"])
def apiAdminSuppier():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 新增資料
    try:
        inputValues = request.get_json()
        msg = admin.addData(inputValues, "supplier")
        return jsonify(msg)
    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 2.[GET]取得"全部"供應商資料 /api/admin/suppliers/all
@app.route("/api/admin/suppliers/all", methods=["GET"])
def apiAdminSuppliersAll():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 查詢供應商資料
    try:
        supplier = MongoData()
        msg = supplier._collection_find("supplier")
        response = {
            "status": 200,
            "message": msg
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 3.[GET]取得"單一"供應商資料 /api/admin/supplier/<id>
# 4.[PUT]修改"單一"供應商資料 /api/admin/supplier/<id>
# 5.[DELETE]刪除"單一"供應商資料 /api/admin/supplier/<id>
@app.route("/api/admin/supplier/<id>", methods=["GET", "PUT", "DELETE"])
# id是指供應商編號
def apiAdminSuppierId(id):
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    try:
        supplier = MongoData()
        queryObjData = {"no": id}
        # [GET]取得"單一"供應商資料
        if (request.method == "GET"):
            msg = supplier._MongoData__collection_find_one(
                queryObjData, "supplier")

        # [PUT]修改"單一"供應商資料
        elif(request.method == "PUT"):
            inputValues = request.get_json()
            sysInfo = {"updateTime": time.time()}
            inputValues.update(sysInfo)
            msg = supplier._MongoData__collection_update_one(
                "$set", queryObjData, inputValues, "supplier")

        # [DELETE]刪除"單一"供應商資料
        elif(request.method == "DELETE"):
            msg = supplier._MongoData__collection_delete_one(
                queryObjData, "supplier")

        response = {
            "status": 200,
            "message": msg
        }
        print("response", response)
        return jsonify(response)

    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


"""
API路由設置-訂單相關(後台管理員)
"""


# 1.[GET]取得"全部"訂單資料 /api/admin/orders/all
@app.route("/api/admin/orders/all", methods=["GET"])
def apiAdminOrdersAll():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 取得全部訂單資料
    try:
        orders = MongoData()
        msg = orders._collection_find("order")
        response = {
            "status": 200,
            "message": msg
        }
        return jsonify(response)
    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 2.[PATCH]修改"單一"訂單狀態(已處理/未處理) /api/admin/order/<id>
# 3.[DELETE]刪除"單一"訂單資料 /api/admin/order/<id>
@app.route("/api/admin/order/<id>", methods=["PATCH", "DELETE"])
def apiAdminOrderId(id):
    # id是訂單編號
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    order = MongoData()
    # 確認是否有該筆訂單號碼
    queryObjData = {"no": id}
    msg = order._MongoData__collection_find_one(queryObjData, "order")
    if ("'NoneType' object does not support item deletion" in msg):
        response = {
            "status": 404,
            "message": "查無該筆訂單編號"
        }
        return jsonify(response)

    try:
        # 修改"單一"訂單狀態(已處理/未處理)
        if (request.method == "PATCH"):
            inputValues = request.get_json()
            queryObjData = {"no": id}
            msg = order._MongoData__collection_update_one(
                "$set", queryObjData, inputValues, "order")
            response = {
                "status": 200,
                "message": msg
            }
            return jsonify(response)
        # 刪除"單一"訂單資料
        elif(request.method == "DELETE"):
            objData = {"no": id}
            msg = order._MongoData__collection_delete_one(objData, "order")
            response = {
                "status": 200,
                "message": msg
            }
            return jsonify(response)

    except Exception as e:
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


"""
API路由設置-進貨相關(後台管理員)
"""


# 1.[POST]新增進貨資料 /api/admin/purchase
@app.route("/api/admin/purchase", methods=["POST"])
def apiAdminPurchase():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    try:
        inputValues = request.get_json()
        purchase = DataBase()
        msg = purchase.addPurchase(inputValues, tokenMsg, "purchases")
        return jsonify(msg)
    except Exception as e:
        response = {
            "status": 400,
            "message": f"Bad Request {str(e)}"
        }
        return jsonify(response)


# 2.[GET]取得"全部"進貨資料 /api/admin/purchases/all
@app.route("/api/admin/purchases/all", methods=["GET"])
def apiAdminPurchaseAll():
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 取得進貨資料
    try:
        purchase = MongoData()
        msg = purchase._collection_find("purchases")
        response = {
            "status": 200,
            "message": msg
        }
        return response
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 3.[GET]取得"單一"進貨資料 /api/admin/purchase/<id>
# 4.[PATCH]修改進貨資料(已點收/未點收) /api/admin/purchase/<id>
# 5.[DELETE]刪除"單一"進貨資料 /api/admin/purchase/<id>
@app.route("/api/admin/purchase/<id>", methods=["GET", "PATCH", "DELETE"])
def apiAdminPurchaseId(id):
    # 驗證token
    admin = DataBase()
    tokenMsg = admin.checkToken("adminMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 確認是否有該筆進貨編號
    queryObjData = {"no": id}
    purchases = MongoData()
    msg = purchases._MongoData__collection_find_one(queryObjData, "purchases")

    if ("'NoneType' object does not support item deletion" in msg):
        response = {
            "status": 404,
            "message": "查無該筆進貨編號"
        }
        return jsonify(response)

    try:
        # 取得"單一"進貨資料
        if (request.method == "GET"):
            queryObjData = {"no": id}
            response = {
                "status": 200,
                "message": msg
            }
            return jsonify(response)
        # 修改進貨資料
        elif (request.method == "PATCH"):
            inputValues = request.get_json()
            print("輸入的值", inputValues)
            queryObjData = {"no": id}
            msg = admin.checkPurchase(msg, inputValues)
            print(jsonify(msg))
            return jsonify(msg)
        # 刪除"單一"進貨資料
        elif (request.method == "DELETE"):
            queryObjData = {"no": id}
            msg = purchases._MongoData__collection_delete_one(
                queryObjData, "purchases")
            response = {
                "status": 200,
                "message": msg
            }
            return jsonify(response)

    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)}"
        }
        return jsonify(response)


"""
API路由設置-產品相關(前台使用者)
"""


# 1.[GET]取得"全部"產品資料 /api/user/products/all
@app.route("/api/user/products/all", methods=["GET"])
def userProductsAll():
    try:
        product = MongoData()
        msg = product._collection_find("product")
        response = {
            "status": 200,
            "message": msg
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        abort(404)


# 2.[GET]取得"單一"產品資料 /api/user/product/<id>
@app.route("/api/user/product/<id>", methods=["GET"])
def userProduct(id):
    try:
        product = MongoData()
        objData = {"no": id}
        msg = product._MongoData__collection_find_one(objData, "product")
        if ("'NoneType' object does not support item deletion" not in msg):
            response = {
                "status": 200,
                "message": msg
            }
            return jsonify(response)
        else:
            response = {
                "status": 404,
                "message": "找不到這個商品編號"
            }
            return jsonify(response)
    except Exception as e:
        print(e)
        abort(404)


"""
API路由設置-會員相關(前台會員)
"""


# 1.[POST]註冊 /api/user/signup
@app.route("/api/user/signup", methods=["POST"])
def apiUserSignup():
    try:
        inputValues = request.get_json()
        user = DataBase()
        msg = user.register(inputValues, "userMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 400,
            "message": f"Bad Request {str(e)}"
        }
        return jsonify(response)


# 2.[POST]登入 /api/user/signin
@app.route("/api/user/signin", methods=["POST"])
def apiUserSignin():
    try:
        inputValues = request.get_json()
        user = DataBase()
        msg = user.signin(inputValues, "userMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 3.[PUT]變更資料 /api/user/changeInfo
@app.route("/api/user/changeInfo", methods=["PUT"])
def apiUserChangeInfo():
    # 驗證token值
    user = DataBase()
    tokenMsg = user.checkToken("userMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 變更資料
    try:
        inputValues = request.get_json()
        msg = user.changeInfo(
            inputValues, tokenMsg["message"][0]["no"], "userMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


# 4.[POST]登出 /api/user/signout/<id>
@app.route("/api/user/signout/<id>", methods=["POST"])
def apiUserSignout(id):
    try:
        user = DataBase()
        inputToken = request.headers['Authorization']
        msg = user.delToken(inputToken, id, "userMember")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)


"""
API路由設置-購物車相關(前台會員)
"""


# 1.[POST]加入購物車 /api/user/carts
# 2.[GET]取得購物車 /api/user/carts
# 3.[DELETE]刪除"全部"購物車 /api/user/carts
@app.route("/api/user/carts", methods=["POST", "GET", "DELETE"])
def apiUserCarts():
    # 驗證token值
    user = DataBase()
    tokenMsg = user.checkToken("userMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    try:
        # [GET]取得購物車
        if (request.method == "GET"):
            user = MongoData()
            objData = {"email": tokenMsg["message"][0]["email"]}
            msg = user._MongoData__collection_find_one(objData, "userMember")
            response = {
                "status": 200,
                "message": msg["cart"]
            }
            return jsonify(response)

        # [POST]加入購物車
        elif(request.method == "POST"):
            inputValues = request.get_json()
            msg = user.addCart(
                inputValues, tokenMsg["message"][0], "userMember")
            return jsonify(msg)

        # [DELETE]刪除"全部"購物車
        elif(request.method == "DELETE"):
            user = MongoData()
            queryObjData = {"email": tokenMsg["message"][0]["email"]}
            objData = {"cart": []}
            msg = user._MongoData__collection_update_one(
                "$unset", queryObjData, objData, "userMember")
            if (msg == [1, 1]):
                response = {
                    "status": 200,
                    "message": "刪除成功"
                }
            elif (msg == [1, 0]):
                response = {
                    "status": 400,
                    "message": "購物車為空值"
                }
            return jsonify(response)

    except Exception as e:
        print(e)
        response = {
            "status": 404,
            "message": f"{str(e)} Not Found"
        }
        return jsonify(response)

# 4.[PUT]編輯購物車 /api/user/cart/<id>
# 5.[DELETE]刪除購物車內的"單一"品項 /api/user/cart/<id>


@app.route("/api/user/cart/<id>", methods=["PUT", "DELETE"])
def apiUserCartId(id):
    # 驗證token值
    user = DataBase()
    tokenMsg = user.checkToken("userMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # [PUT]編輯購物車
    if (request.method == "PUT"):
        try:
            inputValues = request.get_json()
            msg = user.editCart(
                inputValues, tokenMsg["message"][0], id, "userMember")
            return jsonify(msg)
        except Exception as e:
            print(e)
            abort(404)

    # [DELETE]刪除購物車內的"單一"品項
    elif(request.method == "DELETE"):
        try:
            msg = user.delCart(tokenMsg["message"][0], id, "userMember")
            return jsonify(msg)
        except Exception as e:
            print(e)
            abort(404)


"""
API路由設置-訂單相關(前台會員)
"""


# 1.[POST]送出購物車(新增訂單) /api/user/order
@app.route("/api/user/order", methods=["POST"])
def apiUserOrder():
    # 驗證token值
    user = DataBase()
    tokenMsg = user.checkToken("userMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 新增訂單
    try:
        inputValues = request.get_json()
        msg = user.addOrder(
            inputValues, tokenMsg["message"][0], "order")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 400,
            "message": f"Bad Request {str(e)}"
        }
        return jsonify(response)


# 2.[GET]取得個人的"全部"訂單資料 /api/user/orders/all
@app.route("/api/user/orders/all", methods=["GET"])
def apiUserOrdersAll():
    # 驗證token值
    user = DataBase()
    tokenMsg = user.checkToken("userMember")
    if (tokenMsg["status"] != 200):
        return jsonify(tokenMsg)

    # 取得個人訂單資料
    try:
        order = MongoData()
        objData = {"email": tokenMsg["message"][0]["email"]}
        msg = order._MongoData__collection_find_one(objData, "order")
        return jsonify(msg)
    except Exception as e:
        print(e)
        response = {
            "status": 400,
            "message": f"Bad Request {str(e)}"
        }
        return jsonify(response)


if __name__ == '__main__':
    admin = DataBase()
    # app.run(host='0.0.0.0', port=3000, debug=True)
    app.run()

# -*- coding: utf-8 -*-
import os
import time
from flask import jsonify, make_response, request, session, abort
try:
    from dbMongo import SysDataPath, MongoData
except:
    from appModels.dbMongo import SysDataPath, MongoData


# 繼承MongoData類別
class DataBase(MongoData):

    def __init__(self):
        super().__init__()  # 使用super繼承MongoData__init__裡所有屬性

    # 判斷帳號是否存在，data為物件型別
    def loadUserData(self, data, collection):
        # 向資料庫篩選信箱是否在資料庫內
        result = self._MongoData__collection_find(
            {"email": data['email']}, collection
        )

        if (result != []):
            print("帳號存在，回傳資料", result)
            return result
        else:
            result = [{
                "email": None,
                "password": None
            }]
            print("帳號不存在，回傳None", result)
            return result

    # 註冊驗證
    def register(self, data, collection):
        try:
            # 驗證key值是否正確
            if ("email" not in data.keys() or "name" not in data.keys() or "password" not in data.keys() or "passwordCheck" not in data.keys()):
                response = {
                    "status": 400,
                    "message": "key值有誤"
                }
                print("key值有誤", response)
                return response

            # 驗證資料不得空白
            if(data['email'] == "" or data['name'] == "" or data['password'] == "" or data['passwordCheck'] == ""):
                response = {
                    "status": 400,
                    "message": "資料輸入不完整"
                }
                print("資料輸入不完整", response)
                return response

            # 驗證密碼與再次輸入密碼是否一致
            if (data['password'] != data['passwordCheck']):
                response = {
                    "status": 400,
                    "message": "密碼輸入不一致"
                }
                return response

            # 向資料庫篩選信箱是否在資料庫內
            result = self.loadUserData(data, collection)
            if (result[0]['email'] != None):
                response = {
                    "status": 400,
                    "message": "信箱已註冊"
                }
                return response

            # 製作管理員編號，規則：取得最後一筆編號+1
            database = self._collection_find(collection)

            if (result[0]['email'] == None and database == []):
                # 初始化編號
                if (collection == "adminMember"):
                    memberNo = "A00001"
                    level = "admin"
                elif (collection == "userMember"):
                    memberNo = "C00001"
                    level = "user"
            else:
                # 最後一筆編號+1
                lastDatabaseNo = database[len(database)-1]['no']
                memberNo = int(lastDatabaseNo[1:])+1
                memberNo = str(memberNo).zfill(5)
                if (collection == "adminMember"):
                    memberNo = f"A{memberNo}"
                    level = "admin"
                else:
                    memberNo = f"C{memberNo}"
                    level = "user"

            newData = {
                "no": memberNo,
                "level": level,
                "email": data["email"],
                "name": data["name"],
                "password": data["password"],
                "buildTime": self.timeStamp
            }

            # 寫入資料庫
            dataId = self._MongoData__collection_insert_one(
                newData, collection)

            print("註冊成功id是", dataId)
            response = {
                "status": 200,
                "message": "註冊成功"
            }
            return response

        except Exception as e:
            print(str(e))
            abort(400)

    # 登入驗證
    def signin(self, data, collection):
        try:
            # 驗證key值是否正確
            if ("email" not in data.keys() or "password" not in data.keys()):
                response = {
                    "status": 400,
                    "message": "key值有誤"
                }
                print("key值有誤", response)
                return response

            # 載入帳號資料
            result = self.loadUserData(data, collection)
            print("載入帳號資料", result)
            if (result[0]['email'] == None):
                abort(404)

            # 檢查登入帳號密碼是否在資料內
            if (data['email'] in result[0]['email'] and data['password'] == result[0]['password']):

                # # 設定session資料
                # session['username'] = data['email']
                # session["SECRET_KEY"] = os.urandom(16).hex()
                # # 開啟session的有效時間
                # session.permanent = True
                # print(session)

                # 設定Bearer Token
                BearerToken = "Bearer " + os.urandom(24).hex()
                print("BearerToken", BearerToken)

                # 向資料庫寫入token和到期時間(1天)
                insertType = "$set"
                queryObjData = {"email": data['email']}
                setObjData = {
                    "token": BearerToken,
                    "tokenExpire": self.timeStamp + 86400
                }
                msg = self._MongoData__collection_update_many(
                    insertType, queryObjData, setObjData, collection)
                print("寫入token值和到期時間，回傳結果", msg)

                # 回傳驗證結果
                response = {
                    "status": 200,
                    "message": "登入成功",
                    "token": BearerToken
                }
                # response = make_response(jsonify(response))
                # response.headers["Authorization"] = msg['token']
                print("登入成功", response)
                return response
            else:
                abort(404)
        except Exception as e:
            print(e)
            abort(404)

    # 判斷header須帶有token以及token未到期
    def checkToken(self, collection):
        try:
            inputToken = request.headers['Authorization']
            # 查詢資料庫是否有該組token
            result = self._MongoData__collection_find(
                {"token": inputToken}, collection
            )
            # print("確認token", result)

            # 判斷token是否未到期
            if (result != []):
                tokenExpire = result[0]['tokenExpire']
                nowTime = int(time.time())
                if (tokenExpire > nowTime):
                    response = {
                        "status": 200,
                        "message": result
                    }
                    return response
            # 以上兩個條件只要其中一項不符，則回覆驗證過期
            response = {
                "status": 401,
                "message": "驗證過期，請重新登入"
            }
            return response
        except Exception as e:
            response = {
                "status": 401,
                "message": "驗證錯誤"
            }
            return response

    # 變更資料
    def changeInfo(self, data, id, collection):
        try:
            newData = {
                "name": data['name'],
                "password": data['password'],
                "sex": data['sex'],
                "telephone": data['telephone'],
                "address": data['address'],
                "updateTime": self.timeStamp
            }
            insertType = "$set"
            queryObjData = {"no": id}
            setObjData = newData
            msg = self._MongoData__collection_update_one(
                insertType, queryObjData, setObjData, collection)
            print("變更結果", msg)
            response = {
                "status": 200,
                "message": msg
            }
            return response

        except Exception as e:
            print(e)
            response = {
                "status": 400,
                "message": "key值有誤"
            }
            print(response)
            return response

    # 移除資料庫的token和tokenExpire
    def delToken(self, token, id, collection):
        # print("目前尚存session", session.get('username'))
        # # 刪除session
        # session['username'] = False
        # print("session設定為False", session.get('username'))

        # 刪除token
        insertType = "$unset"
        queryObjData = {"token": token}
        ObjData = {"token": "", "tokenExpire": ""}
        msg = self._MongoData__collection_update_many(
            insertType, queryObjData, ObjData, collection)
        print("刪除token", msg)
        if (msg == [1, 1]):
            response = {
                "status": 200,
                "message": "刪除token成功"
            }
            print("刪除指定token", response)
            return response

    # 判斷名稱是否存在
    def loadNameData(self, data, collection):
        # 向資料庫篩選信箱是否在資料庫內
        result = self._MongoData__collection_find(
            {"name": data['name']}, collection
        )

        if(result != []):
            print("名稱存在，回傳資料", result)
            return result
        else:
            result = [{
                "no": None
            }]
            print("名稱不存在，回傳None", result)
            return result

    # 新增商品、物料、供應商資料
    def addData(self, data, collection):

        # 向資料庫篩選信箱是否在資料庫內
        result = self.loadNameData(data, collection)
        if (result[0]['no'] != None):
            response = {
                "status": 400,
                "message": "名稱之前已新增"
            }
            return response

        # 製作編號，規則：取得最後一筆編號+1，沒有則預設1
        database = self._collection_find(collection)
        print(database)

        if (result[0]['no'] == None and database == []):
            # 初始化編號
            if (collection == "product"):
                dataNo = "P00001"
            elif (collection == "supplier"):
                dataNo = "S00001"
            elif (collection == "material"):
                dataNo = "M00001"
        else:
            # 最後一筆編號+1
            lastDatabaseNo = database[len(database)-1]['no']
            dataNo = int(lastDatabaseNo[1:])+1
            dataNo = str(dataNo).zfill(5)
            if (collection == "product"):
                dataNo = f"P{dataNo}"
            elif(collection == "supplier"):
                dataNo = f"S{dataNo}"
            elif(collection == "material"):
                dataNo = f"M{dataNo}"

        # 資料分類
        if (collection == "product"):
            productData = {
                "no": dataNo,
                "finishDegree": data["finishDegree"],
                "category": data["category"],
                "name": data["name"],
                "description": data["description"],
                "picture": data["picture"],
                "online": data["online"],
                "price": int(data["price"]),
                "sale": int(data["sale"]),
                "inventory": int(data["inventory"]),
                "supplier": data["supplier"],
                "haveBOM": data["haveBOM"],
                "buildTime": self.timeStamp,
                "updateTime": self.timeStamp
            }
            newData = productData
        elif(collection == "supplier"):
            supplierData = {
                "no": dataNo,
                "name": data["name"],
                "telephone": data["telephone"],
                "contact": data["contact"],
                "deliveryDate": data["deliveryDate"],
                "buildTime": self.timeStamp,
                "updateTime": self.timeStamp
            }
            newData = supplierData
        elif(collection == "material"):
            materialData = {
                "no": dataNo,
                "finishDegree": "物料",
                "category": data["category"],
                "name": data["name"],
                "unit": data["unit"],
                "price": int(data["price"]),
                "inventory": int(data["inventory"]),
                "supplier": data["supplier"],
                "buildTime": self.timeStamp,
                "updateTime": self.timeStamp
            }
            newData = materialData
        # 寫入資料庫
        dataId = self._MongoData__collection_insert_one(
            newData, collection)
        print("註冊成功id是", dataId)

        response = {
            "status": 200,
            "message": "新增成功"
        }
        return response

    # 加入購物車
    def addCart(self, newData, data, collection):

        # 資料確認
        try:
            newData = {
                "cartNo": f"T{(int(self.timeStamp*1000000))}",
                "quantity": newData["quantity"],
                "total": newData["total"],
                "product": {
                    "no": newData["product"]["no"],
                    "finishDegree": newData["product"]["finishDegree"],
                    "category": newData["product"]["category"],
                    "name": newData["product"]["name"],
                    "description": newData["product"]["description"],
                    "picture": newData["product"]["picture"],
                    "price": newData["product"]["price"],
                    "sale": newData["product"]["sale"]
                }
            }
        except Exception as e:
            print(e)
            response = {
                "status": 400,
                "message": "key值有誤"
            }
            print(response)
            return response

        # 加入購物車
        try:
            queryObjData = {"email": data["email"]}
            # 已有購物車，購物車內若是空值仍視同有購物車
            if (data.__contains__("cart")):
                data["cart"].append(newData)
                setObjData = {"cart": data["cart"]}
                print("已有購物車", newData)

            # 尚未有購物車
            else:
                setObjData = {"cart": [newData]}
                print("尚未有購物車", setObjData)

            msg = self._MongoData__collection_update_one(
                "$set", queryObjData, setObjData, collection)
            response = {
                "status": 200,
                "message": "新增成功"
            }
            return response

        except Exception as e:
            print(e)
            response = {
                "status": 400,
                "message": f"Bad Request {str(e)}"
            }
            return jsonify(response)

    # 判斷是否有購物車
    def haveCart(self, data):
        # 有購物車
        if (data.__contains__("cart") and len(data["cart"]) > 0):
            print("有購物車")
            return True
        # 無購物車
        else:
            print("沒有購物車")
            return False

    # 編輯購物車
    def editCart(self, newData, data, cartId, collection):

        # 確認是否有購物車
        msg = self.haveCart(data)
        if(msg == False):
            response = {
                "status": 404,
                "message": "無購物車資料"
            }
            return jsonify(response)

        # 變更資料
        for i in range(len(data["cart"])):
            if (cartId == data["cart"][i]["cartNo"]):
                data["cart"][i]["quantity"] = newData["quantity"]
                data["cart"][i]["total"] = newData["total"]

        # 寫入資料庫
        queryObjData = {"email": data["email"]}
        objData = data
        msg = self._MongoData__collection_update_one(
            "$set", queryObjData, objData, collection)

        if (msg == [1, 1]):
            response = {
                "status": 200,
                "message": "變更成功"
            }
        elif (msg == [1, 0]):
            response = {
                "status": 200,
                "message": "資料無變更"
            }
        return response

    # 刪除購物車
    def delCart(self, data, cartId, collection):
        # 確認是否有購物車
        msg = self.haveCart(data)
        if(msg == False):
            response = {
                "status": 404,
                "message": "無購物車資料"
            }
            return jsonify(response)

        # 刪除一筆品項資料
        for i in range(len(data["cart"])-1, -1, -1):
            print("========", data["cart"][i])
            if (cartId == data["cart"][i]["cartNo"]):
                data["cart"].pop(i)
        print(data)

        # 寫入資料庫
        queryObjData = {"email": data["email"]}
        msg = self._MongoData__collection_update_one(
            "$set", queryObjData, data, collection)
        if (msg == [1, 1]):
            response = {
                "status": 200,
                "message": "刪除成功"
            }
        elif (msg == [1, 0]):
            response = {
                "status": 200,
                "message": "資料已不存在"
            }
        return response

    # 購物車轉訂單
    def addOrder(self, data, tokenData, collection):

        try:
            # 訂購人資料確認
            orderObjData = {
                "no": f"O{(int(self.timeStamp*1000000))}",
                "email": data["email"],
                "receiver": data["receiver"],
                "receiverTel": data["receiverTel"],
                "receiverAddress": data["receiverAddress"],
                "userMsg": data["userMsg"],
                "allTotal": data["allTotal"],
                "payment": data["payment"],
                "buildTime": self.timeStamp,
                "updateTime": self.timeStamp
            }

            # 送出的購物品項不得少於1
            cartList = data["cart"]
            if (len(data["cart"]) < 1):
                response = {
                    "status": 400,
                    "message": "至少要有一個購物品項"
                }
                return response

            # 取得資料庫中的商品資料，主要是要查庫存量
            productData = self._collection_find("product")

            # 1.確認訂購數量不得大於庫存量
            # 2.符合第1項才扣除庫存量
            for m in range(len(cartList)):
                for n in range(len(productData)):
                    if (cartList[m]["product"]["no"] == productData[n]["no"]):

                        # 購買量大於庫存量，回傳拒絕
                        if (cartList[m]["quantity"] > productData[n]["inventory"]):
                            response = {
                                "status": 400,
                                "message": f"庫存量是{productData[n]['inventory']}，不得高於庫存量"
                            }
                            return response

                        # 小於或等於庫存量，扣庫存，寫入資料庫
                        elif (cartList[m]["quantity"] <= productData[n]["inventory"]):
                            newInventory = int(
                                productData[n]["inventory"])-int(cartList[m]["quantity"])
                            productData[n]["inventory"] = newInventory
                            queryObjData = {"no": productData[n]["no"]}
                            productObjData = {
                                "inventory": productData[n]["inventory"]}
                            inventoryMsg = self._MongoData__collection_update_one(
                                "$set", queryObjData, productObjData, "product")

            # 送到資料庫，訂單成立
            orderObjData.update({"cartList": cartList})
            msg = self._MongoData__collection_insert_one(
                orderObjData, collection)

            # 刪除已轉訂單的購物車品項，由後面索引開始刪除
            for i in range(len(cartList)-1, -1, -1):
                for j in range(len(tokenData["cart"])-1, -1, -1):
                    if (cartList[i]["cartNo"] == tokenData["cart"][j]["cartNo"]):
                        del tokenData["cart"][j]
            # print("新購物車資料",tokenData["cart"])

            queryObjData = {"email": tokenData["email"]}
            objData = {"cart": tokenData["cart"]}
            cartMsg = self._MongoData__collection_update_one(
                "$set", queryObjData, objData, "userMember")
            # print("更新資料庫內的購物車訊息", cartMsg)

            response = {
                "status": 200,
                "message": msg
            }
            return response
        except Exception as e:
            print(e)
            response = {
                "status": 400,
                "message": "key值輸入有誤"
            }
            return response

    # 新增進貨資料
    def addPurchase(self, data, id, collection):
        try:
            # 資料確認
            queryObjData = {
                "no": f"B{(int(self.timeStamp*1000000))}",
                "orderer": id["message"][0]["email"],
                "orderTime": self.timeStamp,
                "productNo": data["productNo"],
                "productName": data["productName"],
                "ordererNum": data["ordererNum"],
                "acceptDate": data["acceptDate"],
                "accepted": data["accepted"],
                "buildTime": self.timeStamp,
                "updateTime": self.timeStamp
            }

            # 寫入資料庫
            msg = self._MongoData__collection_insert_one(
                queryObjData, collection)
            response = {
                "status": 200,
                "message": msg
            }
            return response
        except Exception as e:
            print(e)
            response = {
                "status": 400,
                "message": "key值有誤"
            }
            print(response)
            return response

    # 1.將進貨狀態改為已點收
    # 2.點收後新增庫存數量
    def checkPurchase(self, data, inputValues):
        try:
            # 先確認之前是否已點收
            if (data['accepted']):
                return "已點收過"
            # 確認傳入的資料是未點收
            if(inputValues['accepted'] == "false"):
                return "傳入的值是未點收"

            print("傳進來的資料", data)
            # 篩選條件為產品序號
            # 點收數量加上原產品庫存
            queryObjData = {"no": data['productNo']}
            objData = {"inventory": int(data['ordererNum'])}
            print("篩選條件", queryObjData)
            print("請求物件", objData)
            if ("P" in data['productNo']):
                msg = self._MongoData__collection_update_one(
                    "$inc", queryObjData, objData, "product")
                print("P產品寫入新增庫存", msg)

            elif ("M" in data['productNo']):
                msg = self._MongoData__collection_update_one(
                    "$inc", queryObjData, objData, "material")
                print("M產品寫入新增庫存", msg)

            queryObjData = {'no': data['no']}
            print("篩選資料2", queryObjData)
            objData = {'accepted': True}
            msg2 = self._MongoData__collection_update_one(
                "$set", queryObjData, objData, "purchases")
            print("資料庫寫入已點收", msg2)
            response = {
                "status": 200,
                "message": {
                    "資料庫存已更新": msg,
                    "資料庫寫入已點收": msg2
                }
            }
            return response
        except Exception as e:
            print(e)
            response = {
                "status": 400,
                "message": "key值有誤"
            }
            print(response)
            return response


if __name__ == "__main__":
    admin = DataBase()

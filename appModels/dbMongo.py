# -*- coding: UTF-8 -*-
import os
import time
import pymongo
from bson.objectid import ObjectId


class SysDataPath:

    # 本地端路徑
    adminData = os.getcwd()+"\\appData\\"

    # Heroku路徑
    # adminData = os.getcwd()+"/appData/"

    # Mongo資料庫路徑
    Account = "..."
    Password = "..."
    Database = "website_manager"
    # Collection = "memberData"

    # 連線至Mongo資料庫
    client = pymongo.MongoClient(
        f"mongodb+srv://{Account}:{Password}@mycluster.fqroe83.mongodb.net/?retryWrites=true&w=majority")
    db = client[Database]  # 資料庫名稱
    # collection = db[Collection]  # 集合名稱


class MongoData:
    def __init__(self):
        # 與伺服器有8小時的時間差
        self.timeStamp = time.time()
        self.nowTime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    # 取得一筆文件資料
    def _collection_find_one(self, queryId, collection):
        try:
            self._data = SysDataPath.db[collection].find_one(ObjectId(queryId))
            return self._data
        except Exception as e:
            print("取得一筆文件資料發生錯誤", e)
            return e

    # 取得多筆文件資料
    def _collection_find(self, collection):
        try:
            text = []
            self._cursor = SysDataPath.db[collection].find()
            for doc in self._cursor:
                # 因為此id型別無法直接匯出，採刪除id
                del doc['_id']
                text.append(doc)
            return text
        except Exception as e:
            print("取得多筆文件資料發生錯誤", e)
            return e

    # 新增一筆文件資料，並回傳新增成功的id
    def __collection_insert_one(self, queryObjData, collection):
        try:
            self.__result = SysDataPath.db[collection].insert_one(queryObjData)
            return str(self.__result.inserted_id)
        except Exception as e:
            print("新增一筆文件資料發生錯誤", e)
            return e

    # 新增多筆文件資料，並回傳新增成功的多筆id
    def __collection_insert_many(self, arrayData, collection):
        try:
            self.__result = SysDataPath.db[collection].insert_many(arrayData)
            return self.__result.inserted_ids
        except Exception as e:
            print("新增多筆文件資料發生錯誤", e)
            return e

    """
    insertType可以帶入以下4種方法:
    $set:覆蓋、新增
    $inc加減數字(數字型態)
    $mul加減數字(數字型態)
    $unset清除
    並回傳篩選筆數和更新筆數
    """

    def __collection_update_one(self, insertType, queryObjData, objData, collection):
        try:
            SetObjData = {
                insertType: objData
            }
            self.__result = SysDataPath.db[collection].update_one(
                queryObjData, SetObjData)
            # print("符合篩選條件的文件數量", self._result.matched_count)
            # print("實際完成更新的文件數量", self._result.modified_count)
            return [self.__result.matched_count, self.__result.modified_count]
        except Exception as e:
            print("更新資料發生錯誤", e)
            return e

    # 修改多筆文件資料(覆蓋/新增)，並回傳篩選筆數和更新筆數
    def __collection_update_many(self, insertType, queryObjData, ObjData, collection):
        try:
            setObjData = {
                insertType: ObjData
            }
            self.__result = SysDataPath.db[collection].update_many(
                queryObjData, setObjData)
            # print("符合篩選條件的多筆文件數量", self.__result.matched_count)
            # print("實際完成更新的多筆文件數量", self.__result.modified_count)
            return [self.__result.matched_count, self.__result.modified_count]
        except Exception as e:
            print("修改多筆文件資料發生錯誤", e)
            return e

    # 刪除一筆文件資料，並回傳刪除筆數
    def __collection_delete_one(self, queryObjData, collection):
        try:
            self.__result = SysDataPath.db[collection].delete_one(queryObjData)
            # print(f"實際完成刪除的資料數量有{self.__result.deleted_count}筆")
            return self.__result.deleted_count
        except Exception as e:
            print("刪除一筆文件資料發生錯誤", e)
            return e

    # # 刪除多筆資料，並回傳刪除筆數
    def __collection_delete_many(self, queryObjData, collection):
        try:
            self.__result = SysDataPath.db[collection].delete_many(
                queryObjData)
            # print(f"實際完成刪除的資料數量{self.__result.deleted_count}")
            return self.__result.deleted_count
        except Exception as e:
            print("刪除多筆文件資料發生錯誤", e)
            return e

    # 篩選一筆文件資料，並回傳資料
    def __collection_find_one(self, queryObjData, collection):
        try:
            self.__data = SysDataPath.db[collection].find_one(queryObjData)
            # 因為此id型別無法直接匯出，採刪除id
            del self.__data['_id']
            return self.__data
        except Exception as e:
            print("篩選一筆文件資料發生錯誤", e)
            return str(e)

    # 篩選多筆文件資料，並回傳多筆資料
    def __collection_find(self, queryObjData, collection):
        try:
            text = []
            self.__cursor = SysDataPath.db[collection].find(queryObjData)
            print(SysDataPath.db[collection])
            # 使用for迴圈逐一取得文件加入列表
            for doc in self.__cursor:
                text.append(doc)
                # print(doc['name'])
                # print(text)
            return text
        except Exception as e:
            print("篩選多筆文件資料", e)
            return e

    # # 複合篩選條件
    # # 須同時符合多個條件，只會回傳符合條件的第1筆資料
    def __collection_find_one_and(self, queryObjData, collection):
        try:
            self.__data = SysDataPath.db[collection].find_one(queryObjData)
            print(self.__data['email'])
            return self.__data['email']
        except Exception as e:
            print("複合篩選條件發生錯誤", e)
            return e

    # # 只要符合其一個條件，並回傳多筆資料
    def __collection_find_or(self, queryObjData, collection):
        try:
            text = []
            self.__cursor = SysDataPath.db[collection].find(queryObjData)
            for doc in self.__cursor:
                print(doc['name'])
                text.append(doc)
            return text
        except Exception as e:
            print("篩選其中一個條件發生錯誤", e)
            return e

    # # 由小到大排序
    def __collection_find_sort_ASCENDING(self, data, collection):
        try:
            text = []
            self.__cursor = SysDataPath.db[collection].find({}, sort=[
                (data, pymongo.ASCENDING)
            ])
            for doc in self.__cursor:
                # print("由小到大", doc)
                text.append(doc)
            return text
        except Exception as e:
            print("由小到大排序發生錯誤", e)
            return e

    # # 由大到小排序
    def __collection_find_sort_DESCENDING(self, data, collection):
        try:
            text = []
            self._cursor = SysDataPath.db[collection].find({}, sort=[
                (data, pymongo.DESCENDING)
            ])
            for doc in self._cursor:
                # print("由大到小", doc)
                text.append(doc)
            return text
        except Exception as e:
            print("由大到小排序發生錯誤", e)
            return e

    # _id ObjectId 預設儲存了 4 位元組的時間戳記
    # 將_id ObjectId轉為字串格式
    def idChangeTimeString(self, dataId):
        struct_time = ObjectId(dataId).generation_time.timetuple()
        timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
        return timeString

    # 將_id ObjectId換算為+8小時的台北時間
    def idChangeTaipeiTime(self, dataId):
        struct_time = ObjectId(dataId).generation_time.timetuple()
        time_stamp = int(time.mktime(struct_time)) + 28800
        struct_time = time.localtime(time_stamp)
        timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
        return timeString


if __name__ == "__main__":
    admin = MongoData()
    # print(admin.timeStamp)
    print("查詢單筆會員資料",admin._collection_find_one("63b2e470699857424038bddd", "memberData"))
    queryObjData = {"test":123}
    admin._MongoData__collection_insert_one(queryObjData,"memberData")

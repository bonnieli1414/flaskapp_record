# Flaskapp

## 前後端分離的專案架構

### 前端程式

- html/css/javascript
- bootstrap
- jQuery

### 後端程式

- python

### 資料庫

- [MongoDB](https://www.mongodb.com/docs/manual/crud/)
- 文件資料儲存格式：JSON

___

## 環境設定

- 前端安裝套件：CDN安裝

1. bootstrap
2. jQuery

- 後端安裝套件：

1. pip install Flask
2. pip install Flask-Cors
3. pip install pymongo

___

## 前後端分離的主機和網域規畫-不同主機、不同網域

### 前端

- 前台website網址 <https://個人的github帳號.github.io/website/>
- 後台websiteAdmin網址 <https://個人的github帳號.github.io/websiteAdmin/>

### 後端

- flaskapp網址 <https://flaskapp-project.herokuapp.com/api/>

___

## 跨網域資源分享

透過Flask-Cors處理跨網域問題

___

## 前後端溝通Ajax

前端透過Fetch向後端發出http網路請求，傳遞的資料格式是JSON格式

___

## 前後端的檔案配置

### 前端檔案設置

#### 前台

```text
待補充....
```

#### 後台

```text
index
├── index.html(靜態檔案)
├── style.css
├── script.js
|    1.UI動態調整特效。
|    2.資料取得後的畫面呈現。
└── image
```

### 後端檔案設置

```text
appStart
├── appStart.py(路由設置)
└── appModels(資料處理)
    ├── model.py
    |    1.處理接收前端的資料驗證邏輯。
    |    2.向資料庫提取資料。
    |    3.回傳資料給前端。
    └── dbMongo.py(資料庫的寫入、讀取、修改)
```

___

## 前端HTTP請求方法

- GET：讀取
- POST：新增
- PUT：替換
- PATCH：部分更改
- DELETE：刪除

___

## 路由設計

### 除了前台使用者不須帶token，其他皆須帶入

```text
會員相關(前台會員)
1.[POST]註冊 /api/user/signup
2.[POST]登入 /api/user/signin
3.[PUT]變更資料 /api/user/changeInfo/{id}
4.[POST]登出 /api/user/signout

會員相關(後台管理員)
1.[POST]註冊 /api/admin/signup
2.[POST]登入 /api/admin/signin
3.[PUT]變更資料 /api/admin/changeInfo/{id}
4.[POST]登出 /api/admin/signout

產品相關(前台使用者)
1.[GET]取得"全部"產品資料 /api/user/products/all
2.[GET]取得"單一"產品資料 /api/user/product/{id}

產品相關(後台管理員)
1.[GET]取得"全部"產品資料 /api/admin/products/all
2.[GET]取得"單一"產品資料 /api/admin/product/{id}
3.[POST]新增產品資料 /api/admin/product
4.[PUT]修改"單一"產品資料 /api/admin/product/{id}
5.[DELETE]刪除"單一"產品資料 /api/admin/product/{id}

物料清單相關(後台管理員)
1.[GET]取得"全部"物料清單資料 /api/admin/BOM/all
2.[GET]取得"單一"物料清單資料 /api/admin/BOM/{id}
3.[POST]新增物料清單資料 /api/admin/BOM
4.[PUT]修改"單一"物料清單資料 /api/admin/BOM/{id}
5.[DELETE]刪除"單一"物料清單資料 /api/admin/BOM/{id}

供應商相關(後台管理員)
1.[GET]取得"全部"供應商資料 /api/admin/suppliers/all
2.[GET]取得"單一"供應商資料 /api/admin/supplier/{id}
3.[POST]新增供應商資料 /api/admin/supplier
4.[PUT]修改"單一"供應商資料 /api/admin/supplier/{id}
5.[DELETE]刪除"單一"供應商資料 /api/admin/supplier/{id}

購物車相關(前台會員)
1.[GET]取得購物車 /api/user/cart
2.[POST]加入購物車 /api/user/cart
3.[PUT]編輯購物車 /api/user/cart/{id}
4.[DELETE]刪除購物車內的"單一"品項 /api/user/cart/{id}
5.[DELETE]刪除"全部"購物車 /api/user/cart

訂單相關(前台會員)
1.[POST]送出購物車(新增訂單) /api/user/order
2.[GET]取得"全部"訂單資料 /api/user/orders/all
3.[GET]取得"單一"訂單資料 /api/user/order/{id}
4.[POST]付款 /api/user/pay/{id}

訂單相關(後台管理員)
1.[GET]取得"全部"訂單資料 /api/admin/orders/all
2.[PATCH]修改"單一"訂單狀態(已處理/未處理) /api/admin/order/{id}
3.[DELETE]刪除"單一"訂單資料 /api/admin/order/{id}
4.[DELETE]刪除"全部"訂單資料 /api/admin/orders/all

進貨相關(後台管理員)
1.[GET]取得"全部"進貨資料 /api/admin/purchases/all
2.[GET]取得"單一"進貨資料 /api/admin/purchase/{id}
3.[POST]新增進貨資料 /api/admin/purchase
4.[PATCH]修改進貨狀態(已點收/未點收) /api/admin/purchase/{id}
5.[DELETE]刪除"單一"進貨資料 /api/admin/purchase/{id}
6.[DELETE]刪除"全部"進貨資料 /api/admin/purchases/all
```

___

### 資料庫設計-Mongo以Document為導向

#### Mongo架構

```text
    資料庫(Database)
        └── 集合(Collection)
            └── 文件(Document)
```

#### 資料庫架構

```text
website_manager
├── 會員member(查詢GET、新增POST、修改PUT)
|   ├── 會員編號no：C00001系統帶入、A00001系統帶入
|   ├── 會員權限level：會員user系統帶入、管理員admin系統帶入
|   ├── 會員帳號email：電子信箱，客戶自訂
|   ├── 會員姓名name：客戶自訂
|   ├── 會員密碼password：客戶自訂
|   ├── 會員性別sex：客戶自訂
|   ├── 會員電話telephone：客戶自訂
|   ├── 會員地址address：客戶自訂
|   ├── 建立時間buildTime：系統帶入
|   ├── 更新時間updateTime：系統帶入
|   ├── token：系統帶入
|   ├── tokenExpire：系統帶入
|   └── 購物車內容，編號no：以T加上時間為序號(array型態)
|         ├── [(0-購物車編號，金額，數量，商品內容),
|              (1-購物車編號，金額，數量，商品內容),
|         └──  (2-...可寫入多筆)]
|
├── 商品product(查詢GET、新增POST、修改PUT、刪除DELETE)
|   ├── 商品編號no：P00001系統帶入
|   ├── 產品類別finishDegree：成品，管理員自訂
|   ├── 商品類別category：手機類、配件類，管理員自訂
|   ├── 商品名稱name：管理員自訂
|   ├── 商品描述description：管理員自訂
|   ├── 商品圖案picture：管理員自訂
|   ├── 商品上架online：是、否，管理員自訂
|   ├── 商品價格price：管理員自訂
|   ├── 商品特價sale：管理員自訂
|   ├── 庫存量inventory：客戶自訂
|   ├── 供應商supplier：名單、客戶自訂
|         └── 單一選單，供應商編號no：S00001
|
|   ├──物料清單haveBOM：有[物料清單編號]、false(array型態)
|        ├── [(0-組合編號，數量，物料內容),
|             (1-組合編號，數量，物料內容),
|        └──  (2-...可寫入多筆)]
|
|   ├── 建立時間buildTime：系統帶入
|   └── 更新時間updateTime：系統帶入
├── 供應商suppliers(查詢GET、新增POST、修改PUT、刪除DELETE)
|   ├── 供應商編號no：S00001，系統帶入
|   ├── 供應商名稱name：管理者自訂
|   ├── 供應商電話telephone：管理者自訂
|   ├── 聯絡人contact：管理者自訂
|   ├── 交期deliveryDate：管理者自訂
|   ├── 建立時間buildTime：系統帶入
|   └── 更新時間updateTime：系統帶入
|
├── 物料清單materials(查詢GET、新增POST、修改PUT、刪除DELETE)
|   ├── 物料編號no：M00001，系統帶入
|   ├── 產品類別finishDegree：物料
|   ├── 物料類別category：配件類
|   ├── 物料名稱name：管理者自訂
|   ├── 規格format：管理者自訂
|   ├── 單位unit：管理者自訂
|   ├── 庫存量amount：管理者自訂
|   ├── 建立時間buildTime：系統帶入
|   └── 更新時間updateTime：系統帶入
|
├── 訂單order(查詢GET、新增POST、修改PUT、刪除DELETE)
|   ├── 訂單編號no：以O加上時間為序號
|   ├── 會員信箱email：限定會員登入，由系統帶入
|   ├── 收件人receiver：會員自訂
|   ├── 收件電話receiverTel：會員自訂
|   ├── 收件地址receiverAddress：會員自訂
|   ├── 留言userMsg：會員自訂
|   ├── 總金額total：客戶傳入資料
|   ├── 訂單內容content (array型態)
|         ├──[(0-購物車內容),
|         ├── (1-購物車內容),
|         └── (3-可寫入多筆)]
|   ├── 建立時間buildTime：系統帶入
|   └── 更新時間updateTime：系統帶入
|
|
|
└── 進貨purchases(查詢GET、新增POST、修改PUT、刪除DELETE)
├── 進貨單號no：B00001
├── 預訂人orderer：由系統帶入登入的管理員email
├── 預訂時間orderTime：管理者自訂
├── 產品名稱name：管理者選擇
├── 產品編號product：管理者選擇(需篩選物料及產品名單)
├── 預訂數量ordererNum：管理者自訂
├── 預訂金額ordererMoney：管理者自訂
├── 建立時間buildTime：系統帶入
└── 更新時間updateTime：系統帶入
```
# flaskapp_record

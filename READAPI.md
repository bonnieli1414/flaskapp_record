# HTTPS API

APIURL[https://flaskapp-project.herokuapp.com]
__________________________________________________
[AUTH]

## API路由設置-會員相關(後台管理員)

### 1.[POST]註冊/api/admin/signup

#### post data

{
    "email": "admin1@admin.com",
    "name": "admin1",
    "password": "admin1",
    "passwordCheck": "admin1"
}

#### response

200 => { status: 200, message: "註冊成功" }
400 => { status: 400, message: "key值有誤"、"資料輸入不完整"、"密碼輸入不一致"、"信箱已註冊".... }
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "email": "admin1@admin.com",
  "name": "admin1",
  "password": "admin1",
  "passwordCheck": "admin1"
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/signup", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[POST]登入/api/admin/signin

#### post data

{
    "email": "admin1@admin.com",
    "password": "admin1"
}

#### response

200 => { status: 200, message: "登入成功", token: "..." }
400 => { status: 400, message: "key值有誤" }
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "email": "admin1@admin.com",
  "password": "admin1"
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/signin", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[PUT]變更資料 /api/admin/changeInfo

#### post data

{
    "name": "admin1@admin.com",
    "password": "admin1",
    "sex": "male",
    "telephone": "0910123456",
    "address": "桃園市中壢市健行路229號"
}

#### response

200 => { status: 200, message: [0,0] }
400 => { status: 400, message: "key值有誤" }
401 => { status: 401, message: "401 Unauthorized、驗證過期，請重新登入、驗證錯誤" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "name": "admin1@admin.com",
  "password": "admin1",
  "sex": "male",
  "telephone": "0910123456",
  "address": "桃園市中壢市健行路229號"
});

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/changeInfo", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

4.[POST]登出 /api/admin/signout/<id>

### 4.[POST]登出 /api/admin/signout

#### post data

{}

#### response

200 => { status: 200, message: "刪除token成功" }
404 => { status: 404, message: "找不到這個token" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/signout", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-產品相關(後台管理員)

### 1.[POST]新增產品資料 /api/admin/product

#### post data

{
    "finishDegree": "成品",
    "category": "手機類",
    "name": "motorola edge 20 pro",
    "description": "motorola edge 20 description",
    "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000" ,
    "online": "true",
    "price": 18000,
    "sale": 13000,
    "inventory": 0,
    "supplier": "摩托羅拉",
    "haveBOM": false
}

#### response

200 => { status: 200, message: "新增成功" }
400 => { status: 400, message: "名稱之前已新增"  }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Authorization", token);

let raw = JSON.stringify({
  "finishDegree": "成品",
  "category": "手機類",
  "name": "motorola edge 20 pro",
  "description": "motorola edge 20 description",
  "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000",
  "online": "true",
  "price": 18000,
  "sale": 13000,
  "inventory": 0,
  "supplier": "摩托羅拉",
  "haveBOM": false
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/product", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[GET]取得"全部"產品資料 /api/admin/products/all

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/products/all", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[GET]取得"單一"產品資料 /api/admin/product/P00002

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/product/P00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 4.[PUT]修改"單一"產品資料 /api/admin/product/P00002

***變更項目的key:value後端沒有做防呆機制，由前端處理
***finishDegree、category、name不能改

#### post data

{
    "description": "motorola edge 20 description",
    "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000" ,
    "online": "true",
    "price": 18000,
    "sale": 13000,
    "inventory": 0,
    "supplier": "摩托羅拉",
    "haveBOM": false
}

#### response

200 => { status: 200, message: [1,1] }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Authorization", token);

let raw = JSON.stringify({
  "description": "motorola edge 20 description",
  "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000",
  "online": "true",
  "price": 18000,
  "sale": 13000,
  "inventory": 0,
  "supplier": "摩托羅拉",
  "haveBOM": false
});

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/product/P00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 5.[DELETE]刪除"單一"產品資料 /api/admin/product/P00002

#### post data

{}

#### response

200 => { status: 200, message: 1 }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/product/P00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-物料清單相關(後台管理員)

### 1.[POST]新增物料清單資料 /api/admin/BOM

#### post data

{
    "finishDegree": "物料",
    "category": "面料類",
    "name": "10吋十字紋黑",
    "unit": "片",
    "price": 40,
    "inventory": 100,
    "supplier": "小毛"
}

#### response

200 => { status: 200, message: "新增成功" }
400 => { status: 400, message: "名稱之前已新增"  }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "finishDegree": "物料",
  "category": "面料類",
  "name": "10吋十字紋黑",
  "unit": "片",
  "price": 40,
  "inventory": 100,
  "supplier": "小毛"
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/BOM", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[GET]取得"全部"物料清單資料 /api/admin/BOM/all

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/BOM/all", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[GET]取得"單一"物料清單資料 /api/admin/BOM/M00002

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/BOM/M00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 4.[PUT]修改"單一"物料清單資料 /api/admin/BOM/M00002

***變更項目的key:value後端沒有做防呆機制，由前端處理
***finishDegree、category、name不能改

#### post data

{
    "unit": "個",
    "price": 1,
    "supplier": "小毛"
}

#### response

200 => { status: 200, message: [1,1] }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "format": "快充頭規格",
  "unit": "個",
  "amount": 1
});

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/BOM/M00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 5.[DELETE]刪除"單一"物料清單資料 /api/admin/BOM/M00002

#### post data

{}

#### response

200 => { status: 200, message: "1" }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/BOM/M00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-供應商相關(後台管理員)

### 1.[POST]新增供應商資料 /api/admin/supplier

#### post data

{
    "name": "摩托羅拉廠商",
    "telephone": "03-4581196",
    "contact": "摩先生",
    "deliveryDate": 3
}

#### response

200 => { status: 200, message: "新增成功" }
400 => { status: 400, message: "名稱之前已新增"  }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "name": "摩托羅拉廠商3",
  "telephone": "03-4581196",
  "contact": "摩先生",
  "deliveryDate": 3
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/supplier", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[GET]取得"全部"供應商資料 /api/admin/suppliers/all

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/suppliers/all", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[GET]取得"單一"供應商資料 /api/admin/supplier/S00002

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/supplier/S00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 4.[PUT]修改"單一"供應商資料 /api/admin/supplier/S00002

***變更項目的key:value後端沒有做防呆機制，由前端處理
***name不能改

#### post data

{
    "telephone": "03-4581196",
    "contact": "摩先生",
    "deliveryDate": 3
}

#### response

200 => { status: 200, message: [1,1] }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "telephone": "03-4581195",
  "contact": "摩先生",
  "deliveryDate": 3
});

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/supplier/S00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 5.[DELETE]刪除"單一"供應商資料 /api/admin/supplier/S00002

#### post data

{}

#### response

200 => { status: 200, message: "1" }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/supplier/S00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-訂單相關(後台管理員)

### 1.[GET]取得"全部"訂單資料 /api/admin/orders/all

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "...Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/orders/all", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[PATCH]修改"單一"訂單狀態(已處理/未處理) /api/admin/order/O1673969303435776

#### post data

{
    "handle":true
}

#### response

200 => { status: 200, message: [1,1] }
404 => { status: 404, message: "查無該筆訂單號碼、...Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "handle": true
});

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/order/O167396930343577", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[DELETE]刪除"單一"訂單資料 /api/admin/order/O1673969303435776

#### post data

{}

#### response

200 => { status: 200, message: "1" }
404 => { status: 404, message: "查無該筆訂單編號、...Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/order/O1673969303435776", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-進貨相關(後台管理員)

### 1.[POST]新增進貨資料 /api/admin/purchase

#### post data

{
    "productNo": "M00014",
    "productName": "10吋十字紋黑",
    "ordererNum": 100,
    "acceptDate": "2023/02/27",
    "accepted": false
}

#### response

200 => { status: 200, message: "..." }
400 => { status: 400, message: "key值有誤、Bad Request.." }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "productNo": "P00002",
  "productName": "motorola edge 30 pro",
  "ordererNum": 100,
  "ordererMoney": 3000
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/purchase", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[GET]取得"全部"進貨資料 /api/admin/purchases/all

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "...Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/purchases/all", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[GET]取得"單一"進貨資料 /api/admin/purchase/B1674049793259333

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/purchase/B1674049793259333", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 4.[PATCH]修改進貨資料(已點收/未點收) /api/admin/purchase/B1674049793259333

#### post data

{
    "accepted":true
}

#### response

200 => { status: 200, message: [1,1] }
404 => { status: 404, message: "查無該筆訂單號碼、...Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "receive": false
});

let requestOptions = {
  method: 'PATCH',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/purchase/B1674049793259333", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 5.[DELETE]刪除"單一"進貨資料 /api/admin/purchase/B1674049793259333

#### post data

{}

#### response

200 => { status: 200, message: "1" }
404 => { status: 404, message: "查無該筆進貨編號、...Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/admin/purchase/B1674049793259333", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-產品相關(前台使用者)

### 1.[GET]取得"全部"產品資料 /api/user/products/all

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let raw = "";

let requestOptions = {
  method: 'GET',
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/products/all", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[GET]取得"單一"產品資料 /api/user/product/P00002

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "找不到這個商品編號" }

#### javascript example

let raw = "";

let requestOptions = {
  method: 'GET',
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/product/P00002", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

let raw = "";

let requestOptions = {
  method: 'GET',
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/product/P0000", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-會員相關(前台會員)

### 1.[POST]註冊 /api/user/signup

#### post data

{
    "email": "admin1@admin.com",
    "name": "admin1",
    "password": "admin1",
    "passwordCheck": "admin1"
}

#### response

200 => { status: 200, message: "註冊成功" }
400 => { status: 400, message: "key值有誤"、"資料輸入不完整"、"密碼輸入不一致"、"信箱已註冊".... }
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "email": "admin3@admin.com",
  "name": "admin3",
  "password": "admin3",
  "passwordCheck": "admin3"
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/signup", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[POST]登入 /api/user/signin

#### post data

{
    "email": "admin1@admin.com",
    "password": "admin1"
}

#### response

200 => { status: 200, message: "登入成功", token: "..." }
400 => { status: 400, message: "key值有誤" }
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "email": "admin1@admin.com",
  "password": "admin1"
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/signin", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[PUT]變更資料 /api/user/changeInfo

#### post data

{
    "name": "admin1@admin.com",
    "password": "admin1",
    "sex": "male",
    "telephone": "0910123456",
    "address": "桃園市中壢市健行路229號"
}

#### response

200 => { status: 200, message: [0,0] }
400 => { status: 400, message: "key值有誤" }
401 => { status: 401, message: "401 Unauthorized、驗證過期，請重新登入、驗證錯誤" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "name": "admin1@admin.com",
  "password": "admin1",
  "sex": "male",
  "telephone": "0910123456",
  "address": "桃園市中壢市健行路229號"
});

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/changeInfo", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 4.[POST]登出 /api/user/signout/C00004

#### post data

{}

#### response

200 => { status: 200, message: "刪除token成功" }
404 => { status: 404, message: "找不到這個token" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer 2778502a704bf4ae7b227f069bfe5c2f3561dd5a45a35791");

let raw = "";

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("http://127.0.0.1:3000/api/user/signout/C00005", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-購物車相關(前台會員)

### 1.[POST]加入購物車 /api/user/carts

#### post data

{
    "quantity": 2,
    "total": 36000,
    "product":{
        "no": "P00002",
        "finishDegree": "成品",
        "category": "phone",
        "name": "motorola edge 20 pro",
        "description": "motorola edge 30 description",
        "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000" ,
        "price": 20000,
        "sale": 18000
    }
}

#### response

200 => { status: 200, message: "新增成功" }
400 => { status: 400, message: "key值有誤"}
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "quantity": 2,
  "total": 36000,
  "product": {
    "no": "P00002",
    "finishDegree": "成品",
    "category": "phone",
    "name": "motorola edge 20 pro",
    "description": "motorola edge 30 description",
    "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000",
    "price": 20000,
    "sale": 18000
  }
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/carts", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[GET]取得購物車 /api/user/carts

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "'cart' Not Found"、404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/carts", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 3.[DELETE]刪除"全部"購物車 /api/user/carts

#### post data

{}

#### response

200 => { status: 200, message: "刪除成功" }
400 => { status: 400, message: "購物車為空值" }
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/carts", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 4.[PUT]編輯購物車 /api/user/cart/T1674124699545915

#### post data

{
  "quantity": 2,
  "total": 36000
}

#### response

200 => { status: 200, message: "變更成功、資料無變更" }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "quantity": 2,
  "total": 36000
});

let requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/cart/T1674124699545915", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 5.[DELETE]刪除購物車內的"單一"品項 /api/user/cart/T1674124699545915

#### post data

{}

#### response

200 => { status: 200, message: "刪除成功、資料已不存在" }
404 => { status: 404, message: "xxx.. Not Found"  }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'DELETE',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/cart/T1674124699545915", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

## API路由設置-訂單相關(前台會員)

### 1.[POST]送出購物車(新增訂單) /api/user/order

#### post data

{
    "email":"admin1@admin.com",
    "receiver" : "admin1",
    "receiverTel": "0910123456",
    "receiverAddress": "桃園市中壢區健行科大",
    "userMsg": "留言....",
    "allTotal": 180000,
    "payment": "付現金",
    "cart": [{
        "cartNo": "T1673958628384031",
        "quantity": 2,
        "total": 36000,
        "product":{
            "no": "P00002",
            "finishDegree": "成品",
            "category": "phone",
            "name": "motorola edge 20 pro",
            "description": "motorola edge 30 description",
            "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000",
            "price": 20000,
            "sale": 18000
        }
    },
    {
        "cartNo": "T1673960863003139",
        "quantity": 2,
        "total": 36000,
        "product":{
            "no": "P00002",
            "finishDegree": "成品",
            "category": "phone",
            "name": "motorola edge 20 pro",
            "description": "motorola edge 30 description",
            "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000",
            "price": 20000,
            "sale": 18000
        }
    }
    ]
}

#### response

200 => { status: 200, message: "..." }
400 => { status: 400, message: "key值有誤、至少要有一個購物品項、庫存量是0，不得高於庫存量、Bad Request..."}

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);
myHeaders.append("Content-Type", "application/json");

let raw = JSON.stringify({
  "email": "admin1@admin.com",
  "receiver": "admin1",
  "receiverTel": "0910123456",
  "receiverAddress": "桃園市中壢區健行科大",
  "userMsg": "留言....",
  "allTotal": 180000,
  "payment": "付現金",
  "cart": [
    {
      "cartNo": "T1673958628384031",
      "quantity": 2,
      "total": 36000,
      "product": {
        "no": "P00002",
        "finishDegree": "成品",
        "category": "phone",
        "name": "motorola edge 20 pro",
        "description": "motorola edge 30 description",
        "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000",
        "price": 20000,
        "sale": 18000
      }
    },
    {
      "cartNo": "T1673960863003139",
      "quantity": 2,
      "total": 36000,
      "product": {
        "no": "P00002",
        "finishDegree": "成品",
        "category": "phone",
        "name": "motorola edge 20 pro",
        "description": "motorola edge 30 description",
        "picture": "https://motorolatw.vtexassets.com/arquivos/ids/155679/Motorola-edge-30-pdp-render-Silence-12-bcxm87y2.png?v=637879325266470000",
        "price": 20000,
        "sale": 18000
      }
    }
  ]
});

let requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/order", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

### 2.[GET]取得個人的"全部"訂單資料 /api/user/orders/all

#### post data

{}

#### response

200 => { status: 200, message: "..." }
404 => { status: 404, message: "404 Not Found" }

#### javascript example

let myHeaders = new Headers();
myHeaders.append("Authorization", token);

let raw = "";

let requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch( APIURL +"/api/user/orders/all", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

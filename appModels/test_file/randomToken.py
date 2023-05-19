# import os
# import secrets
# import random
# # 設定Session金鑰，亂數產生
# # 方法1:
# app.secret_key = os.urandom(8).hex()
# # print(app.secret_key)
# # 方法2:
# secrets_num = secrets.token_urlsafe(16)
# # print(secrets_num)
# # 方法3:
# seed = "!#$%()*+,-./:;=?@[]^_`{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
# random_num = ''.join(random.choices(seed, k=16))
# # print(random_num)
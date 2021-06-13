try:
    #优先使用httpx，在httpx无法使用的环境下使用requests
    import httpx
    http = httpx
except ImportError:
    import requests
    http = requests


#这里实际上应该加个"-> dict"但是考虑到请求可能失败的关系，所以直接不声明返回变量
def get(url:str, **headers:dict):
    try:
        req = http.get(url, headers=headers)
        return req.json()
    except:
        print("请求失败，网络错误！")
        return ""

def post(url:str, data:dict, **headers:dict):
    try:
        req = http.post(url, data=data, headers=headers)
        return req.json()
    except:
        print("请求失败，网络错误！")
        return ""

def post_json(url:str, json, **headers:dict):
    try:
        req = http.post(url, json=json, headers=headers)
        return req.json()
    except:
        print("请求失败，网络错误！")
        return ""
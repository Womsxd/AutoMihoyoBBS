import requests

#这里实际上应该加个"-> dict"但是考虑到请求可能失败的关系，所以直接不声明返回变量
def get(url:str, **headers:dict):
    try:
        req = requests.get(url, headers=headers)
        return req.json()
    except:
        print("请求失败，网络错误！")
        return ""

def post(url:str, data:dict, **headers:dict):
    try:
        req = requests.post(url, data=data, headers=headers)
        return req.json()
    except:
        print("请求失败，网络错误！")
        return ""

def post_json(url:str, json, **headers:dict):
    try:
        req = requests.post(url, json=json, headers=headers)
        return req.json()
    except:
        print("请求失败，网络错误！")
        return ""
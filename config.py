import os
import json
from loghelper import log

# 是否启用config
enable_Config = True
# 这里的内容会自动获取
mihoyobbs_Login_ticket = ""
mihoyobbs_Stuid = ""
mihoyobbs_Stoken = ""
# 这里是米游社的cookie
mihoyobbs_Cookies = ""
# 这个dist里面的内容和米游社有关
mihoyobbs = {
    # 全局开关，关闭之后下面的都不执行
    "bbs_Global": True,
    # 讨论区签到
    "bbs_Signin": True,
    # 多个讨论区签到
    "bbs_Signin_multi": True,
    # 指定签到讨论区
    # 1是崩坏3 2是原神 3是崩坏2 4是未定事件簿 5是大别墅
    # 可以通过设置讨论区的id位置来设置主讨论区，[5,1]就是大别墅为主社区
    # 看帖子 点赞 分享帖子都是使用主社区获取到的列表
    "bbs_Signin_multi_list": [2, 5],
    # 浏览3个帖子
    "bbs_Read_posts": True,
    # 完成5次点赞
    "bbs_Like_posts": True,
    # 完成后取消点赞
    "bbs_Unlike": True,
    # 分享帖子
    "bbs_Share": True,
}
# 原神自动签到
genshin_Auto_sign = True
# 崩坏3自动签到
honkai3rd_Auto_sign = True

path = os.path.dirname(os.path.realpath(__file__)) + "/config"
config_Path = f"{path}/config.json"

useFile = os.path.isfile(config_Path);

def load_config():
    if useFile:
        load_config_from_file()
    else:
        load_config_from_env()
    log.info("Config加载完毕")

def load_config_from_file():
    with open(config_Path, "r") as f:
        data = json.load(f)
        global enable_Config
        global mihoyobbs_Login_ticket
        global mihoyobbs_Stuid
        global mihoyobbs_Stoken
        global mihoyobbs_Cookies
        global mihoyobbs
        global genshin_Auto_sign
        global honkai3rd_Auto_sign
        enable_Config = data["enable_Config"]
        mihoyobbs_Login_ticket = data["mihoyobbs_Login_ticket"]
        mihoyobbs_Stuid = data["mihoyobbs_Stuid"]
        mihoyobbs_Stoken = data["mihoyobbs_Stoken"]
        mihoyobbs_Cookies = data["mihoyobbs_Cookies"]
        mihoyobbs["bbs_Global"] = data["mihoyobbs"]["bbs_Global"]
        mihoyobbs["bbs_Signin"] = data["mihoyobbs"]["bbs_Signin"]
        mihoyobbs["bbs_Signin_multi"] = data["mihoyobbs"]["bbs_Signin_multi"]
        mihoyobbs["bbs_Signin_multi_list"] = data["mihoyobbs"]["bbs_Signin_multi_list"]
        mihoyobbs["bbs_Read_posts"] = data["mihoyobbs"]["bbs_Read_posts"]
        mihoyobbs["bbs_Like_posts"] = data["mihoyobbs"]["bbs_Like_posts"]
        mihoyobbs["bbs_Unlike"] = data["mihoyobbs"]["bbs_Unlike"]
        mihoyobbs["bbs_Share"] = data["mihoyobbs"]["bbs_Share"]
        genshin_Auto_sign = data["genshin_Auto_sign"]
        honkai3rd_Auto_sign = data["honkai3rd_Auto_sign"]
        f.close()
       
def load_config_from_env():
    global enable_Config
    global mihoyobbs_Login_ticket
    global mihoyobbs_Stuid
    global mihoyobbs_Stoken
    global mihoyobbs_Cookies
    global mihoyobbs
    global genshin_Auto_sign
    global honkai3rd_Auto_sign
    mihoyobbs_Login_ticket = os.getenv("MIHOYOBBS_LOGIN_TICKET")
    mihoyobbs_Stuid = os.getenv("MIHOYOBBS_STUID")
    mihoyobbs_Stoken = os.getenv("MIHOYOBBS_STOKEN")
    mihoyobbs_Cookies = os.getenv('MIHOYOBBS_COOKIES');
    mihoyobbs["bbs_Global"] = os.getenv('MIHOYOBBS_BBS_GLOBAL')
    mihoyobbs["bbs_Signin"] = os.getenv('MIHOYOBBS_BBS_SIGNIN')
    mihoyobbs["bbs_Signin_multi"] = os.getenv('MIHOYOBBS_BBS_SIGNIN_MULTI')
    mihoyobbs["bbs_Signin_multi_list"] = os.getenv('MIHOYOBBS_BBS_SIGNIN_MULTI_LIST')
    mihoyobbs["bbs_Read_posts"] = os.getenv('MIHOYOBBS_BBS_READ_POSTS')
    mihoyobbs["bbs_Like_posts"] = os.getenv('MIHOYOBBS_BBS_LIKE_POSTS')
    mihoyobbs["bbs_Unlike"] = os.getenv('MIHOYO_BBS_UNLIKE')
    mihoyobbs["bbs_Share"] = os.getenv('MIHOYO_BBS_SHARE')
    genshin_Auto_sign = os.getenv("GENSHIN_AUTO_SIGN")
    honkai3rd_Auto_sign = os.getenv("HONKAI3RD_AUTO_SIGN")

def save_config():
    if useFile:
        save_config_to_file()
    else:
        save_config_to_env()
    log.info("Config保存完毕")

def save_config_to_file():
    with open(config_Path, "r+") as f:
        data = json.load(f)
        data["mihoyobbs_Login_ticket"] = mihoyobbs_Login_ticket
        data["mihoyobbs_Stuid"] = mihoyobbs_Stuid
        data["mihoyobbs_Stoken"] = mihoyobbs_Stoken
        f.seek(0)
        f.truncate()
        temp_Text = json.dumps(data, sort_keys=False, indent=4, separators=(', ', ': '))
        f.write(temp_Text)
        f.flush()
        f.close()

def save_config_to_env():
    os.environ['MIHOYOBBS_LOGIN_TICKET'] = mihoyobbs_Login_ticket
    os.environ['MIHOYOBBS_STUID'] = mihoyobbs_Stuid
    os.environ['MIHOYOBBS_STOKEN'] = mihoyobbs_Stoken


def clear_cookies():
    if useFile:
        clear_cookies_in_file()
    else:
        clear_cookies_in_env()
    log.info("Cookie删除完毕")
    
def clear_cookies_in_file():
    with open(config_Path, "r+") as f:
        data = json.load(f)
        data["enable_Config"] = False
        data["mihoyobbs_Login_ticket"] = ""
        data["mihoyobbs_Stuid"] = ""
        data["mihoyobbs_Stoken"] = ""
        data["mihoyobbs_Cookies"] = ""
        f.seek(0)
        f.truncate()
        temp_Text = json.dumps(data, sort_keys=False, indent=4, separators=(', ', ': '))
        f.write(temp_Text)
        f.flush()
        f.close()

def clear_cookies_in_env():
    os.environ.pop('MIHOYOBBS_LOGIN_TICKET', None)
    os.environ.pop('MIHOYOBBS_STUID', None); 
    os.environ.pop('MIHOYOBBS_STOKEN', None);
    os.environ.pop('MIHOYOBBS_COOKIES', None)
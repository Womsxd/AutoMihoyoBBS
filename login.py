import config
import request
import setting
import sys
from loghelper import log
from error import CookieError


def login(cookies = config.mihoyobbs_Cookies):
    if cookies == '':
        log.error("请填入Cookies!")
        # config.clear_cookies()
        raise CookieError('No cookie')
    # 判断Cookie里面是否有login_ticket 没有的话直接退了
    if "login_ticket" in cookies:
        temp_Cookies = cookies.split(";")
        for i in temp_Cookies:
            if i.split("=")[0] == " login_ticket":
                config.mihoyobbs_Login_ticket = i.split("=")[1]
                break
        # 这里获取Stuid，但是实际是可以直接拿cookie里面的Uid
        data = request.get(url=setting.bbs_Cookieurl.format(config.mihoyobbs_Login_ticket))
        if "成功" in data["data"]["msg"]:
            config.mihoyobbs_Stuid = str(data["data"]["cookie_info"]["account_id"])
            data = request.get(url=setting.bbs_Cookieurl2.format(config.mihoyobbs_Login_ticket, config.mihoyobbs_Stuid))
            config.mihoyobbs_Stoken = data["data"]["list"][0]["token"]
            log.info("登录成功！")
            log.info("正在保存Config！")
            config.save_config()
        else:
            log.error("cookie已失效,请重新登录米游社抓取cookie")
            config.clear_cookies()
            raise CookieError('Cookie expires')
    else:
        log.error("cookie中没有'login_ticket'字段,请重新登录米游社，重新抓取cookie!")
        config.clear_cookies()
        raise CookieError('Cookie lost login_ticket')

if __name__ == '__main__':
    login(sys.argv[1])
    print("stuid:        ", config.mihoyobbs_Stuid)
    print("stoken:       ", config.mihoyobbs_Stoken)
    print("login_ticket: ", config.mihoyobbs_Login_ticket)

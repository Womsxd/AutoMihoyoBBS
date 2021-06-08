import time
import httpx
import tools
import config
import random
import setting

class honkai3rd:
    def __init__(self) -> None:
        self.headers = {
                'Accept': 'application/json, text/plain, */*',
                'DS': tools.Get_ds(web=True, web_old=True),
                'Origin': 'https://webstatic.mihoyo.com',
                'x-rpc-app_version': setting.mihoyobbs_Version_old,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.3.0',
                'x-rpc-client_type': setting.mihoyobbs_Client_type_web,
                'Referer': 'https://webstatic.mihoyo.com/bh3/event/euthenia/index.html?bbs_presentation_style=fullscreen&bbs_game_role_required=bh3_cn&bbs_auth_required=true&act_id=e202104072769&utm_source=bbs&utm_medium=mys&utm_campaign=icon',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'X-Requested-With': 'com.mihoyo.hyperion',
                "Cookie": config.mihoyobbs_Cookies,
                'x-rpc-device_id': tools.Get_deviceid()
            }
        self.acc_List = self.Getacc_list()

    #获取绑定的账号列表
    def Getacc_list(self) -> list:
        tools.log.info("正在获取米哈游账号绑定的崩坏3账号列表...")
        temp_List = []
        req = httpx.get(setting.honkai3rd_Account_info_url, headers=self.headers)
        data = req.json()
        if data["retcode"] != 0:
            tools.log.warn("获取账号列表失败！")
            exit()
        for i in data["data"]["list"]:
            temp_List.append([i["nickname"], i["game_uid"], i["region"]])
        tools.log.info(f"已获取到{len(temp_List)}个崩坏3账号信息")
        return temp_List

    #获取今天已经签到了的dict
    def Get_today_item(self,raw_data:list) -> dict:
        #用range进行循环，当staus等于0的时候上一个就是今天签到的dict
        for i in range(len(raw_data)):
            if raw_data[i]["status"] == 0:
                return raw_data[i-1]
            if raw_data[i]["status"] == 1:
                return raw_data[i]
            if i == int(len(raw_data) - 1) and raw_data[i]["status"] != 0:
                return raw_data[i]

    #判断签到
    def Is_sing(self, region:str, uid:str, nickname:str):
        req = httpx.get(setting.honkai3rd_Is_singurl.format(setting.honkai3rd_Act_id, region, uid), headers=self.headers)
        data = req.json()
        if data["retcode"] != 0:
            tools.log.warn("获取账号签到信息失败！")
            print (req.text)
            exit()
        today_Item = self.Get_today_item(data["data"]["sign"]["list"])
        if today_Item["status"] == 1:
            return True
        else:
            tools.log.info(f"舰长{nickname}今天已经签到过了~\r\n今天获得的奖励是{tools.Get_item(today_Item)}")
            return False

    #签到
    def Sing_acc(self):
        if len(self.acc_List) != 0:
            for i in self.acc_List:
                tools.log.info(f"正在为舰长{i[0]}进行签到...")
                time.sleep(random.randint(2, 6))
                is_data = self.Is_sing(region = i[2], uid = i[1], nickname = i[0])
                if is_data == True:
                    time.sleep(random.randint(2, 6))
                    req = httpx.post(url=setting.honkai3rd_SingUrl, headers=self.headers,
                        json={'act_id': setting.honkai3rd_Act_id, 'region': i[2], 'uid': i[1]})
                    data = req.json()
                    if data["retcode"] == 0:
                        today_Item = self.Get_today_item(data["data"]["list"])
                        tools.log.info(f"舰长{i[0]}签到成功~\r\n今天获得的奖励是{tools.Get_item(today_Item)}")
                    elif data["retcode"] == -5003:
                        #崩坏3应为奖励列表和签到信息在一起了，加上上面已经可以进行了一次判断，所以这里旧不重复再次执行判断来获取内容了
                        tools.log.info(f"舰长{i[0]}今天已经签到过了~")
                    else:
                        tools.log.warn("账号签到失败！")
                        print (req.text)
        else:
            tools.log.warn("账号没有绑定任何崩坏3账号！")
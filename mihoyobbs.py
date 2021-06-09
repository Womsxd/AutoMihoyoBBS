import time
import requests
import tools
import config
import random
import setting

Today_getcoins = 0
Today_have_getcoins = 0 #这个变量以后可能会用上，先留着了
Have_coins = 0

class mihoyobbs:
    def __init__(self):
        self.headers = {
            "DS": tools.Get_ds(web=False, web_old=False),
            "cookie": f"stuid={config.mihoyobbs_Stuid};stoken={config.mihoyobbs_Stoken}",
            "x-rpc-client_type": setting.mihoyobbs_Client_type,
            "x-rpc-app_version": setting.mihoyobbs_Version,
            "x-rpc-sys_version": "6.0.1",
            "x-rpc-channel": "mihoyo",
            "x-rpc-device_id": tools.Get_deviceid(),
            "x-rpc-device_name": tools.Random_text(random.randint(1, 10)),
            "x-rpc-device_model": "Mi 10",
            "Referer": "https://app.mihoyo.com",
            "Host": "bbs-api.mihoyo.com",
            "User-Agent": "okhttp/4.8.0"
        }
        self.Task_do = {
            "bbs_Sign": False,
            "bbs_Read_posts": False,
            "bbs_Like_posts": False,
            "bbs_Share": False
        }
        self.Get_taskslist()
        #如果这三个任务都做了就没必要获取帖子了
        if self.Task_do["bbs_Read_posts"] == True and self.Task_do["bbs_Like_posts"] == True and self.Task_do["bbs_Share"] == True:
            pass
        else:
            self.postsList = self.Getlist()

    #获取任务列表，用来判断做了哪些任务
    def Get_taskslist(self):
        global Today_getcoins
        global Today_have_getcoins
        global Have_coins
        tools.log.info("正在获取任务列表")
        req = requests.get(url=setting.bbs_Taskslist, headers=self.headers)
        data = req.json()
        if "err" in data["message"]:
            tools.log.info("获取任务列表失败，你的cookie可能已过期，请重新设置cookie。")
            config.Clear_cookies()
            exit()
        else:
            Today_getcoins = data["data"]["can_get_points"]
            Today_have_getcoins = data["data"]["already_received_points"]
            Have_coins = data["data"]["total_points"]
            #如果当日可获取米游币数量为0直接判断全部任务都完成了
            if Today_getcoins == 0:
                self.Task_do["bbs_Sign"] = True
                self.Task_do["bbs_Read_posts"] = True
                self.Task_do["bbs_Like_posts"] = True
                self.Task_do["bbs_Share"] = True
            else:
                #如果第0个大于或等于62则直接判定任务没做
                if data["data"]["states"][0]["mission_id"] >= 62:
                    tools.log.info(f"新的一天，今天可以获得{Today_getcoins}个米游币")
                    pass
                else:
                    tools.log.info(f"似乎还有任务没完成，今天还能获得{Today_getcoins}")
                    for i in data["data"]["states"]:
                        #58是讨论区签到
                        if i["mission_id"] == 58:
                            if i["is_get_award"] == True:
                                self.Task_do["bbs_Sign"] = True
                        #59是看帖子
                        elif i["mission_id"] == 59:
                            if i["is_get_award"] == True:
                                self.Task_do["bbs_Read_posts"] = True
                        #60是给帖子点赞
                        elif i["mission_id"] == 60:
                            if i["is_get_award"] == True:
                                self.Task_do["bbs_Like_posts"] = True
                        #61是分享帖子
                        elif i["mission_id"] == 61:
                            if i["is_get_award"] == True:
                                self.Task_do["bbs_Share"] = True
                                #分享帖子，是最后一个任务，到这里了下面都是一次性任务，直接跳出循环
                                break

    #获取要帖子列表
    def Getlist(self) -> list:
        temp_List = []
        tools.log.info("正在获取帖子列表......")
        for i in setting.mihoyobbs_List_Use:
            req = requests.get(url=setting.bbs_Listurl.format(i["forumId"]), headers=self.headers)
            data = req.json()
            for n in range(6):
                temp_List.append([data["data"]["list"][n]["post"]["post_id"], data["data"]["list"][n]["post"]["subject"]])
            tools.log.info("已获取{}个帖子".format(len(temp_List)))
            time.sleep(random.randint(2, 6))
        return temp_List

    #进行签到操作
    def Singin(self):
        #签到这里暂时不设置判断，防止要签到的其他社区没有签到成功
        #if self.Task_do["bbs_Sign"] == False:
        tools.log.info("正在签到......")
        for i in setting.mihoyobbs_List_Use:
            req = requests.post(url=setting.bbs_Signurl.format(i["id"]), data="" ,headers=self.headers)
            data = req.json()
            if "err" not in data["message"]:
                tools.log.info(str(i["name"]+ data["message"]))
                time.sleep(random.randint(2, 6))
            else:
                tools.log.info("签到失败，你的cookie可能已过期，请重新设置cookie。")
                config.Clear_cookies()
                exit()

    #看帖子
    def Readposts(self):
        if self.Task_do["bbs_Read_posts"] == False:
            tools.log.info("正在看帖......")
            for i in range(3):
                req = requests.get(url=setting.bbs_Detailurl.format(self.postsList[i][0]), headers=self.headers)
                data = req.json()
                if data["message"] == "OK":
                    tools.log.info("看帖：{} 成功".format(self.postsList[i][1]))
                time.sleep(random.randint(2, 6))
        else:
            tools.log.info("看帖任务已经完成过了~")

    #点赞
    def Likeposts(self):
        if self.Task_do["bbs_Like_posts"] == False:
            tools.log.info("正在点赞......")
            for i in range(5):
                req = requests.post(url=setting.bbs_Likeurl, headers=self.headers,
                        json={"post_id": self.postsList[i][0], "is_cancel": False})
                data = req.json()
                if data["message"] == "OK":
                    tools.log.info("点赞：{} 成功".format(self.postsList[i][1]))
                #判断取消点赞是否打开
                if config.mihoyobbs["bbs_Unlike"] == True:
                    time.sleep(random.randint(2, 6))
                    req = requests.post(url=setting.bbs_Likeurl, headers=self.headers,
                        json={"post_id": self.postsList[i][0], "is_cancel": True})
                    data = req.json()
                    if data["message"] == "OK":
                        tools.log.info("取消点赞：{} 成功".format(self.postsList[i][1]))
                time.sleep(random.randint(2, 6))
        else:
            tools.log.info("点赞任务已经完成过了~")

    #分享操作
    def Share(self):
        if self.Task_do["bbs_Share"] == False:
            tools.log.info("正在分享......")
            req = requests.get(url=setting.bbs_Shareurl.format(self.postsList[0][0]), headers=self.headers)
            data = req.json()
            if data["message"] == "OK":
                tools.log.info("分享：{} 成功".format(self.postsList[0][1]))
            time.sleep(random.randint(2, 6))
        else:
            tools.log.info("分享任务已经完成过了~")
import os
import sys
import main
import time
import push
import config
import random
import setting
from loghelper import log
from error import CookieError


# 搜索配置文件
def fund_config() -> list:
    file_name = []
    for files in os.listdir(config.path):
        if os.path.splitext(files)[1] == '.json':
            file_name.append(files)
    return file_name


def main_multi(autorun: bool):
    log.info("AutoMihoyoBBS Multi User mode")
    log.info("正在搜索配置文件！")
    config_list = fund_config()
    detail_msg = ""
    if len(config_list) == 0:
        log.warning("未检测到配置文件，请确认config文件夹存在.json后缀名的配置文件！")
        exit(1)
    if autorun:
        log.info(f"已搜索到{len(config_list)}个配置文件，正在开始执行！")
    else:
        log.info(f"已搜索到{len(config_list)}个配置文件，请确认是否无多余文件！\r\n{config_list}")
        try:
            input("请输入回车继续，需要重新搜索配置文件请Ctrl+C退出脚本")
        except:
            exit(0)
    results = {"ok": [], "close": [], "error": []}
    for i in iter(config_list):
        log.info(f"正在执行{i}")
        setting.mihoyobbs_List_Use = []
        config.config_Path = f"{config.path}/{i}"
        try:
            run_code, run_message = main.main()
        except CookieError:
            results["error"].append(i)
        else:
            if run_code == 0:
                results["ok"].append(i)
                detail_msg += "\r\n"+run_message
            else:
                results["close"].append(i)
        log.info(f"{i}执行完毕")
        time.sleep(random.randint(3, 10))
    print("")
    push_message = f'脚本执行完毕\r\n共执行{len(config_list)}个配置文件\r\n成功{len(results["ok"])}个,没执行{len(results["close"])}个,失败{len(results["error"])}个'\
                   f'\r\n没执行的配置文件: {results["close"]}\r\n执行失败的配置文件: {results["error"]}'
    log.info(push_message)
    push.push(0, push_message+"\r\n"+detail_msg)


if __name__ == "__main__":
    if (len(sys.argv) >= 2 and sys.argv[1] == "autorun") or os.getenv("AutoMihoyoBBS_autorun") == "1":
        autorun = True
    else:
        autorun = False
    main_multi(autorun)
    exit(0)
pass

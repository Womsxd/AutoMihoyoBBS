import main

def main_handler(event:dict, context:dict):
    main.main()
    print("云函数测试支持！")
    return 0
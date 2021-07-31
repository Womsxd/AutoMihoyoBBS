# 米游社自动签到
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FWomsxd%2FAutoMihoyoBBS.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FWomsxd%2FAutoMihoyoBBS?ref=badge_shield)


基于Python3的米游社自动签到项目

本项目米游币部分参考[XiaoMiku01/miyoubiAuto](https://github.com/XiaoMiku01/miyoubiAuto)进行编写

* 此项目的用途

  这是一个米游社的自动签到项目，包含了米游币和原神以及崩坏3

## 如何使用程序

* **部署方法**

  1. 下载[本项目](https://github.com/Womsxd/AutoMihoyoBBS/archive/refs/heads/master.zip)

  2. 下载[Python3](https://www.python.org/downloads/)

  3. 解压本项目压缩包,在解压目录中**Shift+右键** 打开你的命令提示符cmd或powershell

  4. [requirements.txt](https://raw.githubusercontent.com/Womsxd/AutoMihoyoBBS/master/requirements.txt) 是所需第三方模块，执行 `pip install -r requirements.txt` 安装模块

  5. 打开目录中的**config文件夹**复制`config.json.example`并改名为`config.json`，如果需要使用多用户的功能的话请改名成`xxx.json`

  6. 请使用vscode/notepad++等文本编辑器打开上一步复制好的配置文件

  7. **使用[获取Cookie](#获取米游社Cookie)里面的方法来获取米游社Cookie**

  8. 将复制的Cookie粘贴到`config.json`的`"mihoyobbs_Cookies":" "`中

        例子

        > ```json
        > "mihoyobbs_Cookies": "你复制的cookie"
        > ```

  9. 在命令提示符(cmd)/powershell，输入`python main.py`来进行执行
  
  10. 多用户的请使用`python main_multi.py`，多用户在需要自动执行的情况下请使用`python main_multi.py autorun`

## 获取米游社Cookie

1. 打开你的浏览器,进入**无痕/隐身模式**

2. 打开`http://bbs.mihoyo.com/ys/`并进行登入操作

3. 按下键盘上的`F12`或右键检查,打开开发者工具,点击Console

4. 输入

   ```javascript
   var cookie=document.cookie;var ask=confirm('Cookie:'+cookie+'\n\nDo you want to copy the cookie to the clipboard?');if(ask==true){copy(cookie);msg=cookie}else{msg='Cancel'}
   ```

   回车执行，并在确认无误后点击确定。

5. **此时Cookie已经复制到你的粘贴板上了**

## License

[MIT License](https://github.com/Womsxd/AutoMihoyoBBS/blob/master/LICENSE)


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FWomsxd%2FAutoMihoyoBBS.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FWomsxd%2FAutoMihoyoBBS?ref=badge_large)
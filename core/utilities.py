import hashlib
from datetime import datetime

class c:
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Orange = '\033[33m'
    Blue = '\033[34m'
    Purple = '\033[35m'
    Reset = '\033[0m'
    Cyan = '\033[36m'
    LightGrey = '\033[37m'
    DarkGrey = '\033[90m'
    LightRed = '\033[91m'
    LightGreen = '\033[92m'
    Yellow = '\033[93m'
    LightBlue = '\033[94m'
    Pink = '\033[95m'
    LightCyan = '\033[96m'

class bc:
    Black = '\033[40m'
    Red = '\033[41m'
    Green = '\033[42m'
    Yellow = '\033[43m'
    Blue = '\033[44m'
    Purple = '\033[45m'
    Reset = '\033[0m'
    Cyan = '\033[46m'
    White = '\033[47m'
    DarkGrey = '\033[100m'
    LightRed = '\033[101m'
    LightGreen = '\033[102m'
    Yellow = '\033[103m'
    LightBlue = '\033[104m'
    Pink = '\033[105m'
    LightCyan = '\033[106m'
    BrightWhite = '\033[107m'

class msg:
    def newRequest():
        return f"\n========================={bc.Black}[ New request caught - {datetime.now()} ]{bc.Reset}=========================\n\r"

    def requestInfo(method,remote_addr,path):
        return f"[{c.Orange}{method}{c.Reset}][{c.Orange}{remote_addr}{c.Reset}] -> {c.Blue}{path}{c.Reset}\n\r"

    def requestHeaders(headers):
        total = len(headers)
        output = ""
        output = f"{bc.Black}[      Headers      ]{c.Reset}\n\r"
        for i, (name, value) in enumerate(headers.items(), 1):
            prefix = "└──" if i == total else "├──"
            output += f" {prefix}{bc.Black}[ {c.Green}{name} :{c.Reset} {value} \n\r"
        return output

    def requestCookies(cookies):
        output = ""
        if cookies:
            output += f"\n{bc.Black}[      Cookies      ]{c.Reset}\n\r"
            output += f" └──{bc.Black}[ {c.Green}Cookies :{c.Reset} {dict(cookies)}\n\r"
        return output

    def requestPostData(data):
        output = ""
        if data:
            output += f"\n{bc.Black}[      Post Data      ]{c.Reset}\n\r"
            output += f" └──{bc.Black}[ {c.Green}Parameters :{c.Reset}{data}\n\r"
        return output

    def requestFiles(files):
        total = len(files)
        output = ""
        if total > 0:
            output+=f"\n{bc.Black}[      Files      ]{c.Reset}\n\r"

        for key, f in files.items():
            output += f" ├──{bc.Black}[ {c.Green}File field :{c.Reset} [{c.Orange}{key}{c.Reset}]: filename={c.Orange}{f.filename}{c.Reset}, content-type={c.Orange}{f.content_type}{c.Reset}\n\r"
            content = f.read()
            output +=f" ├──[{c.Green} Content :{c.Reset} {len(content)} bytes\n\r"
            filename = hashlib.md5(f.filename.encode()).hexdigest() + ".bin"
            open("files/"+filename,'wb').write(content)
            output += f" └──[{c.Green} File saved as files/{filename}{c.Reset}\n\r"
        return output

    def error(msg):
        print(f"\n[{c.Red}*{c.Reset}] {datetime.now()} - {c.Red}{msg}{c.Reset}\n\r")

    def info(msg):
        print(f"[{c.Blue}i{c.Reset}] {datetime.now()} - {c.Blue}{msg}{c.Reset}\r")

    def main_help_menu():
        print('''
            --== options ==--
    exit                  ->  close this app
    list                  ->  show all custom routes
    add                   ->  add new flask route
       ├──  --path        ->  specify a name for the new route
       └──  --header      ->  set a custom header for every http response, you can add multiple headers
                              (--header ContentType:text/html --header test2:test2)
                              if you need add (space) on header value just add ++ 
                              (--header X-Custom-Header:This++is++a++test)
    load                  ->  load all registered custom routes from custom_routes.ini file
    save                  ->  save custom routes on custom_routes.ini file
    del --id <path id>    ->  delete specific path
    run                   ->  start http server
       ├──  --port        ->  specify http port (default 8080)
       ├──  --interface   ->  specify listen interface (default 0.0.0.0)
       ├──  --serveo      ->  expose local flask app to the public internet via ssh port forward via serveo.net
       ├──  --ssl         ->  enable ssl context
       ├──  --key         ->  set private key (.key/.pem)
       └──  --pub         ->  set public key (.crt/.pem)
    help                  ->  show this menu
            ''',end='\n\r')

    def banner():
        print(f"""
██████╗ ██╗   ██╗ ██████╗ █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
██████╔╝ ╚████╔╝ ██║     ███████║   ██║   ██║     ███████║█████╗  ██████╔╝
██╔═══╝   ╚██╔╝  ██║     ██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
██║        ██║   ╚██████╗██║  ██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║
╚═╝        ╚═╝    ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ (v1.0)
Coded by:{c.Red} sp34rh34d{c.Reset}
x: {c.Red}@spearh34d{c.Reset}""")

#!/usr/bin/env python3
import readline, argparse, sys, configparser, subprocess, uuid
from core.utilities import msg, c
from core.catcher import *
from tabulate import tabulate
from pathlib import Path

parser = argparse.ArgumentParser(add_help=False)
args = parser.parse_args()

custom_routes = {}

main_commands = ['exit','help','run','add','del','load','save','list']
def completer(text, state):
    options = [cmd for cmd in main_commands if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

msg.banner()

def custom_routes_list():
    if custom_routes.keys():
        data =[]
        for route in custom_routes:
            data.append([route,custom_routes[route]["path"],custom_routes[route]["file"],custom_routes[route]["headers"]])
        route_table = tabulate(data,headers=["Route id","Path","File","Headers"])
        print(route_table)
    else:
        msg.info("no custom route yet")

def save_custom_routes():
    if not custom_routes.keys():
        msg.info("no custom route yet!")

    config = configparser.ConfigParser()
    for section, values in custom_routes.items():
        config[section]=values

    with open('custom_routes.ini','w') as configfile:
        config.write(configfile)
    msg.info("custom_routes.ini created successfully")

def load_custom_routes():
    file = Path('custom_routes.ini')
    if not file.is_file():
        msg.error('file custom_routes.ini not found!')
        return

    config = configparser.ConfigParser()
    config.read('custom_routes.ini')

    for r in config.sections():
        custom_routes[r] = dict(config[r])

    msg.info("custom_routes.ini loaded successfully")

while True:
    try: 
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)
        main_option= input(f"{c.Red}py{c.Reset}👾{c.Red}Catcher{c.Orange} {c.Green}# {c.Reset}").strip().split()
        parser = argparse.ArgumentParser(exit_on_error=False,add_help=False)
        
        try:
            parser.add_argument('option', help="action you wanna do, use help to show options")
            parser.add_argument('--port',help="Set listening port for http requests", nargs='?',default=8080)
            parser.add_argument('--interface',help="Set listening interface for http requests", nargs='?',default='0.0.0.0')
            parser.add_argument('--ssl',help="Enable ssl context", action='store_true')
            parser.add_argument('--key',help="Set private key (.key/.pem)", nargs='?',default=None)
            parser.add_argument('--pub',help="Set public key (.crt/.pem)", nargs='?',default=None)
            parser.add_argument('--path',help="Add new flask route", nargs='?',default=None)
            parser.add_argument('--id',help="custom path id", nargs='?',default=None)
            parser.add_argument('--header',action='append',help="Set custom headers for http response", nargs='?',default=None)
            parser.add_argument('--serveo',help="Enable serveo.net service for port forward", action='store_true')
            args_main=parser.parse_args(main_option)
        except :
            args_main.option=None
            pass

        if args_main.option=='exit':
            msg.info(f"quitting...")
            break

        elif args_main.option=='run':
            rcatcher = request_catcher(args_main.interface,int(args_main.port),args_main.ssl,args_main.key,args_main.pub,custom_routes,args_main.serveo)
            rcatcher.run()

        elif args_main.option=='list':
            custom_routes_list()

        elif args_main.option=='save':
            save_custom_routes()

        elif args_main.option=='add':
            if not args_main.path:
                msg.error("You need to set a route name, use --path my_new_rute")
                continue
            subprocess.call(["nano", "routes/"+args_main.path+".bin"])
            route_id = str(uuid.uuid4())

            headers_list = args_main.header or []
            headers_dict = dict(h.split(":", 1) for h in headers_list )

            custom_routes[route_id]={"path":args_main.path,"file":f"routes/{args_main.path}.bin","headers":headers_dict}

        elif args_main.option=='del':
            if not args_main.id:
                msg.error("id is required!, use --id <uuid>")
                continue
            if not custom_routes.get(args_main.id):
                msg.info("custom route id not found!")
                continue
            custom_routes.pop(args_main.id,None)

        elif args_main.option=='load':
            load_custom_routes()

        elif args_main.option=='help':
            msg.main_help_menu()

    except KeyboardInterrupt:
       msg.error("Stopped by user!")
       sys.exit()
    except:
       pass

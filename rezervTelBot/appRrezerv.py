#import config
#import telebot
#from aiohttp import web
#import ssl
from subprocess import check_output
from flask import *
import requests
import pprint
#import telegram
#import json
from json import *
import sqlite3 as sq3
#from telegram.ext import *
#from telebot import TeleBot
#from keyboa import keyboa_maker
from io import BytesIO
from PIL import Image
import shutil
import random

WEBHOOK_LISTEN = "0.0.0.0"
WEBHOOK_PORT = 8443

WEBHOOK_SSL_CERT = "/etc/letsencrypt/live/xn--i1ahcl5aza.xyz/fullchain.pem"
WEBHOOK_SSL_PRIV = "/etc/letsencrypt/live/xn--i1ahcl5aza.xyz/privkey.pem"

API_TOKEN = "bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA"

API_TELEGRAMM = "https://api.telegram.org/bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA"

class cloudEditor():
    
    #def __init__(self, BaseData):
    #    self.db = BaseData
    #    self.db.create_table()

    def createCloud(self, data):
        idUser = data['message']['chat']['id']

        try: 
            f = open(f'users/{idUser}/user.txt', "w")
            f.write(str(data['message']['from']))
            f.close()
            output = check_output(f"cd users/{idUser}", shell = True)
            requests.get(API_TELEGRAMM+'/sendMessage'+ f'?chat_id={idUser}'+'&'+ f'text=Облако%20не%20нуждается%20в%20создании')
        except:
            output = check_output(f"mkdir -m 777 -p users/{idUser}", shell = True)
            f = open(f'users/{idUser}/user.txt', "w")
            f.write(data['message']['from'])
            f.close()
            requests.get(API_TELEGRAMM+'/sendMessage'+ f'?chat_id={idUser}'+'&'+ f'text=Облако%20было%20создано')

    def downloadFile(self, data: dict, key: str):
        file_id = data['message'][key]
        try:
            file_id = file_id[-1]["file_id"] #при азгрузке фото предоставялется 3 file_id
        except:
            file_id = file_id["file_id"]
        

        self.idUser = data['message']['chat']['id']

        out = open(f"users/{self.idUser}/{key}.txt", "a")
        out.write(f"{file_id}\n")
        out.close
        requests.get(API_TELEGRAMM+'/sendMessage'+ f'?chat_id={self.idUser}'+'&'+ f'text=Файл%20был%20загружен%20в%20{key}')


    def sendAllFile(self, data, arg = "error"):
        User_Id = data['message']['chat']['id']
        output = check_output(f"ls users/{User_Id}", shell = True).decode('utf-8').split()
        #print(output)
        if arg == "all":
            dick = {"document":"sendDocument", "photo": "sendPhoto", "video" : "sendVideo"}
            for fileName in output:
                if fileName == "user.txt":
                    continue
                f = open(f"users/{User_Id}/{fileName}", "r")
                Allfile = f.read().split()
                print(Allfile)
                for i in range(len(Allfile)):
                    requests.get(API_TELEGRAMM+f'/{dick[fileName[0:-4]]}'+ f'?chat_id={User_Id}'+'&'+ f'{fileName[0:-4]}={Allfile[i]}')
                f.close()
                # добавить ls
        elif arg == "ls":
            for fileName in output:
                f = open(f"users/{User_Id}/{fileName}", "r")
                Allfile = f.read().split()
                print(Allfile)
                requests.get(API_TELEGRAMM+f'/sendMessage'+ f'?chat_id={User_Id}'+'&'+ f'text={fileName[0:-4]} имеется {len(Allfile)}')
                f.close() 
        elif args == "error":
            pass
        else :
            requests.get(API_TELEGRAMM+f'/sendMessage'+ f'?chat_id={User_Id}'+'&'+ f'text=функционал не доделан')

#-Функция запроса
def ReqGet(method = None, argsDict = {}): 
    return requests.get(f'{API_TELEGRAMM}/{method}', params = argsDict)
        


app = Flask(__name__)

@app.route(f'/{API_TOKEN}/', methods=['POST'])
def Update():
    #global ReqGet
    global cloud


    def textMessageAnalyzer(User_id: int, data):
        text = data['message']['text']
        if text[0] == "/":
            with open('configRequests.json', "r") as f:
                keyboars = load(f)
            
            print("this is comand")
            if text == "/start" :
                #вызов клавитуры
                print("вызов пошел")
                ReqGet(method="sendMessage", argsDict = {"chat_id":User_id, "text": 'Hellochild', "reply_markup" :'{%22inline_keyboard%22:%20[[{%22text%22:%20%22hello%22,%22callback_data%22:%20%22hello%20world%22},{%22text%22:%20%22/help%22,%22callback_data%22:%20%22help%22}]]}'})
                #https://api.telegram.org/bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA/sendMessage?chat_id=848986553&text=Hellochild&reply_markup={%22inline_keyboard%22:%20[[{%22text%22:%20%22/cloud%22,%22callback_data%22:%20%22cloudINIT%22},{%22text%22:%20%22/help%22,%22callback_data%22:%20%22help%22}]]}

                    
            elif text == '/help':
                keyboard = keyboars['keyboargs']['helpKeyboard']
                argsDict = {"chat_id":User_id, 
                            "text": 'Command to help',
                            "reply_markup": dumps(keyboard)}
                ReqGet(method="sendMessage", argsDict = argsDict)
                
            elif text == "/cloud" :
                keyboard = keyboars['keyboargs']['cloudKeyboard']
                argsDict = {"chat_id":User_id, 
                            "text": 'Command to cloudEditor',
                            "reply_markup": dumps(keyboard)}
                ReqGet(method="sendMessage", argsDict = argsDict)
            #elif text == "/register" :
                #вызов клавитуры
                #pass
        else:
            #это обычный текст
            pass


    def CallbackQueryAnalyzer(User_id, data):
        command = data['callback_query']['data']
        message_id = data['callback_query']['message']['message_id']
        print(command)
        with open('configRequests.json', "r") as f:
            keyboads = load(f)
        if command == "cloud":
            keyboard = keyboads['keyboargs']['cloudKeyboard']
            argsDict = {"chat_id" : User_id,
                        "message_id": message_id,
                        "text" : "cloudEditor commands",
                        "reply_markup" : dumps(keyboard)}
            ReqGet(method="editMessageText", argsDict = argsDict)
            #ReqGet(method="sendMessage", argsDict = argsDict)


        if command.split("_")[0] == "viewMyFile":
            argsDict = {"chat_id" : User_id,
                        "message_id": message_id,
                        "text" : "Your file: "}
            try:
                if command.split("_")[1] == "ALL":
                    ReqGet(method="editMessageText", argsDict = argsDict)
                    cloud.sendAllFile(data['callback_query'], arg = "all")
                    return
            
                if command.split("_")[1] == "LIST":
                    ReqGet(method="editMessageText", argsDict = argsDict)
                    cloud.sendAllFile(data['callback_query'], arg = "ls")
                    return
            except:
                print("Command viewMyFile пришла без парметра")

            keyboard = keyboads['keyboargs']['viewMyFileKeyboards']
            argsDict = {"chat_id" : User_id,
                        "message_id": message_id,
                        "text" : "viewMyFile commands",
                        "reply_markup" : dumps(keyboard)}
            ReqGet(method="editMessageText", argsDict = argsDict)

        '''
        if command.split("_")[0] == "viewMyFileALL":
            if command.split("_")[1] == "ALL":
                pass
            if command.split("_")[1] == "LIST":
                pass
            argsDict = {"chat_id" : User_id,
                        "message_id": message_id,
                        "text" : "Your file: "}
            ReqGet(method="editMessageText", argsDict = argsDict)
            cloud.sendAllFile(data['callback_query'], arg = "all")
        '''
        #if command == "viewMyFile_LIST":
        #    argsDict = {"chat_id" : User_id,
        #                "message_id": message_id,
        #                "text" : "Your file: "}
        #    ReqGet(method="editMessageText", argsDict = argsDict)
        #    cloud.sendAllFile(data['callback_query'], arg = "ls")


#----------------------------------------------\
#----------------------------------------------
#----------------------------------------------

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        data = request.json
        pprint.pprint(data)
        #print(json.keys())
    
    active = ['video', 'document', 'audio']



    #---Обработка сообщений
    if 'message' in data.keys():
        User_id = data['message']['from']['id'] 
        dataKeys = data['message'].keys()
        textMessageAnalyzer(User_id, data)
        #print("error")
    elif 'callback_query' in data.keys():
        User_id = data['callback_query']['from']['id'] 
        dataKeys = data['callback_query'].keys()
        print("BYE")# это колбек запрос
        CallbackQueryAnalyzer(User_id, data)
            
    return ''



if __name__ == '__main__':

    cloud = cloudEditor()

    app.run(
        host = WEBHOOK_LISTEN, 
        port = WEBHOOK_PORT,
        ssl_context=( WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV ), 
        debug = True)
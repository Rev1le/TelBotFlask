#import config
#import telebot
#from aiohttp import web
#import ssl
from subprocess import check_output
from flask import *
import requests
import pprint
#import telegram
import json
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

'''
class DB():
        def __init__(self):
            self.con = sq3.connect('cloudBD.db', check_same_thread=False)
            self.cur = self.con.cursor()
        
        
        def create_table(self):
            self.cur.execute("""CREATE TABLE IF NOT EXISTS tabl(
                id_tg INTEGER NOT NULL PRIMARY KEY,
                tg_name TEXT);""")
            self.ConCommit()

        def ConCommit(self):
            self.con.commit()

        def InputValues(self, id, name):
            self.cur.execute("SELECT * FROM tabl")
            self.name = name
            self.userId = id
            rest = (self.userId, self.name)
            try:
                self.cur.execute("INSERT INTO tabl VALUES(?,?);", rest)
                self.con.commit()
            except:
                #try:
                output = check_output(f"mkdir -m 777 -p users/{rest[0]}", shell = True)
                output = check_output(f"touch users/{rest[0]}/images.txt", shell = True)
                output = check_output(f"touch users/{rest[0]}/documents.txt", shell = True)
                output = check_output(f"touch users/{rest[0]}/video.txt", shell = True)
                #except:
                #    pass
            self.cur.execute("SELECT * FROM tabl")
            results = self.cur.fetchall()
            print(results)
            self.ConCommit()
        
        def test(self):
            print("Bd ready")
'''

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
        
        '''
        print(file_id)
        file_path = requests.get(API_TELEGRAMM+'/getFile'+ f'?file_id={file_id}').json()
        print(file_path)


        try:
            path = file_path['result']['file_path']
        
     
            #file = requests.get("https://api.telegram.org/file/bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA/" + file_path['result']['file_path'])
            #photo = file
            #file.raw.decode_content = True
            print(file.content)
            #rPhoto = photo #self.convertPhoto(photo)
            out = open("img.jpg", "wb")
            out.write(file.content)
            out.close

            self.idUser = data['message']['chat']['id']
            #output = check_output(f"touch users/{self.idUser}/images.txt", shell = True)
            out = open(f"users/{self.idUser}/images.txt", "a")
            out.write(f"https://api.telegram.org/file/bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA/{path}\n")
            out.close
        except:
            pass
        '''

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



        

app = Flask(__name__)

@app.route(f'/{API_TOKEN}/', methods=['POST'])
def Update():
    
    def ReqGet(method = "sendMessage", **kwargs):
        #kwarg = dict
        pass
    global cloud, flop
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        #print(json['message']['chat']['id'])
        a, b = '', ''
        print('\n\n')
        pprint.pprint(request.json)


        #reply_markup = telegram.InlineKeyboardMarkup(keyboard)

        #print(reply_markup)

        #update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)


        #v = {"resize_keyboard": False, "keyboard": [[{"text": "/command1"}], [{"text": "/command2"}]], "one_time_keyboard": False, "selective": False}
        #json = v.json()
        #print(JSON.stringify(v))
        #your_json = json.loads(v)
        #print(your_json)

        def textFunc(text: str):
            print(text)
            if text == "/help" :
                    pass
            elif text == "/createcloud" :
                cloud.createCloud(json)
            elif text == "!floopa" :
                r = random.randint(0, len(flop)-1)
                a = json['message']['chat']['id']
                print(flop[r], json)
                requests.get(API_TELEGRAMM+'/sendPhoto'+ f'?chat_id={a}'+'&'+ f'photo={flop[r]}')
            elif text.split()[0] == "/myfile" :
                args = 'error'
                try:
                    args = text.split()[1]
                    print(args)
                except IndexError:
                    requests.get(API_TELEGRAMM+f'/sendMessage'+ f'?chat_id={User_id}'+'&'+ f'text=Ошибка аргумента введите название файла, ls - для вывода всего списка файлов, all - для вывода всех файлов')
                cloud.sendAllFile(json, args)


        def decorDown(func):
            def wrapper(data:dict, key: str):
                #print("Я тут был")
                if key in ["photo","document","video"]: func(json, key)
            return wrapper

        def decorText(func):
            def wrapper(data:dict, key: str):
                if key == "text": 
                    print("это текст")
                    func(data['message']['text'])
            return wrapper
        
        
        try:
            User_id = json['message']['chat']['id']
        except:
            print(json)
            return ''

        @decorDown
        def download(json, key):
            print("Я тут был")
            cloud.downloadFile(json, key)
        
        @decorText
        def TextAnalis(text):
            print("Я тут был")
            textFunc(text)

        keysMessage = json['message'].keys()
        for key in keysMessage :
            download(json, key)
            TextAnalis(json, key)
            #pass

                


        '''
        for key in keysMessage :
            if key == "photo":
                cloud.downloadFile(json, 'photo')
            if key == "document":
                cloud.downloadFile(json, 'document')
            if key == "video":
                cloud.downloadFile(json, 'video')
            if key == "text" :
                print(json['message']['text'][0:7])
                if json['message']['text'] == "/help" :
                    pass
                elif json['message']['text'] == "/createcloud" :
                    cloud.createCloud(json)
                elif json['message']['text'] == "!floopa" :
                    r = random.randint(0, len(flop)-1)
                    a = json['message']['chat']['id']
                    print(flop[r], json)
                    requests.get(API_TELEGRAMM+'/sendPhoto'+ f'?chat_id={a}'+'&'+ f'photo={flop[r]}')
                elif json['message']['text'].split()[0] == "/myfile" :
                    args = 'error'
                    try:
                        args = json['message']['text'].split()[1]
                        print(args)
                    except IndexError:
                        requests.get(API_TELEGRAMM+f'/sendMessage'+ f'?chat_id={User_id}'+'&'+ f'text=Ошибка аргумента введите название файла, ls - для вывода всего списка файлов, all - для вывода всех файлов')
                        break
                    cloud.sendAllFile(json, args)
            '''
    return ''

    '''
        try:
            a = json['message']['chat']['id']
            b = json['message']['text']

            if b == '/createCloud':
                cloud.createCloud(json)
                return ''
            b = json
            print(json['message'])
        except KeyError:
            print(json['message'].keys())
            #cloud.downloadPhoto(json)
        
        myId = 848986553
        user_id = json['message']['from']['id']
        #'?chat_id=848986553&text=Без python не кошерно'
         выполнение команды
        if (user_id == myId): #проверяем, что пишет именно владелец
            try:
                comand = json['message']['text']  #текст сообщения
            except :
                pass
            try: #если команда невыполняемая - check_output выдаст exception
                #bot.send_message(message.chat.id, check_output(comand, shell = True))
                output = check_output(comand, shell = True)
                #o = output.replace("app.py", "%0A")
                rer = output.decode('utf-8')
                print(rer)
                if rer != "" :
                    requests.get(API_TELEGRAMM+'/sendMessage'+ f'?chat_id={a}'+'&'+ f'text={rer}')
                else :
                     requests.get(API_TELEGRAMM+'/sendMessage'+ f'?chat_id={a}'+'&'+ f'text={"команда сработала"}')
            except:
                #bot.send_message(message.chat.id, "Invalid input") #если команда некорректна
                requests.get(API_TELEGRAMM+'/sendMessage'+ f'?chat_id={a}'+'&'+ f'text= {"Invalid%20input"}')
            #requests.get(API_TELEGRAMM+'/sendMessage'+ f'?chat_id={a}'+'&'+ f'text={user_id}')
        '''


#def keyBoard():
    '''
    bot = TeleBot(token="5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA")
        
    keyboard = ["banana", "chocolate", "apple"]
    keyboard_S = [[ telegram.InlineKeyboardButton("Hackerearth", callback_data='HElist8'),
                          telegram.InlineKeyboardButton("Hackerrank", callback_data='HRlist8')],
                        [ telegram.InlineKeyboardButton("Codechef", callback_data='CClist8'),
                          telegram.InlineKeyboardButton("Spoj", callback_data='SPlist8')],
                        [ telegram.InlineKeyboardButton("Codeforces", callback_data='CFlist8'),
                          telegram.InlineKeyboardButton("ALL", callback_data='ALLlist8')]]
        
    reply_markup = telegram.InlineKeyboardMarkup(keyboard_S)

        #kb_fruits = keyboa_maker(items = keyboard, copy_text_to_callback=True)

    bot.send_message(chat_id=848986553, reply_markup=reply_markup, text ="Please select!")'''

    #my_bot = telegram.ext.Updater(API_TOKEN,"https://api.telegram.org/", use_context=True)
    
    #bot = TeleBot(token="5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA")
    #my_keyboard = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton('анектод')],[telegram.InlineKeyboardButton('начать')]])
    

    #print(my_keyboard)
    #requests.get(API_TELEGRAMM+f"/sendMessage?chat_id=848986553&text=Hello&reply_markup={my_keyboard}")
    #bot.send_message(chat_id=848986553, reply_markup=my_keyboard, text ="Please select!")

flop = ['https://media1.tenor.com/images/9f61077990a3c31033c1620934dde704/tenor.gif?itemid=18413111',
    'https://pbs.twimg.com/media/EqF0aJhXUAIIB6R.jpg',
    'https://sun1-28.userapi.com/zKVb8i7AFgRa33SkuVMx-0sM9wxPi4YNIFgFFQ/FJV3XE-Pt7U.jpg',
    'https://static.wikia.nocookie.net/d49c64fe-08d8-4e1d-bdb0-f656fe87ed8d',
    'https://i.ytimg.com/vi/PV-DCnBwY5E/maxresdefault.jpg',
    'https://media1.tenor.com/images/f17cb7f46db22305680b1ea671b32f02/tenor.gif?itemid=20154951',
    'https://media1.tenor.com/images/3dccd2405c1d609ed9ca4f3d52ed34ce/tenor.gif?itemid=20873337',
    'https://sun9-39.userapi.com/impg/OPtlnqDnk4Kt8eQk9SXeG2eo_3c473BCBLiVVw/xyEJO5jKVkQ.jpg?size=720x725&quality=96&sign=797177db7f6e41a585969f7ade9a3dc4&type=album',
    'https://sun9-18.userapi.com/impg/XMCHHKX73dlZnHiyEIWQqsjI-8nBQL-OkqHBag/gtJgS9CdaM8.jpg?size=1343x761&quality=96&sign=dd6bd8d20ba320449a51378fdd9164ef&type=album',
    'https://sun9-27.userapi.com/impg/gaerHcEnPxCsfUPYp6Cf5HJ66kf0siYdRt_Jxw/6h6Zdaufywk.jpg?size=1347x761&quality=96&sign=101ce87ba353ad129b61e4a93e99ef90&type=album',
    'https://sun9-77.userapi.com/impg/iug8LAq1YUEHGRuJBecXgfV6zi-41BvMxMb6Fg/zzrUAx-XPUY.jpg?size=1346x759&quality=96&sign=6e7a3070b3b970e8055d40c7aab95e02&type=album',
    'https://c.tenor.com/-aMDPDf-wY4AAAAC/floppa.gif',
    'https://media1.tenor.com/images/5566cd1553c09d13096cb4d176266708/tenor.gif?itemid=19599491',
    'https://sun9-7.userapi.com/impg/kVrpyqGf2TvTf528FjnGfcwJhi994rWml2iMXw/wmj5CMuQkJ0.jpg?size=2560x1846&quality=96&sign=6f1b4b326ea007cb2d3a5527e7b23435&type=album',
    'https://sun1-13.userapi.com/impg/i6We6bTKQoWAFf3qokhEQpKB4CEXADttBOd-Hw/aFx2EES8lBo.jpg?size=1080x1164&quality=96&sign=da986ce1ffcc7eb9fac355e80d5fc68b&type=album',
    'https://sun9-11.userapi.com/impg/WHhoAkSSFdg661KfBS0aomdses6BipB4x4d7-g/fd1DK934boE.jpg?size=1500x1500&quality=96&sign=ff8ed2ff40312a8f7797699cd459a088&type=album',
    'https://sun9-47.userapi.com/impg/_Z77hh74t_gJtZwRRKt6CCqcRBnC0YJtIroMNw/az0GNpKDsq8.jpg?size=800x800&quality=96&sign=f4e74c987468bcbde906610dd413c7ed&type=album',
    'https://sun9-7.userapi.com/impg/kFHh0CaC7RihRKmMuw8qOJQ9e0Id362MmP9CpA/OVvV9-gywog.jpg?size=1200x850&quality=96&sign=6117e402567d4735e764be04b2dddb7f&type=album']


if __name__ == '__main__':

    #keyBoard()

    #db = DB()

    cloud = cloudEditor()

    app.run(
        host = WEBHOOK_LISTEN, 
        port = WEBHOOK_PORT,
        ssl_context=( WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV ), 
        debug = True)



'''{'callback_query': {'chat_instance': '-5862831923088722852',
                    'data': 'hello world',
                    'from': {'first_name': 'Rev1le',
                             'id': 848986553,
                             'is_bot': False,
                             'language_code': 'ru',
                             'username': 'r_ev1le'},
                    'id': '3646369481646663218',
                    'message': {'chat': {'first_name': 'Rev1le',
                                         'id': 848986553,
                                         'type': 'private',
                                         'username': 'r_ev1le'},
                                'date': 1649075490,
                                'from': {'first_name': 'peHelper',
                                         'id': 5013260088,
                                         'is_bot': True,
                                         'username': 'peHelper_bot'},
                                'message_id': 1055,
                                'reply_markup': {'inline_keyboard': [[{'callback_data': 'hello '
                                                                                        'world',
                                                                       'text': 'hello'}]]},
                                'text': 'Hellochild'}},
 'update_id': 172631697}'''

#inline
#https://api.telegram.org/bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA/sendMessage?chat_id=848986553&text=Hellochild&reply_markup={%22inline_keyboard%22:%20[[{%22text%22:%20%22hello%22,%22callback_data%22:%20%22hello%20world%22}]]}

#reply
#"https://api.telegram.org/bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA/sendMessage?chat_id=848986553&text=AllComands:&reply_markup=%20{%22keyboard%22:%20[[%22/createCloud%22,%22/myFile%22],[%22/help%22,%22/about%22]],%22resize_keyboard%22:true}"

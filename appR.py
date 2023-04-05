import asyncio
from subprocess import check_output
from flask import *
import requests
import pprint
from json import *

with open('config.json', "r") as f:
    config = load(f)

WEBHOOK_LISTEN = config['config']['webhookSettings']['WEBHOOK_LISTEN']
WEBHOOK_PORT = config['config']['webhookSettings']['WEBHOOK_PORT']

WEBHOOK_SSL_CERT = config['config']['SSL']['WEBHOOK_SSL_CERT']
WEBHOOK_SSL_PRIV = config['config']['SSL']['WEBHOOK_SSL_PRIV']

API_TOKEN = config['config']['API']['API_TOKEN']
API_TELEGRAMM = config['config']['API']['API_TELEGRAMM']


class cloudEditor():

    def createCloud(self, data):  # старый класс
        idUser = data['message']['chat']['id']

        try:
            f = open(f'users/{idUser}/user.txt', "w")
            f.write(str(data['message']['from']))
            f.close()
            output = check_output(f"cd users/{idUser}", shell=True)
            requests.get(API_TELEGRAMM+'/sendMessage' +
                         f'?chat_id={idUser}'+'&' + f'text=Облако%20не%20нуждается%20в%20создании')
        except:
            output = check_output(
                f"mkdir -m 777 -p users/{idUser}", shell=True)
            f = open(f'users/{idUser}/user.txt', "w")
            f.write(data['message']['from'])
            f.close()
            requests.get(API_TELEGRAMM+'/sendMessage' +
                         f'?chat_id={idUser}'+'&' + f'text=Облако%20было%20создано')

    def downloadFile(self, data: dict, key: str):
        file_id = data['message'][key]
        try:
            # при азгрузке фото предоставялется 3 file_id
            file_id = file_id[-1]["file_id"]
        except:
            file_id = file_id["file_id"]

        self.idUser = data['message']['chat']['id']

        out = open(f"users/{self.idUser}/{key}.txt", "a")
        out.write(f"{file_id}\n")
        out.close
        requests.get(API_TELEGRAMM+'/sendMessage' +
                     f'?chat_id={self.idUser}'+'&' + f'text=Файл%20был%20загружен%20в%20{key}')

    def sendAllFile(self, data, arg="error"):
        User_Id = data['message']['chat']['id']
        output = check_output(
            f"ls users/{User_Id}", shell=True).decode('utf-8').split()
        # print(output)
        if arg == "all":
            dick = {"document": "sendDocument",
                    "photo": "sendPhoto", "video": "sendVideo"}
            for fileName in output:
                if fileName == "user.txt":
                    continue
                f = open(f"users/{User_Id}/{fileName}", "r")
                Allfile = f.read().split()
                print(Allfile)
                for i in range(len(Allfile)):
                    requests.get(API_TELEGRAMM+f'/{dick[fileName[0:-4]]}' +
                                 f'?chat_id={User_Id}'+'&' + f'{fileName[0:-4]}={Allfile[i]}')
                f.close()
                # добавить ls
        elif arg == "ls":
            for fileName in output:
                f = open(f"users/{User_Id}/{fileName}", "r")
                Allfile = f.read().split()
                print(Allfile)
                requests.get(API_TELEGRAMM+f'/sendMessage' +
                             f'?chat_id={User_Id}'+'&' + f'text={fileName[0:-4]} имеется {len(Allfile)}')
                f.close()
        elif arg == "error":
            pass
        else:
            requests.get(API_TELEGRAMM+f'/sendMessage' +
                         f'?chat_id={User_Id}'+'&' + f'text=функционал не доделан')


# -Функция запроса
def ReqGet(method=None, argsDict={}):
    return requests.get(f'{API_TELEGRAMM}/{method}', params=argsDict)


with open('configTelegramKeyboards.json', "r") as f:
    keyboards = load(f)

with open('GodPart.json', "r") as g:
    raspisanJSON = load(g)

# @cache


def textMessageAnalyzer(User_id: int,Chat_id,  data):

    try:
        text = data['message']['text']
    except:
        return


    if text[0] == "/":

        print("this is comand")
        text = text.split('@')[0]
        print(text)
        if text == "/start":
            print("вызов пошел")

        elif text == '/help':
            message_id = data['message']['message_id']
            keyboard = keyboards['keyboards']['helpKeyboard']
            
            argsDict = {
                "chat_id": Chat_id,
                "text": 'Command to help',
                "reply_markup": dumps(keyboard),
                "disable_notification" : True
                }
            ReqGet(method="sendMessage", argsDict=argsDict)

            argsDict = {
                "chat_id": Chat_id,
                "message_id": message_id
                }
            ReqGet(method="deleteMessage", argsDict=argsDict)

        elif text == "/cloud":
            keyboard = keyboards['keyboards']['cloudKeyboard']
            
            argsDict = {
                "chat_id": Chat_id,
                "text": 'Command to cloudEditor',
                "reply_markup": dumps(keyboard),
                "disable_notification" : True
                }
            ReqGet(method="sendMessage", argsDict=argsDict)

        elif text.split()[0] == "/reg":
            checkUserInBD = bd.getValues(column="Tg_id", value=User_id)  # LIMIT 1
            bd.Close()

            if checkUserInBD:

                argsDict = {
                    "chat_id": Chat_id,
                    "text": 'Пользователь уже создан',
                    "disable_notification" : True
                    }
                return ReqGet(method="sendMessage", argsDict=argsDict)

            elif text.split()[1]:
                tg_name = data['message']['from']['username']
                bd.CreateUser(text.split()[1], Tg_name=tg_name, Tg_id=User_id)
                
                argsDict = {
                    "chat_id": Chat_id,
                    "text": 'Регистрация прошла успешно',
                    "disable_notification" : True
                    }
                ReqGet(method="sendMessage", argsDict=argsDict)
            else:
                
                argsDict = {
                    "chat_id": Chat_id,
                    "text": 'Ошибка в регистрации',
                    "disable_notification" : True
                    }
                ReqGet(method="sendMessage", argsDict=argsDict)
    else:
        # это обычный текст
        pass

# @cache(maxsize = 128)


def CallbackQueryAnalyzer(User_id, Chat_id, data):
    command = data['callback_query']['data']
    message_id = data['callback_query']['message']['message_id']
    print(command)

    if command == 'registerAccaunt':
        
        argsDict = {
            "chat_id": Chat_id,
            "message_id": message_id,
            "disable_notification" : True,
            "text": "Чтобы зарегстрировать аккаунт небходимо написать: /reg YOUR_PASSWORD"
            }
        ReqGet(method="editMessageText", argsDict=argsDict)
    
    elif command == "exit":

        argsDict = {
            "chat_id": Chat_id,
            "message_id": message_id,
            "disable_notification" : True
            }
        ReqGet(method="deleteMessage", argsDict=argsDict)
        #ReqGet(method="sendMessage", argsDict = argsDict)
    
    elif command == 'about':
        with open('www.lightaudio.ru.mp3', 'rb+') as voice:
            
            argsDict = {
                "chat_id": Chat_id,
                "message_id": message_id,
                "disable_notification" : True,
                "text": "Мур-мур-мур"
                }
            ReqGet(method="editMessageText", argsDict=argsDict)

            argsDict = {
                "chat_id": Chat_id, 
                "audio" : "https://cdn.discordapp.com/attachments/860822568806383647/1005371598188068904/www.lightaudio.ru.mp3"
                }
            ReqGet(method="sendAudio", argsDict = argsDict)

    elif command == "cloud":
        keyboard = keyboards['keyboards']['cloudKeyboard']

        argsDict = {
            "chat_id": Chat_id,
            "message_id": message_id,
            "disable_notification" : True,
            "text": "cloudEditor commands",
            "reply_markup": dumps(keyboard)
            }
        ReqGet(method="editMessageText", argsDict=argsDict)
        #ReqGet(method="sendMessage", argsDict = argsDict)

    elif command.split("_")[0] == "viewMyFile":
        
        argsDict = {
            "chat_id": Chat_id,
            "message_id": message_id,
            "disable_notification" : True,
            "text": "Your file: "
            }
        try:
            if command.split("_")[1] == "ALL":
                ReqGet(method="editMessageText", argsDict=argsDict)
                cloud.sendAllFile(data['callback_query'], arg="all")
                return

            if command.split("_")[1] == "LIST":
                ReqGet(method="editMessageText", argsDict=argsDict)
                cloud.sendAllFile(data['callback_query'], arg="ls")
                return
        except:
            print("Command viewMyFile пришла без парметра")

        keyboard = keyboards['keyboards']['viewMyFileKeyboards']
        
        argsDict = {
            "chat_id": Chat_id,
            "message_id": message_id,
            "text": "viewMyFile commands",
            "disable_notification" : True,
            "reply_markup": dumps(keyboard)
            }
        ReqGet(method="editMessageText", argsDict=argsDict)

    elif command == "setMessageHome":
        keyboard = keyboards['keyboards']['helpKeyboard']
        argsDict = {
            "chat_id": Chat_id,
            "disable_notification" : True,
            "text": 'Command to help',
            "reply_markup": dumps(keyboard)
            }
        ReqGet(method="deleteMessage", argsDict={
               "chat_id": Chat_id, "message_id": message_id
               })

        ReqGet(method="sendMessage", argsDict=argsDict)

    elif command == "raspisaniePE":
        keyboard = keyboards['keyboards']['raspisaniedaysKeyboards']
        
        argsDict = {
            "chat_id": Chat_id,
            "message_id": message_id,
            "disable_notification" : True,
            "text": 'Дни расписания',
            "reply_markup": dumps(keyboard)
            }
        ReqGet(method="editMessageText", argsDict=argsDict)

    elif command.split("_")[0] == 'viewRasp':

        def strRasp(day: str):
            dayRasp = raspisanJSON[day]
            raspStr = ''
            for i in dayRasp.keys():
                #a = dayRasp[i]
                raspStr = raspStr + \
                    f"\n\n{i[0]} пара:\n-->{dayRasp[i][0]}\n\n{dayRasp[i][1]}"
            # pprint.pprint(raspStr)

            return raspStr

        command = command.split("_")[1]

        dictDayOfday = {
            "Pone": 'понедельник',
            "Vtor": 'вторник ',
            "Sred": 'среда',
            "Chet": 'четверг',
            "Pytn": 'пятница ',
            "Sybot": 'суббота'
        }

        dayName = dictDayOfday[command]

        argsDict = {"chat_id": Chat_id,
                    "message_id": message_id,
                    "disable_notification" : True,
                    "text": strRasp(dayName),
                    "reply_markup": dumps(
                        {
                            "inline_keyboard":
                                [[{
                                    "text": "back",
                                    "callback_data": "raspisaniePE"
                                }]]
                        }
                    )}

        ReqGet(method="editMessageText", argsDict=argsDict)
    
    elif command.split("_")[0] == 'coocked':
        keyboard = keyboards['keyboards']['coockedKeyboard']
        argsDict = {"chat_id": Chat_id,
                    "message_id": message_id,
                    "disable_notification" : True,
                    "text": "Кулинария:",
                    "reply_markup": dumps(keyboard)}
        ReqGet(method="editMessageText", argsDict=argsDict)

    else:
        print("this command not found!!!")


# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
app = Flask(__name__)


@app.route(f'/{API_TOKEN}/', methods=['POST'])
def Update():
    #global ReqGet
    global cloud, keyboards, bd

    #content_type = request.headers.get('Content-Type')

    if (content_type := request.headers.get('Content-Type') == 'application/json'):
        data = request.json
        pprint.pprint(data)


    # ---Обработка сообщений
    if 'message' in data.keys():
        User_id = data['message']['from']['id']
        Chat_id = data['message']['chat']['id']
        textMessageAnalyzer(User_id, Chat_id, data)

    elif 'callback_query' in data.keys():
        User_id = data['callback_query']['from']['id']
        Chat_id = data['callback_query']['message']['chat']['id']
        print("BYE")  # это колбек запрос
        CallbackQueryAnalyzer(User_id, Chat_id, data)

    return ''


if __name__ == '__main__':

    from BD import DBForAll

    cloud = cloudEditor()
    bd = DBForAll()
    bd.Connect()
    bd.create_table()

    app.run(
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)

    bd.Close()

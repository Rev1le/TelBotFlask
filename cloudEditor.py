from subprocess import check_output

class cloudEditor():

    def FileWrite(self, path = None, data = None, method = 'w'):
        try: 
            f = open(path, method)
            f.write(data)
            f.close()
        except:
            print("Ошибка с записью в файл")

    

    def createCloud(self, userId: int):
        idUser = userId#data['message']['chat']['id']
        #self.FileWrite
        
        #self.FileWrite(f'users/{idUser}/user.txt', str(data['message']['from']), 'w')
        output = check_output(f"ls users/", shell = True).decode('utf-8').split()

        try:
            output = check_output(f"cd users/{idUser}", shell = True)
            return False
        except:
            output = check_output(f"mkdir -m 777 -p users/{idUser}", shell = True)
            return True
        return False



    def downloadFile(self, data: dict, key = "document"):
        file_id = data['message'][key]
        try:
            file_id = file_id[-1]["file_id"] #при азгрузке фото предоставялется 3 file_id
        except:
            file_id = file_id["file_id"]
        

        idUser = data['message']['chat']['id']
        self.FileWrite(path = f"users/{idUser}/{key}.txt", data = f"{file_id}\n", method =  "a")
        
        return f'Файл%20был%20загружен%20в%20{key}'


    def sendAllFile(self, data, arg = "error"):
        User_Id = data['message']['chat']['id']

        output = check_output(f"ls users/{User_Id}", shell = True).decode('utf-8').split()
        #print(output)
        dictReturn = {}
        if arg == "all":
            dick = {"document":"sendDocument", "photo": "sendPhoto", "video" : "sendVideo"}
            for fileName in output:
                if fileName == "user.txt":
                    continue
                f = open(f"users/{User_Id}/{fileName}", "r")
                Allfile = f.read().split()
                #print(Allfile)
                tmpDict = {}
                for i in range(len(Allfile)):
                    tmpDict[Allfile[i]] = fileName[0:-4]
                
                dictReturn[dick[fileName[0:-4]]] = tmpDict
                f.close()
                

        elif arg == "ls":
            tmpDict = {}
            for fileName in output:
                if fileName == "user.txt": continue
                f = open(f"users/{User_Id}/{fileName}", "r")
                Allfile = f.read().split()
                #print(Allfile)
                
                tmpDict[f'{fileName[0:-4]} имеется {len(Allfile)}'] = "text"
                f.close()
            dictReturn["sendMessage"] = tmpDict
        elif arg == "error":
            pass
        #else :
            #dictReturn["sendMessage"] = "Функционал не доделан"

        
        return dictReturn

import json

keyboard = {
    "inline_keyboard": [[
        {
            "text": 'some text',
            "url": "some url"
        }
    ]]
}

data = {
    "chat_id": 231442,
    "text": 'some text',
    "reply_markup": json.dumps(keyboard)
}

#print(json.dumps(keyboard))

"https://api.telegram.org/bot5013260088:AAEeM57yLluiO62jFxef5v4LoG4tkLVvUMA/sendMessage?chat_id=848986553&text=AllComands:&reply_markup=%20{%22keyboard%22:%20[[%22/createCloud%22,%22/myFile%22],[%22/help%22,%22/about%22]],%22resize_keyboard%22:true}"


def test(json, key):
    print(key)



def decor(func):
    def wrapper(data:dict, key: str):
        if key in ["photo","document","video"]: func(json, key)
        else: pass
    return wrapper

@decor
def download(json, key):
    test(json, key)


download("re", "gsgs")

a = None
if a :
    print(2)
import pandas as pd

data = pd.read_csv(filepath_or_buffer='/home/roma/PythonApp/TelBot/rasp.csv', encoding='Windows-1251')

print(data[data['№ пары'] == 2])
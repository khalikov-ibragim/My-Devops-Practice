# 2.Мы испортируем библиотеку "request"
import requests

# 4.Мы импортируем библиотеку "csv"
import csv

# 7.Создаем переменную которая хранит в себе запрос GET к сайту
response = requests.get("https://jsonplaceholder.typicode.com/users")

# 10.Преобразовываем переменную "response" в переменную "data" в формате json иначе будет просто выводиться статус кода сайта
data = response.json()


# 13.Создаение функции "save_def" и перекидывание в него существующей переменной и не существующей
def save_def(data, filename):
    # 15.Открытие и создание нового файла "filename" с типом записи и автоматическим закрытием
    with open(filename, "w", newline="") as f:
        # 17.Создаем переменную "writen" и используем "csv.DictWriten" для создания своих названий колонок в словаре
        writer = csv.DictWriter(f, fieldnames=["Name", "Email", "Username", "Phone"])
        # 19.Вписываем названия наших колонок  в первую строку нашего csv file
        writer.writeheader()
        # 21.Создаем цикл и переменную "date" внутри "data"
        for date in data:
            # 23.writerow означает создание вида записи ввиде одной строки с запятыми
            writer.writerow(
                # 25-30 Приравниваем наши колонки к названиям колонок в json для вывода определенных колононк которые мы хотим
                {
                    "Username": date["username"],
                    "Name": date["name"],
                    "Email": date["email"],
                    "Phone": date["phone"],
                }
                # 32 Закрытие "writerow"
            )
    # 34 Возврат данных переменной из функции
    return filename


# 37 Вызов функции и запись ей названия
result = save_def(data, "python_trending.csv")
# 39 открытие файла result в виде чтения и автоматического закрытия
with open(result, "r") as f:
    # 41 Вывод данных из данного файла
    print(f.read())

# Импорт библиотеки FastApi
from fastapi import FastAPI

# Присваивание переменной значения FastAPI
data = FastAPI()


# Декоратор привязываюший выполнение функции снизу к конкретному корневому URL
@data.get("/")
# Выполнение функции при переходе и работе в данном URL
def home():
    return {"name:Andreym, age:22, education:teacher,city:Moscow"}

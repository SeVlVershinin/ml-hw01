# Сервис предсказания стоимости автомобиля (д/з №1 по Машинному обучению, МОВС2023)  
Сервис предсказания стоимости автомобилей по их признаковому описанию разработан в рамках 
выполнения домашнего задания №1 по предмету "Машинное обучение" в магистратуре МОВС2023. 

Видео-демонстрация работы с сервисом [размещена на YouTube](https://www.youtube.com/watch?v=gY5yGY9AT9c)

- [Запуск сервиса](#запуск-сервиса)
- [Анализ данных](#анализ-данных)
- [Обучение модели](#обучение-моделей)
- [Feature engineering](#feature-engineering)
- [Сервис на FastApi](#сервис-на-fastapi)

## Запуск сервиса
Для запуска сервиса на локальной машине: 
- склонируйте данный репозиторий
```commandline
git clone https://github.com/SeVlVershinin/ml-hw01.git
```
- установите необходимые библиотеки Python с помощью pip install
```commandline
pip install -r requirements.txt
```
- запустите сервис, запустив его с помощью uvicorn
```commandline
uvicorn main:app --host "0.0.0.0" --port 80
```
После этого вы можете открыть страницу с описанием методов сервиса по ссылке ```http://localhost/docs``` 

Для работы сервиса необходима версия Python 3.11





## Анализ данных
To be done
## Обучение моделей
To be done
## Feature engineering
To be done
## Сервис на FastApi
To be done
![Screenshot](img/test_image.png)


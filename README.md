# Сервис предсказания стоимости автомобиля (д/з №1 по Машинному обучению, МОВС2023)  
Сервис предсказания стоимости автомобилей по их признаковому описанию разработан в рамках 
домашнего задания №1 по предмету "Машинное обучение" в магистратуре МОВС2023. В ходе разработки 
был проведен разведочный анализ данных и предварительная подготовка тренировочного и тестового датасетов, 
конструирование новых и преобразование существующих признаков, обучение и оценка моделей линейной регрессии, 
а также создание на базе лучшей модели данного сервиса предсказания стоимости автомобилей. 

Видео-демонстрация работы с сервисом [размещена на YouTube](https://www.youtube.com/watch?v=gY5yGY9AT9c)

Краткое описание результатов выполненной работы приведено ниже. Подробное описание работы приведено 
в данном [Jupyter Notebook](https://github.com/SeVlVershinin/ml-hw01/blob/main/HW1_Regression_with_inference.ipynb)

- [Анализ данных](#анализ-данных)
- [Обучение модели](#обучение-моделей)
- [Конструирование и преобразование признаков. Обучение модели](#конструирование-и-преобразование-признаков-обучение-модели)
- [Сервис на FastApi](#сервис-на-fastapi)
- [Запуск сервиса](#запуск-сервиса)

## Анализ данных
В ходе анализа данных:
- проведен обзорный анализ тренировочного и тестового датасетов (далее - трейн и тест, соответственно); 
- выявлено наличие пропусков в значениях признаков mileage, engine, max_power, torque и seats в трейне и тесте, 
которые были заполнены соответствующими медианами трейна (за исключением признака torque, который был удален в связи 
со сложностью его парсинга);
- удалены дубликаты в трейне (1159 объектов с дублирующим признаковым описанием);
- признаки mileage, engine, max_power были преобразованы в численные путем удаления из них наименование 
единиц измерения;
- было определено, что признак seats, несмотря числовой тип, скорее является категориальным, так как имеет 
ограниченный дискретный набор значений и не имеет линейной зависимости с целевой переменной; 
- стало понятно, что наибольшее влияние на целевую переменную оказывают признаки max_power (коэффициент корреляции 0.69),
engine (коэффициент корреляции - 0.45) и year (коэффициент корреляции - 0.43). Также на целевую переменную оказывает 
влияние марка автомобиля.


Более подробное описание хода и результатов анализа данных можно найти [здесь](EDA.md) 
или в [ноутбуке](HW1_Regression_with_inference.ipynb)

## Обучение моделей
В рамках обучения моделей линейной регрессии было сделано следующее: 
- на числовых признаках была обучена простая модель линейной регрессии ```LinearRegression```, эффективность 
предсказаний которой оказалась не очень высокой (R^2 = ~ 0.59); 
- дополнительная стандартизация признаков и использование L1-регуляризации (```Lasso```) с коэффициентом регуляризации 
равным 1 (значение по умолчанию) практически не изменило качество модели;
- поиск оптимального значения коэффициента регуляризации подбором по сетке и кросс-валидацией с 10 фолдами занулил
некоторые коэффициенты модели, но даже слегка ухудшил ее качество (R^2 = ~ 0.58);
- использование ```ElasticNet``` с подбором параметров ```alpha``` и ```l1_ratio```  по сетке и кросс-валидацией с 
10 фолдами не улучшил качество модели (R^2 = ~ 0.58).

Однако, после добавление в модель категориальных признаков, закодированных с помощью one hot encoding, и подбором 
параметра ```alpha``` для ```Ridge```-регрессии по сетке с кросс-валидацией качество модели немного улучшилось, хоть и 
незначительно (R^2 = ~ 0.66 для трейна и ~ 0.61 для теста)
  


## Конструирование и преобразование признаков. Обучение модели
В рамках конструирования и преобразования признаков было сделано следующее: 
- добавлен признак, характеризующий количество лошадиных сил на литр объема двигателя;
- в признаке year год заменен на квадрат года;
- категориальный признак owner заменен на числовой (число владельцев). *В результате экспериментов от этой 
модификации признака пришлось отказаться, т.к. ощутимого результата она не дает, но создает проблемы при подготовке 
признаков внутри сервиса для использования в предсказании*; 
- из трейна удалены объекты с выбросами численных параметров year, max_power, km_driven, mileage, engine, а также с 
выбросами целевой переменной;
- первые два слова в наименовании автомобиля (бренд и название модели) стали использоваться в качестве категориального
признака (до этого данный признак не использовался совсем);
- для обучения модели решено использовать не значения целевой переменной y, а ее логарифм ln(y). Соответственно, 
предсказания модели будут возвращаться не в чистом виде, а как exp(y_predicted). 

После преобразования существующих и добавления новых признаков, кодирования и стандартизации выполнен подбор 
параметра ```alpha``` для  ```Ridge```-регрессии по сетке с кросс-валидацией по 10- фолдам и **получена модель, 
качество которой существенно возросло** (R^2 = ~ 0.95 для трейна и ~ 0.91 для теста). 

Также для предсказаний полученной модели на тестовом датасете рассчитана бизнес-метрика (долю предсказаний, отличающихся 
от реальных цен на авто не более чем на 10%), значение которой составило 47.7% 

## Сервис на FastApi
На базе лучшей модели линейной регрессии, полученной на предыдущем этапе, была разработан сервис на FastApi, 
выполняющий предсказание цены автомобилей по их признаковому описанию. Сервис предоставляет три endpoint-а: 
- ... - позволяет
- ... - позволяет
- ... - позволяет

С точки зрения реализации сервис состоит из следующих элементов: 
- ```main.py```, содержащий реализацию API на FastApi;
- ```api/models.py```, содержащий Pydantic-модели для признакового описания объекта;
- ```models/model.py```, содержащий класс ML-модели, отвечающий за предварительную подготовку переданных признаков 
(очистка, заполнение пропусков, конструирование признаков, стандартизация и кодирование) и за предсказание
значений целевой переменной на базе обученной модели линейной регрессии;
- файлы ```models/*.pickle```, содержащие сериализованные объекты, обученные ранее на трейне, и предназначенные 
для решения задачи предсказания.


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

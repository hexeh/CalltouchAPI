# CalltouchAPI
#### Простой класс для работы с API сервиса Calltouch на языке Python

---

<p align="center">
<b><a href = "https://support.calltouch.ru/hc/ru/sections/201900285">Документация по API Calltouch</a></b>
</p>

---

## Использование 

### Инициализация

Для начала работы с API Calltouch необходимо получить *ключ доступа* и *идентификатор сайта* ([подробнее](https://support.calltouch.ru/hc/ru/articles/209242609)).

```python
""" Инициализация класса """
ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
```

### Получение статистики по звонкам

API допускает получать статистику по звонкам 2 способами:

#### [Получение данных статистики](https://support.calltouch.ru/hc/ru/articles/209230609)

  В случае использования этого варианта имеется возможность уточнять степень детализации статистики:
  - Суммарное количество звонков за выбранный период
 
  ```python
  from calltouch_definition import CalltouchApi
  
  ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
  stats = ct.captureStats('11/07/2017', '11/07/2017')
  """Помимо такого использования, можно явно указать степень разбиения статистики.
  Например:
  stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsTotal')
  """
  print(stats)
  ```

  - Суммарное количество звонков за выбранный период в разбивке по дням
  ```python
  import pprint
  from calltouch_definition import CalltouchApi
  
  pp = pprint.PrettyPrinter(indent = 4)
  ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
  stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsByDate')
  
  print(stats)
  ```
  - Суммарное количество звонков из поисковых систем в разбивке по дням
  ```python
  import pprint
  from calltouch_definition import CalltouchApi
  
  pp = pprint.PrettyPrinter(indent = 4)
  ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
  stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsByDateSeoOnly')
  
  print(stats)
  ```
  - Суммарное количество звонков из поисковых систем в разбивке по ключевым фразам
  ```python
  import pprint
  from calltouch_definition import CalltouchApi
  
  pp = pprint.PrettyPrinter(indent = 4)
  ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
  stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsByKeywords')
  
  print(stats)
  ```
  **Входные параметры** метода *captureStats*:
  
  - Дата начала сбора статистики (в формате **dd/mm/yyyy**)
  - Дата окончания сбора статистики (в формате **dd/mm/yyyy**)
  - Разбиение (необязательный параметр, в случае задания возможные значения: *callsTotal*, *callsByDate*, *callsByDateSeoOnly*, *callsByKeywords*)
  
  **Возвращаемое значение** отличается в зависимости от выбранного типа разбиения:
  
  - При выборе статистики без разбивки возвращается целое число
  - При выборе статистики с разбивкой по дням (вне зависимости от того, выбираются все звонки или только из поисковых систем) возвращается список словарей с ключами *date* и *calls*
  - Пот выборе статистики с разбивкой по ключевым словам возвращается список словарей с ключами *keyword* и *calls*
    
#### [Получение данных о звонках](https://support.calltouch.ru/hc/ru/articles/209231269)

  При использовании этого варианта имеется возможность указать ряд параметров, в текущей реализации предусмотрена только их часть:
  
   - Модель атрибуции (последнее (0) или последнее непрямое (1) взаимодействие)
   - Возвращать только целевые звонки
   - Возвращать только уникальные звонки
   - Возвращать только уникально-целевые звонки
   - Возвращать только обратные звонки
   
  Кроме того, метод позволяет получать статистику только за один день.
  
  ```python
  import pprint
  from calltouch_definition import CalltouchApi
  
  pp = pprint.PrettyPrinter(indent = 4)
  ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
  stats = ct.captureCalls('11/07/2017', '1', 'false', 'false', 'false', 'false')
  
  print(stats)
  ```
  
  **Входные параметры** метода *captureCalls*:
  
  - Дата сбора статистики (в формате **dd/mm/yyyy**)
  - Модель атрибуции (*1* или *0*)
  - Только целевые звонки ('true', 'false')
  - Только уникальные звонки ('true', 'false')
  - Только уникально-целевые звонки ('true', 'false')
  - Только обратные звонки ('true', 'false')
  
  **Возвращаемое значение** представляет собой список словарей следующего вида:
  
  ```json
  {
    "date": "Дата из входных параметров",
    "source": "Источник трафика, с которого поступили звонки",
    "name": "Значение из utm_campaign для звонков",
    "ordinaryCalls": "Общее количество звонков для такой комбинации источника/кампании",
    "uniqCalls": "Количество уникальных звонков для такой комбинации источника/кампании",
    "targetCalls": "Количество целевых звонков для такой комбинации источника/кампании",
    "uniqTargetCalls": "Количество уникально-целевых звонков для такой комбинации источника/кампании"
  }
  ```
  
  ### [Получение записей звонков](https://support.calltouch.ru/hc/ru/articles/209189625)
  
  Возможность скачивания записей звонков в формате *mp3* реализована при помощи метода *captureRecords*
  
  ```python
  import pprint
  from calltouch_definition import CalltouchApi
  
  pp = pprint.PrettyPrinter(indent = 4)
  ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
  stats = ct.captureCalls('11/07/2017', '1', 'false', 'false', 'false', 'false')
  totalCallIDs = [i['callIDs'] for i in result]
  totalCallIDs = [y for x in totalCallIDs for y in x]
  
  saveResults = [ct.captureRecords('PasteYourNodeAddressHere', i) for i in totalCallIDs]
  pp.pprint(saveResults)
  ```
  **Входные параметры** метода *captureRecords*:
  
   - Адрес API-сервера для выбранного ранее сайта (определить можно при помощи формы в [руководстве](https://support.calltouch.ru/hc/ru/articles/209189625))
   - Идентификатор звонка в системе Calltouch
   
   **Возвращаемое значение** представляет собой словарь следующего вида:
   
   ```json
    {
      "status": "True|False",
      "message": "Сообщение о результате выполнения"
    }
   ```
   В сообщение о результате выполнения записывает либо название файла, если сохранение завершено успешно, либо код ошибки от API-сервиса.
   
## Зависимости
   
  - Python3+
  - Модули:
    - urllib
    - json
    - requests
    - BytesIO
  

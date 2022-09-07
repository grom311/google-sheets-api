# google-sheets-api

My Google sheet:
https://docs.google.com/spreadsheets/d/1Ix4EINGShspfUMEEROWe0c90kS0xGxUCYYSNYVuu8uI/edit#gid=0  
SPREADSHEET_ID=1Ix4EINGShspfUMEEROWe0c90kS0xGxUCYYSNYVuu8uI  

запускаем docker-compose.yml  
переходим по адресу: http://localhost:15433/  
настраиваем подключение к БД согласно переменным environment из docker-compose,  
это нужно сделать 1 раз при первом запуске.  
создать server:
Name - любое
Host Name - DB_PORT
Username - POSTGRES_USER
Password - POSTGRES_PASSWORD


Для отправки сообщения о просроченной доставки в телеграмм необходио:  
TOKEN: 
CHAT_ID: 
Получить токен и чат ид телеграм бота.  
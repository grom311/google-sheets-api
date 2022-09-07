# google-sheets-api

# credentials  
creds.json - файл с креденшиалами с гугл апи, нужно положить в папку app, сейчас подложены мои креды.

My Google sheet:
https://docs.google.com/spreadsheets/d/1Ix4EINGShspfUMEEROWe0c90kS0xGxUCYYSNYVuu8uI/edit#gid=0  
SPREADSHEET_ID=1Ix4EINGShspfUMEEROWe0c90kS0xGxUCYYSNYVuu8uI  

# docker-compose  
запускаем docker-compose.yml  
переходим по адресу: http://localhost:15433/  
настраиваем подключение к БД согласно переменным environment из docker-compose,  
это нужно сделать 1 раз при первом запуске.  
создать server:  
Name - любое  
Host Name - DB_PORT  
Username - POSTGRES_USER  
Password - POSTGRES_PASSWORD  

# telegram
Для отправки сообщения о просроченной доставки в телеграмм необходио:  
TOKEN:  
CHAT_ID:  
Получить токен и чат ид Вашего телеграм бота.  
Цель:
Разработать систему управления финансами с расширенными функциями для обработки транзакций
Требования:
1.	Среда разработки: 
   - Использовать Python 3.8+. 
   - Использовать Django 3.2+ и Django REST Framework 3.12+. 
   - Использовать PostgreSQL в качестве базы данных.
2.	Модели:
   - User: Представляет пользователя с полями для имени, фамилии, email и даты регистрации. 
   - Transaction: Представляет финансовую транзакцию с полями для суммы, даты, типа (доход/расход), категории и внешним ключом на модель User.
3.	API эндпоинты:
   - Пользователи:
     - GET /users/: Список всех пользователей. 
     - POST /users/: Создание нового пользователя. 
     - GET /users/{id}/: Получение информации о конкретном пользователе по ID. 
     - PUT /users/{id}/: Обновление информации о конкретном пользователе по ID. 
     - DELETE /users/{id}/: Удаление конкретного пользователя по ID. 
   - Транзакции:
     - GET /transactions/: Список всех транзакций. 
     - POST /transactions/: Создание новой транзакции. 
     - GET /transactions/{id}/: Получение информации о конкретной транзакции по ID. 
     - PUT /transactions/{id}/: Обновление информации о конкретной транзакции по ID. 
     - DELETE /transactions/{id}/: Удаление конкретной транзакции по ID.
4.	Расширенные функции (необязательно для реализации):
   - Отслеживание бюджета: Реализовать логику для отслеживания расходов по бюджетам и оповещения пользователей, когда они приближаются к лимитам бюджета. 
   - Генерация отчетов: Реализовать функциональность для создания финансовых отчетов, суммирующих транзакции за указанный период. 
   - Экспорт данных: Предоставить эндпоинты для экспорта данных транзакций и отчетов в формате CSV.
5.	Валидация:
   - Убедиться, что email пользователя является валидным. 
   - Убедиться, что сумма транзакции является положительным числом.
   - (Необязателно) Убедиться, что дата окончания бюджета следует за датой начала.
6.	Тестирование (необязательно для реализации):
   - Написать unit-тесты для моделей. 
   - Написать интеграционные тесты для API эндпоинтов. 
   - Написать тесты для расширенных функций (отслеживание бюджета, генерация отчетов, экспорт данных).
7.	Документация:
   - (Необязательно) Предоставить документацию API с использованием Django REST Framework's browsable API или Swagger. 
   - Включить подробные инструкции по настройке и запуску проекта в файл README.md.


=================
JWT: исп. 32-байтовый ключ в шестнадцетиричном формате, содержащий спецсимволы
Суперпользователь создается автоматически (логин - пароль - admin)
Установлен gunicorn для иммитации деплоя на продакшн
Список пользователей и транзакций можно просматривать, редактировать и удалять также через админку
Исп. стандартная валидация email
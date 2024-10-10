Цель:
Разработать систему управления финансами с расширенными функциями для обработки транзакций
Требования:
1.	Среда разработки:
o	Использовать Python 3.8+.
o	Использовать Django 3.2+ и Django REST Framework 3.12+.
o	Использовать PostgreSQL в качестве базы данных.
2.	Модели:
o	User: Представляет пользователя с полями для имени, фамилии, email и даты регистрации.
o	Transaction: Представляет финансовую транзакцию с полями для суммы, даты, типа (доход/расход), категории и внешним ключом на модель User.
3.	API эндпоинты:
o	Пользователи:
o	GET /users/: Список всех пользователей.
o	POST /users/: Создание нового пользователя.
o	GET /users/{id}/: Получение информации о конкретном пользователе по ID.
o	PUT /users/{id}/: Обновление информации о конкретном пользователе по ID.
o	DELETE /users/{id}/: Удаление конкретного пользователя по ID.
o	Транзакции:
o	GET /transactions/: Список всех транзакций.
o	POST /transactions/: Создание новой транзакции.
o	GET /transactions/{id}/: Получение информации о конкретной транзакции по ID.
o	PUT /transactions/{id}/: Обновление информации о конкретной транзакции по ID.
o	DELETE /transactions/{id}/: Удаление конкретной транзакции по ID.
4.	Расширенные функции (необязательно для реализации):
o	Отслеживание бюджета: Реализовать логику для отслеживания расходов по бюджетам и оповещения пользователей, когда они приближаются к лимитам бюджета.
o	Генерация отчетов: Реализовать функциональность для создания финансовых отчетов, суммирующих транзакции за указанный период.
o	Экспорт данных: Предоставить эндпоинты для экспорта данных транзакций и отчетов в формате CSV.
5.	Валидация:
o	Убедиться, что email пользователя является валидным.
o	Убедиться, что сумма транзакции является положительным числом.
o	(Необязателно) Убедиться, что дата окончания бюджета следует за датой начала.
6.	Тестирование (необязательно для реализации):
o	Написать unit-тесты для моделей.
o	Написать интеграционные тесты для API эндпоинтов.
o	Написать тесты для расширенных функций (отслеживание бюджета, генерация отчетов, экспорт данных).
7.	Документация:
o	(Необязательно) Предоставить документацию API с использованием Django REST Framework's browsable API или Swagger.
o	Включить подробные инструкции по настройке и запуску проекта в файл README.md.
=================
JWT: исп. 32-байтовый ключ в шестнадцетиричном формате, одержащиц спецсимволы 
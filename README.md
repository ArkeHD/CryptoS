# CryptoS
Проект CryptoS будет в себя включать:
  1. Архитектуру базы данных:
    Таблица users:
      id — уникальный идентификатор пользователя.
      username, email, password — (разные столбцы) данные для регистрации и аутентификации.
      balance — баланс пользователя.
      cart — корзина пользователя.
      role — роль (пользователь, разработчик, модератор).
    Таблица games:
      id — уникальный идентификатор игры.
      title, description, price — (разные столбцы) информация об игре.
      developer_id — внешний ключ (Foreign Key) для связи с разработчиком из таблицы users.
  2. Функционал веб-платформы:
    Информационный раздел
    Каталог игр с фильтрами по жанрам, ценам.
    Детальные страницы игр с описанием, скриншотами.
    Регистрация/вход.
    Корзина с возможностью оформления заказа.
    Панель разработчика
    Добавление/редактирование игр.
    Модерация (удаление игр
  3. Дополнительные возможности:
    Количество зарегистрированных пользователей.
    Безопасность.
    Хеширование паролей.
    API для интеграций.

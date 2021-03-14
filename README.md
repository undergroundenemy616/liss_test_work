# LISS test work

## Эндпойнты

- [POST] api/sign-in - регистрация

- [GET] api/posts - получить все посты
- [POST] api/posts - добавить пост
- [GET] api/post/<int:id> - получить пост по его id
- [PUT] api/post/<int:id> - изменить пост по его id
- [DELETE] api/post/<int:id> - удалить пост по его id

- [GET] api/comments - получить все комментарии
- [POST] api/comments - добавить коментарий
- [GET] api/comment/<int:id> - получить комментарий по его id
- [PUT] api/comment/<int:id> - изменить комментарий по его id
- [DELETE] api/comment/<int:id> - удалить комментарий по его id

## Как запустить проект

1. Установить виртуальное окружение командой:
    
    ```python -m venv venv```

3. Активировать виртуальное окружение командой:
    
    ```source venv/bin/activate```
    
3. Установить необходимые зависимости командой:
    
    ```pip install -r requirements.txt```
    
4. Запустить скрипт:
    
    ```sh activate.sh```

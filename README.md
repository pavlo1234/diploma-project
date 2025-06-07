
# Diploma Project

# 📘 Назва проєкту

> *Веб-сервіс для планування активного відпочинку з використанням штучного інтелекту*

---

## 👤 Автор

- **ПІБ**: Клочинський Павло Олегович
- **Група**: ФЕІ-42
- **Керівник**: Чмихало Олександр Сергійович, асистент
- **Дата виконання**: [24.05.2025]

---

## 🧠 Опис функціоналу

- Створення рекомендацій туристичних активностей за відповідним запитом користувача
- Чат з ШІ-помічником 
- Отримання даних про основні об'єкти туристичної інфраструктури (місця ночівлі, харчування, інтересу, авіаперельоти та екскурсії)

---

## 📌 Загальна інформація

- **Тип проєкту**: Вебсайт (backend-частина)
- **Мова програмування**: Python
- **Фреймворки / Бібліотеки**: FastAPI, LangChain\LangGraph

---

## 🚀  Як запустити проєкт

1. **Встановити Docker**  
   Завантажити та встановити Docker з офіційного веб-сайту:  
   👉 [https://www.docker.com/](https://www.docker.com/)

2. **Отримати Google Gemini API Key**  
   Зареєструватись та згенерувати ключ до Gemini API тут:  
   👉 [https://ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)

3. **Налаштувати змінні оточення в файлі збірки**  
   Додати `GOOGLE_API_KEY` як системну змінну в `app` секції файлу `docker-compose.yml`.

4. **Створити Docker-образ проекту**  
   ```bash
   docker-compose build
   ```

5. **Запустити контейнери**  
   ```bash
   docker-compose up
   ```

---

## 🛠️ Налаштування бази-даних

6. **Відновити MongoDB базу даних**  
   6.1. Розкрити архів:
   ```bash
   unzip database.zip
   ```  
   6.2. Скопіювати копію бази даних в MongoDB контейнер:
   ```bash
   docker cp ./database diploma_project-mongodb-1:/dump
   ```  
   6.3. Запустити термінал в MongoDB контейнері:
   ```bash
   docker exec -it diploma_project-mongodb-1 bash
   ```  
   6.4. Відновити базу даних в контейнері:
   ```bash
   mongorestore /dump
   ```

7. **Завантажити дані в векторну базу даних Qdrant**  
   7.1. Встановити необхідні Python бібліотеки:
   ```bash
   pip install qdrant-client google pymongo
   ```  
   7.2. Встановити значення змінну `GOOGLE_API_KEY` в файлі `app/scripts/qdrant_load_data.py`.  
   7.3. Запустити сценарій:
   ```bash
   python app/scripts/qdrant_load_data.py
   ```

---

## 📚 API Документація

Після успішного запуску документація доступна через Swagger за посиланням:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Travel Assistant (LLM Chat) — Тестування

1. **Встановити бібліотеку Gradio**  
   ```bash
   pip install gradio
   ```

2. **Запустити інтерфейс чату**  
   ```bash
   python app/scripts/gradio_chat.py
   ```

3. **Відкрити в браузері**  
   👉 [http://localhost:7860/](http://localhost:7860/)

## 🧪 Recommendations — Тестування

1. **Встановити бібліотеку Gradio**  
   ```bash
   pip install gradio
   ```

2. **Запустити інтерфейс чату**  
   ```bash
   python app/scripts/gradio_recommendations.py
   ```

3. **Відкрити в браузері**  
   👉 [http://localhost:7860/](http://localhost:7860/)
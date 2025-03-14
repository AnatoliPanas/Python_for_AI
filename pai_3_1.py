from google import genai
import os, random, json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
hidden_number = str(random.randint(1, 100))

# Запрос данных пользователя
user_parameters = {
    'weight': input('Введите ваш вес: '),
    'height': input('Введите ваш рост: '),
    'age': input('Введите ваш возраст: ')
}

start_message = f"""Ты специалист по здоровому питанию. Ты умеешь составлять меню на день
исходя из возраста, роста и веса. 
Вот параметры пользователя:
{'\n'.join(f"{key}: {value}" for key, value in user_parameters.items())}""" + \
                """Ответ на сообщение пользователя структурируй следующим образом:
                {
                    "day_menu": "в этом поле распиши меню на день (str)",
                    "user_parameters": {
                        "weight": вес либо из ранее предоставленных данных, либо согласно новым данным от пользователя,
                        "height": высота либо из ранее предоставленных данных, либо согласно новым данным от пользователя,
                        "age": возраст либо из ранее предоставленных данных, либо согласно новым данным от пользователя,
                    }
                }
                Убедись, что в ответ ты передаешь только валидный JSON
                """

messages = [f'System: {start_message}']

# Получение ответа от модели
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=messages
)

while True:
    try:
        # Выводим ответ от API для диагностики
        print(f"Ответ от API: {response.text}")  # Это поможет нам увидеть сам ответ

        # Убираем пробелы и символы новой строки с начала и конца ответа
        cleaned_response = response.text.strip()

        # Проверяем, что ответ не пустой
        if not cleaned_response:
            print("Ответ от API пустой.")
            break

        # Парсим очищенный JSON-ответ
        data = json.loads(cleaned_response)

        # Проверяем, что в ответе есть нужные данные
        if "day_menu" in data and "user_parameters" in data:
            day_menu = data.get('day_menu')
            user_parameters = data.get('user_parameters')

            # Выводим меню на день
            if day_menu:
                print(day_menu)
            else:
                print("Меню на день не было предоставлено.")
                break

            # Проверяем, если обновились параметры пользователя
            if user_parameters:
                print(f"Обновленные параметры пользователя: {json.dumps(user_parameters, indent=2)}")
        else:
            print("Ответ от API не содержит ожидаемых данных (day_menu или user_parameters).")
            break

        # Запрос изменений от пользователя
        user_input = input("Введите ваши изменения (или нажмите Enter для завершения): ")

        # Если пользователь не вводит данных, выходим из цикла
        if not user_input:
            print("Завершаем программу.")
            break

        # Добавляем новое сообщение от пользователя
        messages.append(f'Agent: {response.text}')
        messages.append(f'User: {user_input}')

        # Получаем новый ответ от модели
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=messages
        )

    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON: {e}")
        break
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        break

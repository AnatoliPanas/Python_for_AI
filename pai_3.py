# загадываете число через модуль random
# после этого показываете число иишке - себе не показываете
# затем идёт процесс отгадывания - вы ему число, а он вам в стихотворной форме рассказывает насколько горячо или холодно


from google import genai
import os, random
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Создание клиента API
client = genai.Client(api_key=api_key)

hidden_number = str(random.randint(1,100))
satrt_message = f"""Мы с тобой сыграем в игру, ты загадал число {hidden_number}.
Моя задача - отгадать это число. Твоя задача - либо сказать "Победа", если я отгадал число, либо
написать четверостишие, о том, "горячо" или "холодно" если названное мной число близко к загаданному - "горячо"
иначе - "холодно" 
User: {input("Введите вашу попытку: ")}"""

messages = [f"System: {satrt_message}"]
# Отправка запроса к модели
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=messages
)
# Вывод ответа
while response.text.strip().capitalize() != "Победа":
    print(response.text)
    messages.append(f"Agent: {response.text}")
    messages.append(f"User: {input("Введите вашу попытку: ")}")
    # Отправка запроса к модели
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=messages)

print(response.text)
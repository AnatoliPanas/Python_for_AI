import time
from google import genai
from dotenv import load_dotenv
import os
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
import requests

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

def handle_rate_limit_error(e):
    """
    Обработчик ошибки, если API вернуло превышение лимита запросов.
    """
    if isinstance(e, requests.exceptions.HTTPError):
        if e.response.status_code == 429:
            print("Превышен лимит скорости, повторная попытка")
            return True
    return False

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3), retry=handle_rate_limit_error)
def get_gemini_response(prompt):
    """
    Отправляет запрос к модели Gemini и возвращает текст ответа.

    :param prompt: Текст запроса.
    :return: Текст ответа модели.
    """
    time.sleep(0.3)  # Небольшая задержка перед отправкой запроса (можно убрать или изменить)

    # Используем глобальный объект клиента
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt],
        )
        return response.text
    except requests.exceptions.Timeout:
        print("Время ожидания запроса истекло.")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Запрос не выполнен: {e}.")
        raise


# Пример использования
if __name__ == "__main__":
    try:
        response = get_gemini_response("Что такое лимиты запросов?")
        print(response)
    except RetryError:
        print("Достигнуто максимальное количество попыток. Пожалуйста, повторите попытку позже.")
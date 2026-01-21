import smtplib
import ssl

# Ваши данные
sender_email = "schattencheg_dev@mail.ru"
password = "RGblu3K1yL8iKibJf7wE"
receiver_email = "schattencheg@gmail.com"
subject = "Тема письма"
body = "Тело вашего письма на Python"

# Настройки SMTP
smtp_server = "smtp.mail.ru"
port = 465  # Для SSL, порт 587 для TLS

# Создаем защищенное соединение
context = ssl.create_default_context()

try:
    # Подключаемся к серверу
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # Формируем сообщение
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
        print("Письмо успешно отправлено!")
except Exception as e:
    print(f"Произошла ошибка: {e}")

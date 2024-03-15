import datetime
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import ssl


alarm_hour = 7
alarm_minute = 0


email_user = "l2628787@fastmail.com"
email_pass = "ha2hjhvkcryqfzkd"
recipient_email ="l2628787@gmail.com"


weather_url = 'https://www.met.ie/dublin-forecast.html'


def get_weather_from_web():

    page = requests.get(weather_url)
    soup = BeautifulSoup(page.content, 'html.parser')


    weather_div = soup.find('section', id='National-Forecast-Map')
    for p in weather_div.find_all('p'):
        if not "Issued at" in p.text:
            return(p.text)


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient_email
    server = "smtp.fastmail.com"
    port = 465
    message = f"""From: {email_user}
To: {recipient_email}
{body}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(server, port, context=context) as server:
        server.set_debuglevel(1)
        server.login(email_user, email_pass)
        server.sendmail(email_user, recipient_email, message)


def play_alarm():
    os.system('mpg123 /home/pi/Leo/static/audio/warningvoice.mp3')

weather_info = (get_weather_from_web())
send_email("weather",weather_info)

weather_info = (get_weather_from_web())
send_email("Weather", weather_info)


while True:
    now = datetime.datetime.now()
    if now.hour == alarm_hour and now.minute == alarm_minute:
        play_alarm()
        weather_info = get_weather_from_web()
        send_email("Today's Weather", weather_info)
        print("Weather email sent.")
        time.sleep(60)
    time.sleep(10)
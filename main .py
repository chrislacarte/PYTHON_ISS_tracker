import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "c.lacarte0909@gmail.com"
MY_PASSWORD = "28102810Aa."

MY_LAT = 52.205338 # Your latitude
MY_LONG = 0.121817 # Your longitude


def is_iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    if response.status_code == 404:
        raise Exception("That resource does not exist")
    elif response.status_code == 401:
        raise Exception("You are not authorised to access this data")

    data = response.json()
    iss_longitude = float(data["iss_position"]['longitude'])
    iss_latitude = float(data["iss_position"]["latitude"])
    #if your position is +/- 5 degrees from Iss location :
    if MY_LAT-5  <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def isd_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data['results']['sunset'].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and isd_night():
        connection = smtplib.SMPT("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr= MY_EMAIL,
            to_addrs= "chrislacarte@icloud.com",
            msg="Subject=Look UP !!\n\n The Iss is above you ! "
        )

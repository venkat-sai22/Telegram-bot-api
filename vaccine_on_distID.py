import requests
from datetime import datetime, timedelta
import time
import pytz

#Define all the constants
time_interval = 20 # (in seconds) Specify the frequency of code execution
DISTRICTID="512"
msg = "Blank"
tele_auth_token = "5570999103:AAFYPT2o0A27JTCJP17AlLNfgaeYHslEFMM"  # Authentication token provided by Telegram bot
tel_group_id = "vaccine_aroundme"     # Telegram group name
IST = pytz.timezone('Asia/Kolkata')        # Indian Standard Time - Timezone
slot_found =  False                        # Intial slot found status
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
def update_timestamp_send_Request(PINCODE):
 raw_TS = datetime.now(IST) + timedelta(days=1)      # Tomorrows date
 tomorrow_date = raw_TS.strftime("%d-%m-%Y")         # Formatted Tomorrow's date
 today_date = datetime.now(IST).strftime("%d-%m-%Y") #Current Date
 curr_time = (datetime.now().strftime("%H:%M:%S"))   #Current time
 request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DISTRICTID}&date={tomorrow_date}"

 response = requests.get(request_link, headers = header)
 raw_JSON = response.json()
 return raw_JSON, today_date, curr_time
def get_availability_45(age = 45):
 raw_JSON, today_date, curr_time = update_timestamp_send_Request(DISTRICTID)
 for cent in raw_JSON['centers']:
     for sess in cent["sessions"]:
         sess_date = sess['date']
         if sess["min_age_limit"] == age and sess["available_capacity"] > 0:
             slot_found =  True
             msg = f"""For age 45+ [Vaccine Available] at {DISTRICTID} on {sess_date}\n\tState : {cent["state_name"]}\n\t  DISTRICT:{cent["district_name"]}\n\tCenter : {cent["name"]}\n\t  Vaccine: {sess["vaccine"]}\n\tDose_1: {sess["available_capacity_dose1"]}\n\tDose_2: {sess["available_capacity_dose2"]}"""
             send_msg_on_telegram(msg)
             print (f"INFO:[{curr_time}] Vaccine Found for 45+ at {DISTRICTID}")
 else:
     slot_found =  False
     print (f"INFO: [{today_date}-{curr_time}] Vaccine NOT-Found for 45+ at {DISTRICTID}")
def get_availability_18(age = 18):
 raw_JSON, today_date, curr_time = update_timestamp_send_Request(DISTRICTID)
 for cent in raw_JSON['centers']:
     for sess in cent["sessions"]:
         sess_date = sess['date']
         if sess["min_age_limit"] == age and sess["available_capacity"] > 0:
             slot_found =  True
             msg = f"""For age 18+ [Vaccine Available] at {DISTRICTID} on {sess_date}\n\tState : {cent["state_name"]}\n\t  DISTRICT:{cent["district_name"]}\n\tCenter : {cent["name"]}\n\t  Vaccine: {sess["vaccine"]}\n\tDose_1: {sess["available_capacity_dose1"]}\n\tDose_2: {sess["available_capacity_dose2"]}"""
             send_msg_on_telegram(msg)
             print (f"INFO: [{curr_time}] Vaccine Found for 18+ at {DISTRICTID}")
 else:
     slot_found =  False
     print (f"INFO: [{today_date}-{curr_time}] Vaccine NOT Found for 18+ at {DISTRICTID}")

def send_msg_on_telegram(msg):
 telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendMessage?chat_id=@{tel_group_id}&text={msg}"
 tel_resp = requests.get(telegram_api_url)
 if (tel_resp.status_code == 200):
  print ("Notification has been sent on Telegram")
 else:
  print ("Could not send Message")

if __name__ == "__main__":
     while True:
         get_availability_45()
         get_availability_18()
         time.sleep(time_interval)
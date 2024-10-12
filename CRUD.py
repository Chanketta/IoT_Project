import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "11h-7ds4RkssFfyq3AcVaIr2FlXpwJDRDcn-eVLE4-ZQ"
workbook= client.open_by_key(sheet_id)
data = workbook.sheet1.get_all_values()
def display_all():
    for row in data:
        print(row)
        
def add_row(newTemp, newHumidity, newMoisture, newWaterTank, newStatus):
    now = datetime.now()
    newDate = now.strftime("%Y-%m-%d")
    newTime = now.strftime("%H:%M:%S")
    workbook.sheet1.append_row([newDate, newTime, newTemp, newHumidity, newMoisture, newWaterTank, newStatus])
    print(">>>Row added succesfully!")


cached_graphs_data = None
last_fetch_time = 0
data_cache_duration = 600  

def get_graphs_data(dataType):
    global cached_graphs_data, last_fetch_time
    
    if cached_graphs_data and time.time() - last_fetch_time < data_cache_duration:
        print("Returning cached data.")
        return cached_graphs_data
    
    print("Fetching new data from Google Sheets.")
   
    humidity30 = []
    soilmoisture30 = []
    temperature30 = []
    if dataType == "temperature":
        temperature30 = []
        for i in range(2, 12):
            data = workbook.sheet1.cell(i, 3).value
            temperature30.append(data)
        cached_graphs_data = temperature30
        last_fetch_time = time.time()
        return temperature30
    if dataType == "humidity":
        humidity30 = []
        for i in range(2, 12):
            data = workbook.sheet1.cell(i, 4).value
            humidity30.append(data)
        cached_graphs_data = humidity30
        last_fetch_time = time.time()
        return humidity30
    if dataType == "soilmoisture":
        soilmoisture30 = []
        for i in range(2, 12):
            data = workbook.sheet1.cell(i, 5).value
            soilmoisture30.append(data)
        cached_graphs_data = soilmoisture30
        last_fetch_time = time.time()
        return soilmoisture30
   
def get_data():
    data = workbook.sheet1.row_values(2)
    return data
def get_relay_status():
    relay_status = workbook.sheet1.cell(1, 10).value  
    return relay_status
def get_row1():
    data = workbook.sheet1.row_values(1)
    return data
    
def update_user_schedule(schedule_list):
    if (len(schedule_list) != 0):
        for i in range (0, 4):
            if schedule_list[i] != "Empty":
                workbook.sheet1.update_cell(1, 23 + i, schedule_list[i])  
            else:
                workbook.sheet1.update_cell(1, 23 + i, "Empty")
    else:
        for i in range (0, 4):
            workbook.sheet1.update_cell(1, 23 + i, "Empty")
            print("Schedule updated in Google Sheet successfully!")

def toggle_relay_switch(status):
    workbook.sheet1.update_cell(1, 10, status)  
    return status
def save_user_notification_setting(humidity_range, temperature_range, soil_moisture_range, water_tank_level_range):
    workbook.sheet1.update_cell(1, 15, f"{humidity_range[0]}-{humidity_range[1]}")
    workbook.sheet1.update_cell(1, 17, f"{temperature_range[0]}-{temperature_range[1]}") 
    workbook.sheet1.update_cell(1, 19, f"{soil_moisture_range[0]}-{soil_moisture_range[1]}")
    workbook.sheet1.update_cell(1, 21, f"{water_tank_level_range[0]}-{water_tank_level_range[1]}")

def search_date(searchDate):
    matched_rows = []
    timeStampFound = False
    for row in data:
        if row[0] == searchDate:  # Assuming Date is in column A
            matched_rows.append(row)
    if matched_rows:
        for row in matched_rows:
            print(row)
        choice = input("Would you like to find the exact timestamp?(y/n): ")
        if choice == 'y':
            searchTimestamp = input("Enter timestamp(hh:mm:ss): ")
            for timeStamp in matched_rows:
                if timeStamp[1] == searchTimestamp:
                    print(f">>>Matched timestamp found! {timeStamp} ")
                    timeStampFound = True
                    break
            if timeStampFound:
                pass
            else:
                return ">>>Unable to find it!"
        else:
            return ">>>Skipped searching for timestamp!"
    else:
        print(f">>>No entries found for {searchDate}!")
              
    
def update_row(row_number, newDate, newTime, newTemp, newHumidity, newMoisture, newWaterTank, newStatus):
    workbook.sheet1.update_acell(f'A{row_number}', newDate)
    workbook.sheet1.update_acell(f'B{row_number}', newTime)
    workbook.sheet1.update_acell(f'C{row_number}', newTemp)
    workbook.sheet1.update_acell(f'D{row_number}', newHumidity)
    workbook.sheet1.update_acell(f'E{row_number}', newMoisture)
    workbook.sheet1.update_acell(f'F{row_number}', newWaterTank)
    workbook.sheet1.update_acell(f'G{row_number}', newStatus)
    print(f">>>Row #{row_number} updated successfully!")

def delete_row(row_number):
    workbook.sheet1.delete_rows(row_number)
    print(f">>>Row #{row_number} deleted successfully!")




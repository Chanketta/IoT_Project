import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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

def get_temperature_data_30():
    temperature30 = []
    for i in range(2,32):
        data = workbook.sheet1.cell(i, 3).value
        if data:
            temperature30.append(float(data))
    return temperature30

def get_humidity_data_30():
    humidity30 = []
    for i in range(2,32):
        data = workbook.sheet1.cell(i, 4).value
        if data:
            humidity30.append(float(data))
    return humidity30

def get_soilmoisture_data_30():
    soilmoisture30 = []
    print("hi")
    for i in range(2,32):
        data = workbook.sheet1.cell(i, 5).value
        print(data)
        if data:
            soilmoisture30.append(float(data))
    return soilmoisture30

def get_water_tank_level_data_30():
    watertank30 = []
    for i in range(2,32):
        data = workbook.sheet1.cell(i, 7).value
        if data:
            watertank30.append(float(data))
    return watertank30

arr1 = get_soilmoisture_data_30()
print(arr1)

def get_data():
    data = workbook.sheet1.row_values(2)
    return data
def get_settings():
    data = workbook.sheet1.row_values(1)
    return data
def get_relay_status():
    relay_status = workbook.sheet1.cell(1, 10).value  
    return relay_status

# Toggle relay switch (e.g., turn ON/OFF)
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




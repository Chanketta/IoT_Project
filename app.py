from flet import *
import CRUD
import asyncio
import requests
import time
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import numpy as np
from datetime import datetime
import time


def main(page: Page):    
    page.window.width = 420
    page.window.height = 860
    global BACKGROUND, INK, CONTAINER, FONT
    #light_theme():       
    LT1 = "#FEF3E2"
    LT2 = "#BEC6A0"        
    LT3 = "#708871"
    LT4 = "#606676"
    #dark_theme():
    DT1 = "#606676"
    DT2 = "#6B8A7A"
    DT3 = "#B7B597"
    DT4 = "#DAD3BE"
    BACKGROUND = LT3
    INK = LT2
    CONTAINER = LT1
    FONT = DT4

   

    page.window.bgcolor = 'Black'

    API_TOKEN = "aoytq6n6vm8h3qgxf1pc17vveftjm7"
    USER_KEY = "uro2vbsnxrb8vkjaxq8aatvt78h78s"
 
    NOTIFICATION_COOLDOWN = 3600  
    last_notification_time = {
    "battery": 0,
    "humidity": 0,
    "temperature": 0,
    "soil_moisture": 0,
    "water_tank": 0
    }

    def send_notification(title, body):
        """Sends a notification via Pushover using HTTP requests"""
        url = "https://api.pushover.net/1/messages.json"
        data = {
            "token": API_TOKEN,
            "user": USER_KEY,
            "title": title,
            "message": body
        }
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("Notification sent successfully!")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.text}")

    def can_send_notification(sensor_name):
        """Checks if a notification can be sent based on the cooldown"""
        current_time = time.time()
        if current_time - last_notification_time[sensor_name] > NOTIFICATION_COOLDOWN:
            last_notification_time[sensor_name] = current_time  
            print(f"Can send notification for {sensor_name}.")
            return True
        else:
            print(f"Cannot send notification for {sensor_name}, cooldown active.")
        return False

    def check_datas_and_notify():
        data = CRUD.get_data()
        temperature = float(data[2])
        humidity = float(data[3])
        soil_moisture = float(data[4])
        water_tank_level = float(data[6])
        battery_voltage = float(data[7])
        humidity_range = user_settings["humidity_range"]
        if not float(humidity_range[0]) <= humidity <= float(humidity_range[1]):
            if can_send_notification("humidity"):
                send_notification("Humidity Alert", f"Humidity is out of range: {humidity}%")
        
        temperature_range = user_settings["temperature_range"]
        if not float(temperature_range[0]) <= temperature <= float(temperature_range[1]):
            if can_send_notification("temperature"):
                send_notification("Temperature Alert", f"Temperature is out of range: {temperature} °C")
        

        soil_moisture_range = user_settings["soil_moisture_range"]
        if not float(soil_moisture_range[0]) <= soil_moisture <= float(soil_moisture_range[1]):
            if can_send_notification("soil_moisture"):
                send_notification("Soil Moisture Alert", f"Soil moisture is out of range: {soil_moisture}%")
        
        water_tank_level_range = user_settings["water_tank_level_range"]
        if not float(water_tank_level_range[0]) <= water_tank_level <= float(water_tank_level_range[1]):
            if can_send_notification("water_tank"):
                send_notification("Water Tank Level Alert", f"Water Tank level is out of range: {water_tank_level}%")
        if battery_voltage < 5:  
            if can_send_notification("battery"):
                send_notification("Low Battery Alert", "Battery voltage is low, please check the system.")

    menu_option = Row(
        alignment='center',  # Center align
        wrap = True,
        spacing= 50,  # space between the boxes
    )
    
    options = ['Temperature', 'Humidity', 'Soil Moisture', 'Health Status', 'Water Tank Level', 'Relay\'s battery']
    
    for option in options:
        menu_option.controls.append(
            Container(
                border_radius=20,
                border=border.all(5, color = CONTAINER),
                bgcolor = CONTAINER,
                height=150,  
                width=150,   
                alignment=alignment.center,  
                content=Text(value=option, color= BACKGROUND, size=12, text_align='center'),
            )
        )
    first_page_contents = Column(
        height = 150,
        width = 350,
        controls=[
            Row(
                alignment='START',
                controls=[
                    Container(content = Icon(name = 'SETTINGS', color = CONTAINER), on_click=lambda _: page.go('/settings')),
                    Container(content = Icon(name = 'BAR_CHART', color= CONTAINER), on_click=lambda _: page.go('/graphs')), 
                    Container(content = Icon(name = 'ACCESS_ALARM_OUTLINED', color = CONTAINER), on_click=lambda _: page.go('/schedule')),
                ],
            ),
            Container(height = 10),
            Text(value="WELCOME BACK!", color = FONT, size=35, weight = 'bold'),
            Text(value="Last Updated Statuses:", color = FONT, size = 18, italic=True),
        ],
    )
    
  

    def update_homepage(page, data):
        Date, Time, Temperature, Humidity, SoilMoisture, HealthStatus, WaterTankLevel, RelayBattery = data
        menu_option.controls[0].content = Text(f"Temperature: \n {Temperature} °C", color=BACKGROUND, size=18, weight='bold', text_align='center')
        menu_option.controls[1].content = Text(f"Humidity: \n {Humidity}%", color=BACKGROUND, size=18, weight='bold', text_align='center')
        menu_option.controls[2].content = Text(f"Soil Moisture: \n{SoilMoisture}%", color=BACKGROUND, size=18, weight='bold', text_align='center')
        menu_option.controls[3].content = Text(f"Health Status: \n{HealthStatus}", color=BACKGROUND, size=18, weight='bold', text_align='center')
        menu_option.controls[4].content = Text(f"Water Tank Level: \n{WaterTankLevel}%", color=BACKGROUND, size=18, weight='bold', text_align='center')
        menu_option.controls[5].content = Text(f"Relay's Battery: \n{RelayBattery}%", color=BACKGROUND, size=18, weight='bold', text_align='center')
        page.update() 

    def toggle_relay(e = None):
        print("Switcing relay...")
        current_status = CRUD.get_relay_status()
        new_status = "OFF" if current_status == "ON" else "ON"
        CRUD.toggle_relay_switch(new_status)
        update_homepage(page, CRUD.get_data())

    # Home page 
    home_page = Container(
        width=450,
        height=800,
        bgcolor= BACKGROUND,
        border_radius=10,
        padding = padding.only(left = 15, right = 15, top = 15, bottom = 15),
        content=Column(
            controls=[
                first_page_contents,
                menu_option,
                Container(height = 20),
                Text(value = 'Manual Control: ', color= FONT, size = 18, italic=True),
                Row(
                    controls=[
                        Text("Relay's Status", color= FONT, size = 15, weight = 'bold'),  
                        Switch(
                            value=CRUD.get_relay_status(),
                            on_change=toggle_relay,  
                            ),
                        ]
                ),
            ],
        ),
    )

#Setting page and widgets
    data = CRUD.get_row1()
    user_settings = {"humidity_range": data[14].split("-"),  
                     "temperature_range": data[16].split("-"),  
                     "soil_moisture_range": data[18].split("-"),
                     "water_tank_level_range": data[20].split("-"),}
    
    humidity_slider = RangeSlider(
        min = 0,
        max = 100,
        divisions=10,
        start_value = user_settings["humidity_range"][0],
        end_value = user_settings["humidity_range"][1],
        inactive_color = BACKGROUND,
        active_color = FONT,
        overlay_color = colors.GREEN_200,
        label = "{value}%",
    )
    temperature_slider = RangeSlider(
        min = 0,
        max = 50,
        divisions=25,
        start_value = user_settings["temperature_range"][0],
        end_value = user_settings["temperature_range"][1], 
        inactive_color = BACKGROUND,
        active_color = FONT,
        overlay_color = colors.GREEN_200,
        label = "{value} C",
    )
    soilmoisture_slider = RangeSlider(
        min = 0,
        max = 100,
        divisions=10,
        start_value = user_settings["soil_moisture_range"][0],
        end_value = user_settings["soil_moisture_range"][1],
        inactive_color = BACKGROUND,
        active_color = FONT,
        overlay_color = colors.GREEN_200,
        label = "{value}%",
    )
    watertanklevel_slider = RangeSlider(
        min = 0,
        max = 100,
        divisions=10,
        start_value = user_settings["water_tank_level_range"][0],
        end_value = user_settings["water_tank_level_range"][1],
        inactive_color = BACKGROUND,
        active_color = FONT,
        overlay_color = colors.GREEN_200,
        label = "{value}%",
    )
   
    saved_label = Text("Settings Saved!", color=FONT, size=12, visible = False) 

    async def save_rangers():
        user_settings["humidity_range"] = (humidity_slider.start_value, humidity_slider.end_value)
        user_settings["temperature_range"] = (temperature_slider.start_value, temperature_slider.end_value)
        user_settings["soil_moisture_range"] = (soilmoisture_slider.start_value, soilmoisture_slider.end_value)
        user_settings["water_tank_level_range"] = (watertanklevel_slider.start_value, watertanklevel_slider.end_value)
        
        CRUD.save_user_notification_setting( 
            humidity_range = user_settings["humidity_range"],
            temperature_range = user_settings["temperature_range"],
            soil_moisture_range = user_settings["soil_moisture_range"],
            water_tank_level_range = user_settings["water_tank_level_range"])
        
        print(f"Settings saved: {user_settings}")

        saved_label.visible = True
        page.update()
        await asyncio.sleep(2)
        saved_label.visible = False
        page.update()

    save_icon = Container(
        content=Icon(name="SAVE_ALT_OUTLINED", color=CONTAINER),
        on_click=lambda _: asyncio.run(save_rangers()) 
    )

    settings_page = Container(
        width=400,
        height=800,
        bgcolor= BACKGROUND,
        border_radius=10,
        padding = padding.only(left = 15, right = 15, top = 15, bottom = 15),
        content = Column(
            controls=[
                Container(content = Icon(name = 'HOME', color = CONTAINER), on_click=lambda _: page.go('/')),
                Text('SETTING:', color=FONT, size=35, weight = 'bold'),
                Container(height=30),
                Row(
                    alignment = 'START',
                    controls = [
                    Text(value="Save Setting:", color=FONT, size=18, weight='bold'),
                    save_icon,
                    saved_label,
                    ]
                ),
                Text('Notify me when: ', color = FONT, size = 25, italic = True),
                Container(height = 15),
                Container(
                    bgcolor = "GREY",
                    padding = 10,
                    border_radius = 10,
                    height = 400,
                    content= Column(
                        controls=[
                            Text('  When humidity is not in between: ', size = 15, color = colors.GREY_800, weight='bold'),
                            humidity_slider,
                            Text('  When temperature is not in between: ', size = 15, color = colors.GREY_800, weight='bold'),
                            temperature_slider,
                            Text('  When soil moisture level is not in between: ', size = 15, color = colors.GREY_800, weight='bold'),
                            soilmoisture_slider,
                            Text('  When water tank level is not in between: ', size = 15, color = colors.GREY_800, weight='bold'),
                            watertanklevel_slider,
                        ],
                    ),
                ),
            ],
        )
    )

#Graphs page and widget  
    generating_label = Text("Generating...", color=FONT, size=12, italic = True, visible = False) 
    graphs_container = Container(height = 300, bgcolor = INK) 
    def create_temperature_chart():
        temperatureData = CRUD.get_graphs_data("temperature")
        
        fig, ax = plt.subplots()
        x = np.arange(1, len(temperatureData) + 1)

        ax.plot(x, temperatureData, label='Temperature (°C)', color=INK, linestyle='-', marker='o')

        ax.set_facecolor(CONTAINER)  # Light grey background
        ax.set_xlabel("Data Points", fontsize=12, fontweight='bold')
        ax.set_ylabel("Values", fontsize=12, fontweight='bold')
        ax.set_title("Sensor Data (Last 10 Readings)", fontsize=14, fontweight='bold')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend(loc='upper right', fontsize=10)

        # Tweak axis ticks and font size
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        fig.tight_layout()

        return MatplotlibChart(fig, expand=True)
    def create_humidity_chart():
            humidityData = CRUD.get_graphs_data("humidity")
            fig, ax = plt.subplots()
            x = np.arange(1, len(humidityData) + 1)

            ax.plot(x, humidityData, label='Humidity (%)', color=INK, linestyle='-', marker='^')

            ax.set_facecolor(CONTAINER)  
            ax.set_xlabel("Data Points", fontsize=12, fontweight='bold')
            ax.set_ylabel("Values", fontsize=12, fontweight='bold')
            ax.set_title("Sensor Data (Last 10 Readings)", fontsize=14, fontweight='bold')

            ax.grid(True, which='both', linestyle='--', linewidth=0.5)
            ax.legend(loc='upper right', fontsize=10)

            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)

            fig.tight_layout()

            return MatplotlibChart(fig, expand=True)
    def create_soilmoisture_chart():
            soilmoistureData = CRUD.get_graphs_data("soilmoisture")
            fig, ax = plt.subplots()
            x = np.arange(1, len(soilmoistureData) + 1)

            ax.plot(x, soilmoistureData, label='Soil Moisture (%)', color=INK, linestyle='-', marker='s')

            ax.set_facecolor(CONTAINER)  # Light grey background
            ax.set_xlabel("Data Points", fontsize=12, fontweight='bold')
            ax.set_ylabel("Values", fontsize=12, fontweight='bold')
            ax.set_title("Sensor Data (Last 10 Readings)", fontsize=14, fontweight='bold')

            ax.grid(True, which='both', linestyle='--', linewidth=0.5)
            ax.legend(loc='upper right', fontsize=10)

            # Tweak axis ticks and font size
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)

            fig.tight_layout()

            return MatplotlibChart(fig, expand=True)

    def generate_new_graphs(dataType):
        generating_label.visible = True
        page.update()
        
        if dataType == "temperature":
            graphs_container.content = create_temperature_chart()
        if dataType == "humidity":
            graphs_container.content = create_humidity_chart()
        if dataType == "soil_moisture":
            graphs_container.content = create_soilmoisture_chart()
        generating_label.visible = False
        page.update()

    graphs_page = Container(
        width=400,
        height=800,
        bgcolor= BACKGROUND,
        border_radius=10,
        padding = padding.only(left = 15, right = 15, top = 15, bottom = 15),
        content = Column(
            controls=[
                Container(content = Icon(name = 'HOME', color= CONTAINER ), on_click=lambda _: page.go('/')),
                Container(height = 15),
                Text("GRAPHS:", color = FONT, size = 35, weight = 'bold'),
                Text("What would you like to see?", color = FONT, size = 18, italic = True),
                generating_label,
                Container(
                    content=Row(
                        [
                            Icon(name="get_app", color=FONT, size=30),
                            Text("Temperature Graphs:", color= BACKGROUND, size=18, weight='bold', text_align='center'), 
                        ],
                        spacing = 50,
                        alignment = "Center",
                    ),
                    on_click=lambda _: generate_new_graphs("temperature"),
                    border_radius=20,
                    bgcolor=CONTAINER,
                    height=50,
                    width=350,
                    alignment=alignment.center,  # Centers the entire container itself
                    padding=5,
                    ink = True
                ),
                 Container(
                    content=Row(
                        [
                            Icon(name="get_app", color=FONT, size=30),
                            Text("  Humidity Graphs:", color=BACKGROUND, size=18, weight='bold', text_align='center'), 
                        ],
                        spacing = 72,
                        alignment = "Center",
                    ),
                    on_click=lambda _: generate_new_graphs("humidity"),
                    border_radius=20,
                    bgcolor=CONTAINER,
                    height=50,
                    width=350,
                    alignment=alignment.center,  
                    padding=5,
                    ink = True
                ),
                 Container(
                    content=Row(
                        [
                            Icon(name="get_app", color=FONT, size=30),
                            Text("Soil Moisture Graphs:", color=BACKGROUND, size=18, weight='bold', text_align='center'), 
                        ],
                        spacing = 50,
                        alignment = "Center",
                    ),
                    on_click=lambda _: generate_new_graphs("soil_moisture"),
                    border_radius=20,
                    bgcolor= CONTAINER,
                    height=50,
                    width=350,
                    alignment=alignment.center,  
                    padding=5,
                    ink = True
                ),
                Container(height=40),
                graphs_container,
            ],
        ),
    )


#Schedule page and widgets
    def get_schedule():
        list = []
        data = CRUD.get_row1()
        list.insert(0, data[22])
        list.insert(1, data[23])
        list.insert(2, data[24])
        list.insert(3, data[25])
        return list
    global schedul_list
    schedule_list = get_schedule()

    schedule_display = Column()
    def update_schedule_list(schedule_list):
        schedule_display.controls.clear()
        i = 1
        for time in schedule_list:
            schedule_display.controls.append(Text(f"    Scheduled Time[{i}]: {time}", color=BACKGROUND, weight = 'bold'))
            i = i + 1
        CRUD.update_user_schedule(schedule_list)
        page.update()
        print("Schedule updated in flet successfully!")

    schedule_container = Container(
        content = schedule_display,
        bgcolor = FONT,
        padding = 10,
        border_radius = 10,
        width = 355,
    )
    def handle_change(e):
        Slot = False
        selected_time = time_picker.value.strftime("%H:%M")
        print(selected_time)
        print(f"You have selected {selected_time}")
        for i in range(0,4):  
            if schedule_list[i] == "Empty": 
                schedule_list[i] = str(selected_time) 
                Slot = True
                break                     
        if Slot == False:
            print("Maximum 4 timers allowed or no time selected.")
        else:
            update_schedule_list(schedule_list)  
            print("Timer added successfully!")

    def handle_dismissal(e):
        print(f"TimePicker dismissed: {time_picker.value}")
    def handle_entry_mode_change(e):
        print(f"TimePicker Entry mode changed to {e.entry_mode}")
    
    time_picker = TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change = handle_change,
        on_dismiss = handle_dismissal,
        on_entry_mode_change = handle_entry_mode_change,
    )
     
    def add_timer():
        page.open(time_picker)
        page.update()

    def delete_timer(index):
        if schedule_list[index] != "Empty":
            if index == 3:
                schedule_list[index] = "Empty"  
                print(f"Deleted Timer {index}")
            else:
                for i in range(index, 3):
                    schedule_list[i] = schedule_list[i + 1]
                schedule_list[3] = "Empty"
            
            update_schedule_list(schedule_list) 
        else:
            print("No timer found at this index to delete.")

    dropdown_edit_menu = Dropdown(
            label="Edit Schedule",
            options=[
                dropdown.Option("Add Timer"),
                dropdown.Option("Delete Timer"),
            ],
         on_change=lambda e: handle_schedule_action(e),  
    )
    def get_timer_options():
        return [dropdown.Option(f"Index {i+1}") for i in range(len(schedule_list))]

    dropdown_delete_menu = Dropdown(
        label="Select Timer to Delete",
        options=get_timer_options(),
        on_change=lambda e: handle_delete_dropdown(e),
        visible = False,
    )

    def handle_delete_dropdown(e):
        selected_index = e.control.value  
        if selected_index:
            index = int(selected_index.split()[-1]) - 1  
            delete_timer(index)

    def handle_schedule_action(e):
        selected_action = dropdown_edit_menu.value
        if selected_action == "Add Timer":
            add_timer()
            page.update()
            page.add(Text("Select a time for the timer"))
        elif selected_action == "Delete Timer":
            dropdown_delete_menu.visible = True
            dropdown_delete_menu.options = get_timer_options()
        update_schedule_list(schedule_list)  
    #initializing schedule_page    
    update_schedule_list(schedule_list)
    CRUD.update_user_schedule(schedule_list)      
    schedule_page = Container(
        width=400,
        height=800,
        bgcolor=BACKGROUND,
        border_radius=10,
        padding=padding.only(left=15, right=15, top=15, bottom=15),
        content=Column(
            controls=[
                Container(content = Icon(name = 'HOME', color= CONTAINER ), on_click=lambda _: page.go('/')),
                Container(height = 15),
                Text("SCHEDULE:", size=35, color=FONT, weight = 'bold'),
                Text("Current Schedule:", size=20, color=FONT, italic = True),
                schedule_container,
                dropdown_edit_menu,
                dropdown_delete_menu,
            ],
            
        ),
    )

    
    async def check_schedule():
        while True:
            current_time = datetime.now().strftime("%H:%M")
            for schedule_time in schedule_list:
                if schedule_time == current_time:
                    toggle_relay()  # Turn on the relay
                    print(f"Relay turned ON at {current_time}")
                    await asyncio.sleep(5)
                    toggle_relay() 

            await asyncio.sleep(60)  # Check every minute

    
    async def periodic_update():
        while True:
            print("Fetching latest data and updating...")
            update_homepage(page, CRUD.get_data())  
            check_datas_and_notify() 
            await asyncio.sleep(60)  

    async def start_background_task():
        await asyncio.gather(
            periodic_update(),
            check_schedule()  
        )
    page.run_task(start_background_task)
#Page routing and Navigation
    pages = {
        '/': View("/", [home_page]),
        '/settings': View("/settings", [settings_page]),
        '/schedule': View("/schedule", [schedule_page]),
        '/graphs': View("/graphs", [graphs_page]),
    }

    def route_change(route):
        page.views.clear()  
        page.views.append(pages[page.route])  
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

app(target=main)

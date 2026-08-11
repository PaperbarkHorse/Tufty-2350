import json
import math

services_data = None

def init():
    global services_data
    services_data = fetch_example_services()

def update():
    global services_data

    if not services_data:
        return
    
    screen.pen = color.rgb(0, 0, 0)
    screen.clear()

    services = sorted(services_data["services"], key=lambda service: f"{service["runDate"]}-{service["locationDetail"]["gbttBookedDeparture"]}")

    y = 8

    for i, service in enumerate(services):
        if y >= screen.height:
            break
        
        if not service["locationDetail"]["isPublicCall"]:
            continue

        screen.font = font.sins
        screen.pen = color.rgb(255, 255, 255)
        screen.text(f"{service["locationDetail"]["gbttBookedDeparture"][0:2]}", 0, y)
        screen.text(":", 10, y - 1)
        screen.text(f"{service["locationDetail"]["gbttBookedDeparture"][2:4]}", 13, y)

        screen.clip = rect(28, 0, screen.width - 72, screen.height)
        screen.font = font.match
        text_overflow(f"{service["locationDetail"]["destination"][0]["description"]}", 28, y, screen.width - 72, (badge.ticks / 4000) % 1)
        screen.clip = rect(0, 0, screen.width, screen.height)

        screen.font = font.sins
        if "gbttBookedDeparture" in service["locationDetail"] and "realtimeDeparture" in service["locationDetail"]:
            delay_time = railway_time_to_mins(service["locationDetail"]["realtimeDeparture"]) - railway_time_to_mins(service["locationDetail"]["gbttBookedDeparture"])

            if delay_time >= 5 or delay_time <= -20 * 60:
                screen.pen = color.rgb(255, 80, 80)
                screen.text("Delayed", 118, y)
            else:
                screen.pen = color.rgb(80, 128, 255)
                screen.text("On time", 118, y)


        if i == 0:
            y += 10

            screen.font = font.sins
            screen.pen = color.rgb(200, 200, 200)
            screen.text(f"Calling at: ...", 0, y)

        y += 10

    screen.font = font.match
    screen.pen = color.rgb(255, 66, 0)
    screen.rectangle(0, 0, 160, 10)
    screen.pen = color.rgb(255, 255, 255)
    text_centered(f"{services_data["location"]["name"]}", 80, -2)

    (year, month, day, hour, minute, second, dow) = rtc.datetime()
    screen.pen = color.rgb(255, 66, 0)
    screen.rectangle(0, 110, 160, 10)
    screen.pen = color.rgb(255, 255, 255)
    text_centered(f"{hour:02}:{minute:02}:{second:02}", 80, 108)

def text_centered(text, x, y):
    width, height = screen.measure_text(text)
    screen.text(text, math.floor(x - width / 2), y)

def text_overflow(text, x, y, width, t):
    text_width, text_height = screen.measure_text(text)
    overflow_x = max(0, text_width - width)

    prev_clip = screen.clip
    screen.clip = rect(x, y, width, text_height)

    screen.text(text, math.floor(x - (overflow_x * t)), y)

    screen.clip = prev_clip

def railway_time_to_mins(time_str):
    hours = int(time_str[0:2])
    mins = int(time_str[2:4])
    return (hours * 60) + mins

def fetch_services(station):
    pass

def fetch_example_services():
    with open("example.json", "r") as file:
        data = json.load(file)
    return data
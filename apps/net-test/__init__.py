import wifi
import fetch_patched as fetch
import system
import draw

req = None
data = None
last_fetch = -1

cover_req = None
cover_url = None
cover_image = None

last_cover_url = None

def init():
    badge.mode(HIRES)

    network = system.get_selected_network() 
    wifi.connect(network["ssid"], network["password"])

def input():
    pass

def update():
    global req, data, last_fetch, cover_req, cover_url, cover_image, last_cover_url

    draw.clear(0, 0, 0)
    screen.pen = color.rgb(255, 255, 255)
    screen.font = font.ignore

    if not wifi.is_connected():
        screen.text(f"{wifi.status()[0]}", 10, 10)
        screen.text(f"{wifi.status()[1]}", 10, 30)
        return

    req_done = req is not None and req.done

    if req_done:
        data = req.json()
        last_fetch = badge.ticks

    if req is None:
        req = fetch.url("https://api.paperbark.horse/activity/current", 2)

    if cover_req is not None and cover_req.done:
        cover_image = image.load("/cache-track-cover.jpg")
        last_cover_url = cover_url
        cover_req = None

    if data:
        activity = data["activities"][0]

        if activity["type"] == "finding-music":
            draw.center_text(f"Finding music...", screen.width / 2, screen.height / 2)
        
        if activity["type"] == "music":
            if (activity["track"]["cover"] and activity["track"]["cover"] != cover_url and cover_req is None) or (cover_req is not None and cover_req.error):
                cover_url = activity["track"]["cover"]
                cover_req = fetch.url(cover_url).to("/cache-track-cover.jpg")

            if cover_image and activity["track"]["cover"] == last_cover_url:
                screen.blit(cover_image, rect((screen.width - 160) / 2, 5, 160, 160))

            draw.center_text(f"{activity["track"]["title"]}", screen.width / 2, 165)
            draw.center_text(f"{activity["track"]["artist"]}", screen.width / 2, 190)

            duration = activity["player"]["playback"]["end"] - activity["player"]["playback"]["start"]
            position = activity["time"]["from"] - activity["player"]["playback"]["start"]

            screen.pen = color.rgb(50, 50, 50)
            screen.rectangle(5, screen.height - 15, screen.width - 10, 10)
            screen.pen = color.rgb(255, 255, 255)
            screen.rectangle(5, screen.height - 15, (screen.width - 10) * (position / duration), 10)
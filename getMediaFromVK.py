import requests
import re
import time

from bs4 import BeautifulSoup
from vk import VK
from datetime import datetime, timedelta
from urllib.parse import unquote

def getMediaFromVK(vk, owner_id):

  response = vk.makeRequest("wall.get", {"owner_id": owner_id, "count": 100})
  items = response["items"]

  time_limit = datetime.now() - timedelta(hours=24)

  max_er = 0
  max_i = 0

  for i, item in enumerate(items):
    if (datetime.fromtimestamp(int(item["date"])) > time_limit and "views" in item and "attachments" in item):
      if (item["attachments"][0]["type"] == "link"):
        ev = item["likes"]["count"] + item["reposts"]["count"] + item["comments"]["count"]
        er = ev / item["views"]["count"] * 100
        if (er > max_er):
          max_er = er
          max_i = i

  if (max_er != 0):

    media = items[max_i]["attachments"][0]["link"]

    response = requests.post("https://vk.com/al_wall.php", data = {
      "act": "get_wall",
      "al": 1,
      "offset": max_i,
      "owner_id": owner_id,
      "type": "own",
      "wall_start_from": max_i
    })

    parsed_html = re.findall(r'<div class="page_media_link_photo">(.*?)</div>', str(response.content, "windows-1251"), re.M)
    soup = BeautifulSoup(parsed_html[0], "html.parser")

    my_url = re.findall((r"/away\.php\?to=(.*?)&"), soup.a["href"], re.M)[0]

    return {"text": media["title"], "photo": soup.img["src"], "url": unquote(my_url)}

  else:
    return None

GROUP_ID = 37862023
vk = VK()

group_ids = {
  "VOGUE": 24396213,
  "ELLE": 7144938,
  "GQ Russia": 2089898,
  "GRAZIA": 37523614,
  #"Buro 24/7": 27345776,
  "Wonderzine": 54218032,
  "Harper's Bazaar": 37416018
}

message = "Лучшие статьи из популярных журналов о моде за последние 24 часа &#128293;\n\n"
photos = []

for alias, group_id in group_ids.items():

  media = getMediaFromVK(vk, -group_id)
  print(media)

  if (media != None):
    message += "%s: «%s»\n%s\n\n" % (alias, media["text"], vk.getShortLink(media["url"]))
    response = requests.get(media["photo"])
    open("photo.jpg", "wb").write(response.content)
    photos.append(vk.uploadPhoto(GROUP_ID, "photo.jpg", media["text"]))

if (len(photos) >= 3):
  #message += "#Мода@faces"
  vk.post(-GROUP_ID, message, photos)

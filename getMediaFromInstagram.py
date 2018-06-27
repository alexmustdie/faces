import requests
import re
import json as json_parser

from vk import VK
from datetime import datetime, timedelta

def getMediaFromInstagram(username):

  response = requests.get("https://instagram.com/%s" % username)
  data = re.findall(r'<script type="text/javascript">window\._sharedData = (.*?);</script>', response.content.decode("utf-8"), re.M)
  json = json_parser.loads(data[0])

  items = json["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
  time_limit = datetime.now() - timedelta(hours=12)

  media = []

  for i, item in enumerate(items):
    node = item["node"]
    if (datetime.fromtimestamp(int(node["taken_at_timestamp"])) > time_limit
      and node["is_video"] != True):
      media.append({
        "text": "",
        "photo": node["display_url"],
        "url": "http://instagram.com/p/%s" % node["shortcode"]
      });

  if (len(media) != 0):
    return media;
  else:
    return None

GROUP_ID = 37862023
vk = VK()

celebrities = {
  "Селена Гомес": "selenagomez",
  "Зак Эфрон": "zacefron",
  "Блейк Лавли": "blakelively",
  "Нина Добрев": "nina",
  "Крис Пратт": "prattprattpratt",
  "Эмма Робертс": "emmaroberts",
  "Лили Колинз": "lilyjcollins",
  "Бейонсе": "beyonce",
  "Криштиану Роналду": "cristiano",
  "Джей Ло": "jlo",
  "Victoria's Secret": "victoriassecret",
  "Джастин Тимберлейк": "justintimberlake",
  "Дэвид Бекхэм": "davidbeckham",
  "Рианна": "badgalriri",
  "Марго Робби": "margotrobbie",
  "Уилл Смит": "willsmith",
  "Настя Ивлеева": "_agentgirl_",
  "Меган Фокс": "the_native_tiger",
  "Дрейк": "champagnepapi",
  "Дженнифер Лоуренс": "jenniferlawrencepx",
  "Кайли Дженнер": "kyliejenner",
  "Джиджи Хадид": "gigihadid",
  "Белла Хадид": "bellahadid",
  "Эмили Ратаковски": "emrata",
  "Роми Стрейд": "romeestrijd",
  "Кендалл Дженнер": "kendalljenner",
  "Жозефин Скривер": "josephineskriver",
  "Сара Сампайо": "sarasampaio",
  "Ирина Шейк": "irinashayk",
  "Грейс Элизабет": "lovegrace_e",
  "Адриана Лима": "adrianalima",
  "Эльза Хоск": "hoskelsa",
  "Кара Делевинь": "caradelevingne",
  "Вика Одинцова": "viki_odintcova",
  "Алексис Рэн": "alexisren",
  "Ким Кардашян": "kimkardashian",
  "Тейлор Хилл": "taylor_hill",
  "Роузи Хантингтон-Уайтли": "rosiehw",
  "Джессика Ли Бьюкенен": "jessleebuchanan",
  "Жасмин Тукс": "jastookes",
  "Алессандра Амбросио": "alessandraambrosio",
  "Стелла Максвелл": "stellamaxwell",
  "Кайя Гербер": "kaiagerber",
  "Барбара Палвин": "realbarbarapalvin",
  "Марта Хант": "marthahunt",
  "Синди Мелло": "cindymello"
}

'''
message = "Лучшие публикации из инстаграмм-аккаунтов селебрити за последние 24 часа &#128293;\n\n"
photos = []
'''

for name, username in celebrities.items():

  media = getMediaFromInstagram(username)
  print(media)

  if (media != None):
    
    photos = []

    for item in media:
      response = requests.get(item["photo"])
      open("photo.jpg", "wb").write(response.content)
      photos.append(vk.uploadPhoto(GROUP_ID, "photo.jpg", name))
    
    vk.post(-GROUP_ID, "&#128163; %s\n&#128247; Instagram: %s" % (name, username), photos)

'''
if (len(photos) >= 3):
  message += "#Селебрити@faces"
  vk.post(-GROUP_ID, message, photos)
'''

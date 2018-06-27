import requests
import urllib
import time

class VK:

  access_token = ""
  v = "5.73"

  def __init__(self, access_token = "your access token"):
    self.access_token = access_token
    print("VK initialized with user %s" % (self.getCurrentUserId()))

  def makeRequest(self, method, params = []):

    my_params = {
      "access_token": self.access_token,
      "v": self.v
    }

    if (params):
      for key, param in params.items():
        my_params[key] = param

    response = requests.get("https://api.vk.com/method/%s?%s" % (method, urllib.parse.urlencode(my_params)))
    time.sleep(5)
    #print(response.content.decode("utf-8"))
    json = response.json()

    return json["response"]

  def getCurrentUserId(self):
    return self.makeRequest("users.get")[0]["id"]

  def uploadPhoto(self, group_id, file_name, caption = None):

    response = self.makeRequest("photos.getWallUploadServer", {"group_id": group_id})

    files = {"photo": open(file_name, "rb")}
    response = requests.post(response["upload_url"], files=files)
    json = response.json()

    response = self.makeRequest("photos.saveWallPhoto",
    {
      "group_id": group_id,
      "photo": json["photo"],
      "server": json["server"],
      "hash": json["hash"],
      "caption": caption
    })

    return "photo%s_%s" % (response[0]["owner_id"], response[0]["id"])

  def post(self, owner_id, message, attachments = []):
    response = self.makeRequest("wall.post",
    {
      "owner_id": owner_id,
      "message": message,
      "attachments": ",".join(attachments)
    })
    print(response)

  def getShortLink(self, url):
   response = self.makeRequest("utils.getShortLink", {"url": url})
   return response["short_url"]

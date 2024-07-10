import requests
from conf import OWNER_ID, VK_SERVICE_TOKEN 


VERSION = 5.199

def get_post(old_hash) -> list:
    response = requests.get(
        "https://api.vk.com/method/wall.get",
        params={
            "access_token": VK_SERVICE_TOKEN,
            "v": VERSION,
            "owner_id": OWNER_ID,
            "count": 1
        }
    )
        
    item = response.json()["response"]["items"][0]
    hash_post = item["hash"]
    if old_hash == hash_post:
        return []

    attachments = item["attachments"]
    text = item["text"]
    links_photo = []

    if len(attachments) > 0:
        for attachment in attachments:
            link_photo = max(attachment["photo"]["sizes"], key=lambda x: x["height"])
            links_photo.append(link_photo["url"])

    return [text, hash_post, links_photo]


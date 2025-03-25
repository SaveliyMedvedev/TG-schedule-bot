import requests
from conf import OWNER_ID, VK_GROUP_TOKEN, VK_SERVICE_TOKEN

API_VERSION = 5.199


response = requests.get(
    "https://api.vk.com/method/groups.getLongPollServer",
    params={
        "group_id": OWNER_ID,
        "access_token": VK_GROUP_TOKEN,
        "v": API_VERSION,
        "scope": "manage",
    },
)
print(response.json())
data = response.json()["response"]
server = data["server"]
key = data["key"]
ts = data["ts"]


def get_updates():
    global ts
    response = requests.get(
        server, params={"act": "a_check", "key": key, "ts": ts, "wait": 25}
    )

    with open("log.json", "w") as json_file:
        print(response.json(), file=json_file)

    updates = response.json()
    if "failed" in updates:
        raise RuntimeError("Error in VK long poll response")

    ts = updates["ts"]
    return updates.get("updates", [])


def get_post():
    response = requests.get(
        "https://api.vk.com/method/wall.get",
        params={
            "access_token": VK_SERVICE_TOKEN,
            "v": API_VERSION,
            "owner_id": OWNER_ID,
            "count": 1,
        },
    )

    item = response.json()["response"]["items"][0]
    attachments = item["attachments"]
    text = item["text"]
    links_photo = []

    if attachments:
        for attachment in attachments:
            link_photo = max(attachment["photo"]["sizes"], key=lambda x: x["height"])
            links_photo.append(link_photo["url"])

    return {"text": text, "links_photo": links_photo}

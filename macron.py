import json
import os
import random
import requests


def get_current_emoji(token, user_id):
    headers = {"Authorization": "Bearer %s" % token}
    res = requests.get("https://slack.com/api/users.profile.get", headers=headers, params={"user": user_id}).json()
    return res["profile"]["status_emoji"]


def choice_emoji():
    emojis = (
        ":fishing_pole_and_fish:", ":coffee:", ":tea:", ":sake:", ":beer:",
        ":cocktail:", ":tropical_drink:", ":wine_glass:", ":pizza:", ":hamburger:",
        ":fries:", ":spaghetti:", ":meat_on_bone:", ":curry:", ":fried_shrimp:", ":bento:",
        ":sushi:", ":fish_cake:", ":rice_ball:", ":rice_cracker:", ":rice:", ":ramen:",
        ":stew:", ":oden:", ":dango:", ":egg:", ":bread:", ":doughnut:", ":custard:", ":icecream:",
        ":ice_cream:", ":shaved_ice:", ":birthday:", ":cake:", ":cookie:", ":chocolate_bar:",
        ":candy:", ":lollipop:", ":apple:", ":green_apple:", ":tangerine:", ":lemon:",
        ":cherries:", ":grapes:", ":watermelon:", ":strawberry:", ":peach:", ":melon:",
        ":banana:", ":pear:", ":pineapple:", ":sweet_potato:", ":eggplant:", ":tomato:", ":corn:"
    )
    return random.choice(emojis)


def lambda_handler(**kwargs):
    TOKEN = os.environ["TOKEN"]
    USER_ID = os.environ["USER_ID"]

    current_emoji = get_current_emoji(TOKEN, USER_ID)
    new_emoji = choice_emoji()
    while new_emoji == current_emoji:
        new_emoji = choice_emoji()

    headers = {"Authorization": "Bearer %s" % TOKEN, "X-Slack-User": USER_ID, "Content-Type": "application/json; charset=utf-8"}
    payload = {"profile": {"status_emoji": new_emoji, "status_text": new_emoji.strip(":")}}
    res = requests.post("https://slack.com/api/users.profile.set", data=json.dumps(payload), headers=headers).json()
    print(res)

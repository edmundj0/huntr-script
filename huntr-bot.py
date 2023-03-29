import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

linkedin_msg_arr = ["bot-test", "bot-test1", "bot-test2"]

headers = {
    "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"
}


def make_linkedin_outreach():

    for i in range(len(linkedin_msg_arr)):
        body = {
            "activityCategoryId": os.getenv('LINKEDIN_MESSAGE_ID'),
            "boardId": os.getenv('BOARD_ID'),
            "completed": "true",
            "completedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "endAt": None,
            "note": "",
            "startAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "title": linkedin_msg_arr[i]
        }

        response = requests.post('https://api.huntr.co/api/activity', headers=headers, data=body)
        response_data = response.json()

        print(response_data)

make_linkedin_outreach()

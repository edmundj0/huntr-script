import requests
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

linkedin_msg_arr = ["test2"]
regular_apply_arr = [("test job title", "test company name")]

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

        pprint(response_data)

def log_regular_apply():


    body = {
        "company.name": {"placeholder": "placeholder"}, #values don't matter but key required, or else "company requires name or id error"
        "company": {"name": "placeholder"}, #value doesn't matter but key required, or else _id undefined error
        "listId": os.getenv('LIST_ID'),
        "jobTitle": "REPLACE THIS",
    }

    response = requests.post('https://api.huntr.co/api/job', headers=headers, data=body)
    response_data = response.json()
    pprint(response_data)

    time.sleep(0.5)

    headers["Content-Type"] = "application/json" #have to add for put request, but get "company requires name or id error" if added to post

    data = {
        "company": {"name": "THIS VALUE PERSISTS"},
        "company.name": "placeholder" #value doesn't matter but key required, or else "company requires name or id error"
    }

    update_name = requests.put(f'https://api.huntr.co/api/job/{response_data["job"]["id"]}/company', headers=headers, data=json.dumps(data))
    update_name_data = update_name.json()
    print('------------------------------')
    pprint(update_name_data)


if __name__ == "__main__":
    make_linkedin_outreach()
    log_regular_apply()


# testing = {"company.name": "??", "company": {"name":"THIS IS THE VALUE THAT MATTERSs"}}

# headers = {
#     "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
#     "Content-Type": "application/json"
# }

# update_test = requests.put(f'https://api.huntr.co/api/job/{}/company', headers=headers,data=json.dumps(testing))
# print(update_test.json())



# {
#     "company": {
#         "name": "testing_bota"
#     },
#     "listId": "Test",
#     "jobTitle": "No Job Title"
# }


# testing2 = {"company": {"name": "yooooo"}}

# testing = {"company.name": {"name": "yooooooooooooooooooooooooooo"}, "company": {"name":"yoooooooo"}}

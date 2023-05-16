import requests
import os
import time
import json, random
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint
from parse_csv import parse_csv

load_dotenv()

csv_data = parse_csv()


linkedin_msg_arr = []
regular_apply_arr = []
high_quality_apply_arr = []

high_quality_apply_arr.extend(csv_data) #edit this line!!!

headers = {
    "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
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

def log_apply(i, isHighQuality=None):


    body = {
        "company.name": {"placeholder": "placeholder"}, #values don't matter but key required, or else "company requires name or id error"
        "company": {"name": "placeholder"}, #value doesn't matter but key required, or else _id undefined error
        "listId": os.getenv('LIST_ID'),
        "jobTitle": regular_apply_arr[i][1] if not isHighQuality else high_quality_apply_arr[i][1],
    }

    response = requests.post('https://api.huntr.co/api/job', headers=headers, data=body)
    response_data = response.json()
    pprint(response_data)

    time.sleep(0.5)

    headers["Content-Type"] = "application/json" #have to add for put request, but get "company requires name or id error" if added to post

    data = {
        "company": {"name": regular_apply_arr[i][0] if not isHighQuality else high_quality_apply_arr[i][0]},
        "company.name": "placeholder", #value doesn't matter but key required, or else "company requires name or id error"
    }

    update_name = requests.put(f'https://api.huntr.co/api/job/{response_data["job"]["id"]}/company', headers=headers, data=json.dumps(data))
    update_name_data = update_name.json()
    print('------------------------------')
    pprint(update_name_data)


    #add color to job on ui
    def get_random_color():
        chars = "0123456789ABCDEF"
        color = "#"
        for i in range(6):
            color += chars[random.randint(0,15)]
        return color


    color_data = {
        "jobId": str(response_data["job"]["id"]),
        "job": {"color": get_random_color()}
    }

    add_color = requests.put(f'https://api.huntr.co/api/job', headers=headers, data=json.dumps(color_data))
    add_color_response = add_color.json()
    print('------------------------')
    pprint(add_color_response)

    if isHighQuality:

        data = {
            "activityCategoryId": os.getenv('HIGH_QUALITY_APPLICATION_EFFORT')
        }
        change_activity_to_high_quality = requests.put(f'https://api.huntr.co/api/activity/{update_name_data["job"]["_activities"][0]}', headers=headers, data=json.dumps(data))
        change_activity_res = change_activity_to_high_quality.json()
        print('------------------------------')
        pprint(change_activity_res)


    del headers["Content-Type"] #delete since headers is globally defined


if __name__ == "__main__":
    make_linkedin_outreach()

    for i in range(len(regular_apply_arr)):
        log_apply(i)

    for i in range(len(high_quality_apply_arr)):
        log_apply(i, 1)


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

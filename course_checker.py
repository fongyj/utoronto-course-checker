import requests
import time
from notify_run import Notify
from interested_courses import interested_courses
import datetime

url = r"https://api.easi.utoronto.ca/ttb/getPageableCourses"
payload = {"courseCodeAndTitleProps":
           {"courseCode":"",
            "courseTitle":"",
            "courseSectionCode":"F",
            "searchCourseDescription":"false"
            },
            "departmentProps":[],
            "campuses":[],
            "sessions":["20239"],
            "requirementProps":[],
            "instructor":"",
            "courseLevels":[],
            "deliveryModes":[],
            "dayPreferences":[],
            "timePreferences":[],
            "divisions":[],
            "creditWeights":[],
            "page":1,
            "pageSize":20,
            "direction":"asc"}
headers = {"Accept": "application/json"}

notify = Notify()
frequency = 30 # seconds

if __name__ == "__main__":
    while True:
        for interested_course in interested_courses:
            course_payload = dict(payload)
            course_payload["courseCodeAndTitleProps"]["courseCode"] = interested_course["courseCode"]
            course_payload["courseCodeAndTitleProps"]["courseTitle"] = interested_course["courseTitle"]
            course_payload["divisions"] = interested_course["divisions"]
            response = requests.post(url, json=course_payload, headers=headers)
            response = response.json()
            course = response["payload"]["pageableCourse"]["courses"][0]
            sections = course["sections"]
            target = interested_course["target"]
            for section in sections:
                message = course["code"] + " " + course["name"]
                if target and section["name"] not in target:
                    continue
                if section["type"] == "Lecture":
                    message += "\n" + section["name"]
                    availability = section["maxEnrolment"] - section["currentEnrolment"]
                    # waitlist = section["currentWaitlist"]
                    message += " Availability: {}".format(availability)
                    if availability > 0:
                        message += "\n" + str(datetime.datetime.now())
                        print(message)
                        print()
                        notify.send(message)
        time.sleep(frequency)

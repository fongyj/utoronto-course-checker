import requests
import time
from notify_run import Notify

url = r"https://api.easi.utoronto.ca/ttb/getPageableCourses"
interested_courses = [
    {"courseCode":"CSC309H1", "courseTitle":"Programming on the Web", "divisions":["ARTSC"]},
    {"courseCode":"CSCC73H3", "courseTitle":"Algorithm Design and Analysis", "divisions":["SCAR"],},
    {"courseCode":"MATB43H3", "courseTitle":"Introduction to Analysis", "divisions":["SCAR"],},
    ]
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
        for section in sections:
            message = course["code"] + " " + course["name"]
            if section["type"] == "Lecture":
                message += "\n" + section["name"]
                availability = section["maxEnrolment"] - section["currentEnrolment"]
                waitlist = section["currentWaitlist"]
                message += " Availability: {}".format(availability)
                if availability > 0:
                    print(message)
                    notify.send(message)
    time.sleep(5)

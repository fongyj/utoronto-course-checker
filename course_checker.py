import requests
import time

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

while True:
    for interested_course in interested_courses:
        course_payload = dict(payload)
        course_payload["courseCodeAndTitleProps"]["courseCode"] = interested_course["courseCode"]
        course_payload["courseCodeAndTitleProps"]["courseTitle"] = interested_course["courseTitle"]
        course_payload["divisions"] = interested_course["divisions"]
        response = requests.post(url, json=course_payload, headers=headers)
        response = response.json()
        course = response["payload"]["pageableCourse"]["courses"][0]
        print(course["name"] + " " + course["code"] + "\r")
        sections = course["sections"]
        for section in sections:
            if section["type"] == "Lecture":
                print(section["type"], section["name"])
                print("Availability: {}\r".format(section["maxEnrolment"] - section["currentEnrolment"]))
                print("Current waitlist: {}\r".format(section["currentWaitlist"]))
                print()
    time.sleep(5)

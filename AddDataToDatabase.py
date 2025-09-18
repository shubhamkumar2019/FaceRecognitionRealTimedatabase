

import firebase_admin
from firebase_admin import credentials,db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognition-c7a6e-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')
data = {


    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "section": "Cse 25",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "section": "Cse 28",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "224314":
        {
            "name": "Shailendra Shukla",
            "major": "Computer ",
            "starting_year": 2022,
            "total_attendance": 22,
            "section": "Cse 42",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "224169":
        {
            "name": "Shakshi Baruah",
            "major":"Computer",
            "starting_year": 2022,
            "total_attendance": 27,
            "section": "Cse 12",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "224174":
        {
            "name": "Siddharth",
            "major":"Computer",
            "starting_year": 2022,
            "total_attendance": 27,
            "section": "Cse 19",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
    },
    "224172":
        {
            "name": "Shubham",
            "major":"Computer",
            "starting_year": 2022,
            "total_attendance": 2,
            "section": "Cse 1",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
    },
    "2229208":
        {
            "name": "Nikhil",
            "major":"Computer",
            "starting_year": 2022,
            "total_attendance": 2,
            "section": "Cse 1",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        }

}

for key, value in data.items():
    ref.child(key).set(value)
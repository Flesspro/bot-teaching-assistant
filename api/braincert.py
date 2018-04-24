import json
import requests
import urllib.request, urllib.parse, urllib.error
import config
import re
import systemtools
from sender import sender
import sqlite3, re, sys
from datetime import datetime


def create_class(start_at, end_at, full_title):
    """
    Creates a braincert class
    start_at : datetime "2018-03-16 19:20"
    end_at : datetime "2018-03-16 19:40"
    """

    # Convert date and time into format appropriate for braincert
    # Date: YYYY-MM-DD; Time: HH:MMAM
    date = start_at.date()
    start_time = datetime.strptime(str(start_at)[11:16],"%H:%M").strftime("%I:%M%p")
    end_time = datetime.strptime(str(end_at)[11:16],"%H:%M").strftime("%I:%M%p")

    # Create JSON to be sent to Braincert API
    data = {
            'title': full_title,
            'timezone': '54',
            'start_time': start_time,
            'end_time': end_time,
            'date' : date,
            'record' : '3',  # PUT 3 to enable recording (limited in free version of braincert)
            'isVideo' : '1'
    }
    url = 'https://api.braincert.com/v2/schedule?apikey='+config.api_braincert
    request = requests.post(url, params=data)

    request_json = json.loads(request.text)

    # If there was an error on the Braincert side, report and quit
    if (request.status_code)!= 200 or (request_json["status"] == "error"):
        print (request.text)
        return (None)

    print (request_json)
    braincert_id = request_json["class_id"]
    # self.braincert_id = 144892

    return (braincert_id)

def delete_class(classId):
    """
    Delete a class
    classId : Braincert id - int
    """

    data = {
            'cid': classId,
    }

    url = 'https://api.braincert.com/v2/removeclass?apikey='+config.api_braincert
    request = requests.post(url, params=data)

    # If there was an error on the Braincert side, report and quit
    if request.status_code != 200:
        print (request.text)
        return (0)


    request_json = json.loads(request.text)

    print (request_json)

    if request_json["status"] == "error":
        print (request_json["error"] )
        return (None)

    print ("Class %s succesfully deleted"%classId)


def join_class(class_id, userId, userName, isTeacher, lessonName, courseName):
    """
    Add a student to the online class in Braincert
    user_name : string
    user_status : 0 (student) or 1 (instructor, admin)
    """

    # url = 'https://api.braincert.com/v2/listclass?apikey='+config.api_braincert
    # request = requests.post(url)
    # print (request.text)

    data = {
            'class_id': class_id,
            'userId': userId,
            'userName': userName,
            'isTeacher': isTeacher,
            'lessonName' : lessonName,
            'courseName' : courseName,
            'isVideo' : '1'
    }

    url = 'https://api.braincert.com/v2/getclasslaunch?apikey='+config.api_braincert
    request = requests.post(url, params=data)
    # print (request.text)

    # If there was an error on the Braincert side, report and quit
    if request.status_code != 200:
        print (request.text)
        return (0)

    request_json = json.loads(request.text)
    if request_json["status"] == "error":
        print (request_json["error"] )
        return (None)

    user_url = request_json["encryptedlaunchurl"]
    return (user_url)


def download_class(file_name, class_id):
    """
    Downloads a video recording of a Braincert class
    file_name : string
    class_id : Braincert id - int
    """

    data = {
            'class_id': class_id,
    }

    url = 'https://api.braincert.com/v2/getclassrecording?apikey='+config.api_braincert
    request = requests.post(url, params=data)

    # If there was an error on the Braincert side, report and quit
    if request.status_code != 200:
        print (request.text)
        return (None)

    # In this case json is a list, hence reference [0]
    request_json = json.loads(request.text)[0]
    if request_json["status"] == "error":
        print (request_json["error"] )
        return (None)

    file_url = request_json["record_url"]
    extension = re.search('.*[.](.*$)', request_json["name"]).group(1)

    file_name_ext = file_name + "." + extension

    # Download using systemtools
    full_file_path = systemtools.download_from_url(file_url, file_name_ext)

    return(full_file_path)


def statistics(classId, userId):
    """
    Downloads a video recording of a Braincert class
    classId : Braincert id - int
    userId : id from DB
    """

    data = {
            'classId': classId,
            'userId' : userId
    }

    url = 'https://api.braincert.com/v2/getclassreport?apikey='+config.api_braincert
    request = requests.post(url, params=data)

    # If there was an error on the Braincert side, report and quit
    if request.status_code != 200:
        print (request.text)
        return (None)


    request_json = json.loads(request.text)

    print (request_json)

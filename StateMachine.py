# -*- coding: utf-8 -*-
from enum import Enum
import config

class States(Enum):
    """
    A simple state machine to easier navigation
    """
    START = 0
    TG = 10
    CHECK_CONTACT= 111
    TG_ERR = 11
    GMAIL = 121

    HOME = 200
    COURSE = 21
    ASSIGNMENTS =220
    SEND_ASSIGNMENT = 250
    SUCCESS_ASSIGNMENT = 28
    PROGRESS = 30
    CONTACT = 40
    CONTACT_THANKS = 42

    APPLY = 60
    LNAME = 61

    ALL_COURSES = 51
    NOT_ENROLLED = 80
    USER_SAVED = 85

    ERROR = 1
    FETCH = 999


    UNKNOWN = 0
    STUDENT = 1
    APPLICANT = 2

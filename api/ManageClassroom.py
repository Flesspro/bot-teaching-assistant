from DataBase import db
import braincert
import sys
import datetime
import sender

class OnlineClassroom ():
    """
    Online classroom in Braincert
    """
    def __init__(self, class_id):
        """
        Set up the OnlineClassroom object using class_id from DB
        """
        self.class_info = db.get_class_by_id(class_id)
        self.course_info = db.get_course(self.class_info["course_id"])

        # Add some useful varialbles for easier reference
        self.class_title = self.class_info["title"]
        self.course_title = self.course_info["title"]
        self.full_title = self.course_title + ": " + self.class_title
        self.start = self.class_info["start"]
        self.end = self.class_info["end"]

        # Check if the class already has a braincert classroom. If not, create it
        self.braincert_id = self.class_info["braincert_id"]

        if (self.braincert_id == None) or (self.braincert_id == ""):
            self.braincert_id = braincert.create_class(self.start, self.end, self.full_title)
            if self.braincert_id == None:       # if could not create classroom for some reason
                print ("\n Error in creating Braincert classroom")
                return (None)
            else:
                print ("\n Successfully created Braincert classroom {0} for Class {1}".format(self.braincert_id, self.full_title))
                db.save_class_braincert_id(self.class_info, self.braincert_id)
        else:
            print ("\n Braincert classroom {0} for Class \"{1}\" already exists".format(self.braincert_id, self.full_title))

    def create_user_link(self, user_id):
        """
        Given user_id, create a unique braincert link for them for this OnlineClassroom
        braincert.join_class(braincert_id, userId, userName, isTeacher, lessonName, courseName)
        """

        user = db.get_user_by_id(user_id)
        userName = user["firstname"] + " " + user["lastname"]
        print ("\n Creating a link for %s to Class %s" %(userName, self.full_title))

        if self.course_info["users"][user_id]["user_status"] > 1:
            isTeacher = 1
        else:
            isTeacher = 0

        lessonName = self.class_title
        courseName = self.course_title

        link = braincert.join_class(self.braincert_id, user_id, userName, isTeacher, lessonName, courseName)

        if (link == None) or (link == ""):
            print ("\n Failed to create a link for %s to Class %s" %(userName, self.full_title))
            return (None)
        else:
            print ("\n Successfully created a link for %s to Class %s" %(userName, self.full_title))
            db.save_user_link_to_classroom(self.class_info, user_id, link)
            return (link)

    def notify_user(self, user_id, link):
        """
        Given user_id and link to online classroom, notify them of the upcoming class and share the online classroom link
        braincert.join_class(braincert_id, userId, userName, isTeacher, lessonName, courseName)
        """

        user = db.get_user_by_id(user_id)
        firstname = user["firstname"]
        chat_id = user["tgchat"]

        now = datetime.datetime.now()

        # If the class is not today, mention the date
        if now.date() != self.start.date():
            ClassDate = self.start.date().strftime(' on %b, %d')
        else:
            ClassDate = " today"

        message = ("Hey %s, your class %s of %s is going to start%s at %s:%s. Please join the class via your [personal link](%s)"
            %(firstname, self.class_title, self.course_title, ClassDate, str(self.start.hour), str(self.start.minute), link))

        print ("Message for %s : \n %s" %(chat_id, message))
        sender.sender(chat_id, message)


if __name__=='__main__':
    # pass class_id as argument
    OnlineClassroom = OnlineClassroom(sys.argv[1])
    for user in OnlineClassroom.course_info["users"]:
        link = OnlineClassroom.create_user_link(user)
        if sys.argv[2] == "True":
            OnlineClassroom.notify_user(user, link)

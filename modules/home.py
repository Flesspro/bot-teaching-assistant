from StateMachine import States
from frm import handles as handles
from DataBase import db
from frm.TgFlow import get_file_link

handlePost =handles.post
handleAction = handles.action
handleString = handles.st

def contact_check(i,s,**d):
    db = DataBase()
    c= i.contact
    if i.from_user.id ==c.user_id:
        if db.user_registered(c.phone_number):
            db.add_chat_id(c.phone_number,c.user_id)
            d['role']='student'
            if db.user_gmail(c.user_id):
                new_state = States.HOME
            else:
                new_state=States.GMAIL
        else:
            new_state=States.NOT_ENROLLED
    return new_state, d

home_kb= [
    {'Home':handleAction(States.HOME)},
    {'Contact':handleAction(States.CONTACT)}
]

def format_lessons(lessons, personal = False):
    text = "*Schedule:*\n"
    for lesson in lessons:
        text += lesson['title'] + '\n'
    return text

def format_course(course):
    format = "%d/%m,%H:%M"
    frm = course['from'].strftime( format)
    to = course['to'].strftime( format)
    return "*%s*\n *Dates*: %s-%s \n *Enrollment*: %s \n%s"%(
        course['title'],frm,to,'Open' if course['active'] else 'Closed',
        course['description'])

def generate_course_text(s,**d):
    course = db.get_course(d['course_id'])
    text = ''
    if d['role']=='student':
        text += 'Your course details:\n'
        text += format_course(course)
        text += format_lessons(d['lessons'], personal = True)

    if d['role'] == 'applicant':
        text += 'Course details:\n'
        text += format_course(course)
        text += format_lessons(d['lessons'])
    return text

def get_courses(i,s,**d):
    courses = db.get_courses(i.from_user.id)
    if courses:
        d['role']='student'
    d['courses'] = courses
    #print('courses', courses)
    return d

def save_assignment(i,course_id=None):
    print ('INP',i)
    error= db.save_assignment(**{
                           'user':str(i.from_user.id),
                           'course_id':course_id,
                           'link':get_file_link(i.document.file_id),
    })
    if not error:
        return States.SUCCESS_ASSIGNMENT
    else:
        return States.ERROR

UI={
    States.HOME:{'t':'Here are your courses',
          'b':[
               # button to display each course with title on it
               handlePost(lambda s,**d:\
                  (list(map(lambda course:\
                      {course.get('title') : handleAction(lambda i,s,**d:
                            (States.COURSE,\
                             # and also save course_id he picked
                             dict(d,**{'course_id':str(course.get('_id')),
                                       'course_name':course.get('title'),
                                       'role':'student'})\
                            ),
                            name=course.get('title')
                            )},\
                        d.get('courses',[]) or []))\
                )
                ),
                # list all other Fless courses
                {'List other Fless courses':handleAction(States.ALL_COURSES)}
              ],
                 'prepare':get_courses,
                 'kb_txt':"Welcome!",
                 'kb':handles.obj(home_kb)
      },

    States.ASSIGNMENTS:{'t':
                        handleString("*Your assignments for* %s",'course_name'),
                        'b':[{
                            'Show my progress':handleAction(States.PROGRESS)}]
                        #'fetch':True
       },
    States.SEND_ASSIGNMENT:{'t':
                handleString("Please send me your assignment for %s",'course_name'),
                     'b':[{
                         'Back':handleAction(States.HOME)}],
                     'react':handleAction(save_assignment,react_to='document'),
       },
    States.SUCCESS_ASSIGNMENT:{'t':
                     ("Success! Thank you for assignment"),
                     'b':[{
                         'Back home':handleAction(States.HOME)}]
       },
    States.PROGRESS:{'t':
                     handleString(("I'm sorry %s, but I don't know how to provide "
                      "progress reports - yet. I'm still learning. Meanwhile, "
                      "course instructor will help you out for sure."),'name'),
                     'b':[{
                         'Back home':handleAction(States.HOME)}]
       },
}

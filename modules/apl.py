from StateMachine import States
from frm import handles as handles
from DataBase import db

import pprint
pp = pprint.PrettyPrinter(indent=1)

handlePost =handles.post
handleAction = handles.action
handleString = handles.st

app_kb= [
    {'Home':handleAction(lambda i,s,**d:\
              (States.HOME if d.get('role')\
               else States.ALL_COURSES, d
             ))},
    {'Login':handleAction(States.TG)},
    {'Contact':handleAction(States.CONTACT)}
]

def format_lessons(lessons,personal=False):
    if lessons:
        text = "\n*Schedule:*\n"
        for lesson in lessons:
            lessonFull = db.get_lesson_by_id(lesson['lesson_id'])
            text += lessonFull['title']+'\n'
    else:
        text = "\nNo lessons yet"
    return text

def format_course(c):
    f = "%d/%m/%y"
    if c.get('from') and c.get('to'):
        fr = c['from'].strftime( f)
        to =c['to'].strftime( f)
    else:
        fr= 'n/a'
        to= 'n/a'
    return "*%s*\n*Dates*: %s-%s\n%s\n"%(
        c['title'],fr,to,
        c.get('description') or 'No description')

def generate_course_text(s,**d):
    pp.pprint(d.keys())
    course = db.get_course(d['course_id'])
    pp.pprint("***************")
    pp.pprint(course)

    text =''
    if d['role'] == 'student':
        text += 'Your course details:\n'
        text += format_course(course)
        try:
            text += format_lessons(course['lessons'],personal=True)
        except:
            text += "No scheduled lessons"

    if d['role'] == 'applicant':
        text += 'Course details:\n'
        text += format_course(course)
        try:
            text += format_lessons(course['lessons'])
        except:
            text += "No scheduled lessons"
    return text

UI={
    States.ALL_COURSES:{'t':'Have a look at our courses',
          'b': handlePost(lambda s,**d:\
                  (list(map(lambda course:\
                      {course.get('title') : handleAction(lambda i,s,**d:
                            (States.COURSE,\
                             # and also save course_id he picked
                             dict(d,**{'course_id':str(course.get('_id')),
                                       'course_name':course.get('title'),
                                       'role':'applicant'})\
                            ),
                            name=course.get('title')
                            )},\
                        d.get('courses',[]) or []))\
                    )
                ),
                 'prepare':lambda i,s,**d:\
                 dict(d,**{'courses':db.get_courses()}),
                 'kb_txt':"Welcome!",
                 'kb':handles.obj(app_kb)
      },
    States.COURSE:{'t':handlePost(generate_course_text),
                 'b':[
                   handles.choose('role',
                              {'student':{
                                  'Show assignments':handleAction(States.ASSIGNMENTS),
                                  'Submit assignment':handleAction(States.SEND_ASSIGNMENT),
                                  'My progress':handleAction(States.PROGRESS)
                              }},
                              default = [
                                  {'Apply':handleAction(States.APPLY) }
                              ]
                             )],
                 'prepare':lambda i,s,**d:\
                 dict(d,**{'lessons':db.get_lessons(d['course_id'])})
                  },
    States.APPLY:{'t': "Please type your first name",
                  'react':handleAction(lambda i,s,**d:\
                                (States.LNAME,dict(d,fname=i.text)),
                                 react_to='text')
       },
    States.LNAME:{'t': "Please type your last name",
                  'react':handleAction(lambda i,s,**d:\
                                (States.TG,dict(d,lname=i.text)),
                                 react_to='text')
       },
    States.PROGRESS:{'t':
                     handleString(("I'm sorry %s, but I don't know how to provide "
                      "progress reports yet. I'm still learning. Meanwhile, "
                      "course instructor will help you out for sure."),'name'),
                     'b':[{
                         'Back home':handleAction(States.HOME)}]
       },
}

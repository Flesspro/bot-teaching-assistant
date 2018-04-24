import config
import StateMachine
import telebot,shelve

from frm import TgFlow as Tgflow
#from modules import login, student, apply
from modules import login,home,misc,apl
from DataBase import db

data = {'av':2}

States =StateMachine.States

Tgflow.__init__(config.token)
Tgflow.set_default_state_data(States.START,data)

UI = dict({})
UI.update(login.UI)
UI.update(home.UI)
UI.update(misc.UI)
UI.update(apl.UI)

def start():
    Tgflow.start(UI)

Args = {}

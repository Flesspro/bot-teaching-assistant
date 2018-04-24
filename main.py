import json
import signal
from pymongo import MongoClient

# local modules
import config
import bot
from DataBase import db

def signal_handler(signal, frame):
    #Set KeyboardInterrupt handler to properly close all DBs
    logger.info('Signal caught, closing databases')
    print('Signal caught, closing databases')
    utils.close_storages()
    sys.exit(0)

if __name__=='__main__':
    bot.start()
    signal.signal(signal.SIGINT, signal_handler)

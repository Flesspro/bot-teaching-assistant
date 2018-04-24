#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# https://github.com/MasterGroosha/telegram-reminder-bot/blob/master/sender.py
"""
This script is triggered by "at" command (man at for more)
Even if bot has stopped, this script will run, because data is saved
in "atjobs" folder somewhere in system
"""
import telebot
import sys
from config import token, log_name
import logging

def sender(chat_id, message):
    """
    Send Message to a given Telegram chat (chat_id)
    """

    bot = telebot.TeleBot(token)
    logger = logging.getLogger(log_name)
    logging.basicConfig(filename=log_name + '.log',
                        format='[%(asctime)s] SENDER %(levelname)s - %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')
    logger.setLevel(logging.INFO)
    try:
        bot.send_message(chat_id, message, parse_mode = "Markdown")
        logger.info('Successfully sent message!')
    except Exception as ex:
        logger.error('Failed to send message: {0!s}'.format(str(ex)))

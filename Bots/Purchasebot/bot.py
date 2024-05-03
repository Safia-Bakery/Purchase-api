import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('.')

from telegram.constants import ParseMode
import os
from telegram import ReplyKeyboardMarkup,Update,WebAppInfo,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,PicklePersistence

)

from database import SessionLocal
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests
import database
from fastapi import Depends


db = SessionLocal()
backend_location = 'app/'



BOTTOKEN = os.environ.get('BOT_TOKEN')
url = f"https://api.telegram.org/bot{BOTTOKEN}/sendMessage"
LANGUAGE= range(1)
persistence = PicklePersistence(filepath='hello.pickle')
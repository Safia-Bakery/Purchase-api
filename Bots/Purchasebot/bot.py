import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('.')
import json
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
from Bots.Purchasebot.services import transform_list

from Bots.Purchasebot.queries import crud

FRONT_URL = 'https://super.purchase.safiabakery.uz/'

manu_buttons = [['Подать заявку','Моя заявки']]

db = SessionLocal()
backend_location = 'app/'



BOTTOKEN = os.environ.get('BOT_TOKEN')
url = f"https://api.telegram.org/bot{BOTTOKEN}/sendMessage"
NAME,PHONE,PASSWORD,MANU,ORDERLIST,CREATEORDER= range(6)
persistence = PicklePersistence(filepath='purchasepickle.pickle')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    """Starts the conversation and asks the user about their gender."""
    user_client = crud.get_client(db=db,id=update.message.from_user.id)
    if user_client:
        await update.message.reply_text('Manu',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU

    else:
        await update.message.reply_text("""Здравствуйте
    Это корпоративный бот компании Safia
    Пожалуйста введите пароль:
    если у вас её нет, обратитесь к системному администратору вашей компании""")

        return PASSWORD



async def password(update:Update,context:ContextTypes.DEFAULT_TYPE,db=db):
    input_text = update.message.text 
    if input_text == '5Thxk@t1':
        await update.message.reply_text('Пожалуйста напишите своё имя')
        return NAME
    else:
        await update.message.reply_text('Пароль не верный. Попробуйте еще раз')
        return PASSWORD
    

async def name(update:Update,context:ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    context.user_data['name']= input_text

    reply_keyboard = [[KeyboardButton(text='Поделиться', request_contact=True)]]
    await update.message.reply_text(
        f"📱 Какой у Вас номер, {input_text}? Отправьте или введите ваш номер телефона.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Поделиться контактом",resize_keyboard=True
        ),
    )
    return PHONE



async def phone(update:Update,context:ContextTypes.DEFAULT_TYPE,db=db):
    context.user_data['phone_number'] = update.message.contact.phone_number.replace('+','')
    crud.create_user(db=db,phone_number=context.user_data['phone_number'],name=context.user_data['name'],id=update.message.from_user.id)
    await update.message.reply_text("""Вы прошли регистрацию. Теперь можете оформлять заявки""",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return MANU


async def manu(update:Update,context:ContextTypes.DEFAULT_TYPE,db=db):
    input_text = update.message.text
    if input_text =='Подать заявку':
        await update.message.reply_text(
        f"Пожалуйста нажмите кнопку: Открыть меню",
        
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Открыть меню",
                web_app=WebAppInfo(url=f"{FRONT_URL}tg/select-branch?client_id={update.message.from_user.id}")
            ),resize_keyboard=True))
        return CREATEORDER
    
    elif input_text=='Моя заявки':
        await update.message.reply_text('My orders')
        order_list = crud.get_orders(db=db,id=None)
        reply_keyboard = transform_list(order_list,size=3,key='id')
        update.message.reply_text('Your orders', reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return  ORDERLIST



async def createorder(update:Update,context:ContextTypes.DEFAULT_TYPE,db=db):
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_text(f"можете оформлять заявки",reply_markup=ReplyKeyboardMarkup(keyboard=manu_buttons,resize_keyboard=True))
    return MANU



async def orderlist(update:Update,context:ContextTypes.DEFAULT_TYPE,db=db):
    input_data = update.message.text
    order_list = crud.get_orders(db=db,id=input_data)
    if order_list:
        text = ""
        text += f"№{order_list[0].id}\n"
        text +=f"Филиал: {order_list[0].branch.name}\n\n"
        text +='Товары:\n'
        for i in order_list[0].expendituretool:
            text += f"{i.tool.name} x {i.amount} шт"
    else:
        text = "None"
    await update.message.reply_text(text=text,reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))  
    return MANU






def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME:[MessageHandler(filters.TEXT,name)],
            PHONE:[MessageHandler(filters.CONTACT,phone)],
            PASSWORD:[MessageHandler(filters.TEXT,password)],
            MANU:[MessageHandler(filters.TEXT,manu)],
            ORDERLIST:[MessageHandler(filters.TEXT,orderlist)],
            CREATEORDER:[MessageHandler(filters.TEXT,createorder)]
            
           
        },
        fallbacks=[CommandHandler('start',start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,
        

    )
    application.add_handler(conv_handler)



    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
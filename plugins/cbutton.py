""" Create Buttons Through Bots """

# IMPROVED BY code-rgb
# By @krishna_singhal

from pyrogram.errors.exceptions.bad_request_400 import (
    UserIsBot, BadRequest, MessageEmpty)

from userge import userge, Config, Message, get_collection
from userge.utils import parse_buttons as pb
import re

BTN = r"\[([^\[]+?)\](\[buttonurl:(?:/{0,2})(.+?)(:same)?\])|\[([^\[]+?)\](\(buttonurl:(?:/{0,2})(.+?)(:same)?\))"
BTNX = re.compile(BTN)

@userge.on_cmd("cbutton", about={
    'header': "Create buttons Using bot",
    'description': "First Create a Bot via @Botfather and "
                   "Add bot token To Config Vars",
    'usage': "{tr}cbutton [reply to button msg]",
    'buttons': "<code>[name][buttonurl:link]</code> - <b>add a url button</b>\n"
               "<code>[name][buttonurl:link:same]</code> - "
               "<b>add a url button to same row</b>"})
async def create_button(msg: Message):
    """ Create Buttons Using Bot """
    if Config.BOT_TOKEN is None:
        await msg.err("First Create a Bot via @Botfather to Create Buttons...")
        return
    replied = msg.reply_to_message
    if not (replied and replied.text):
        await msg.err("Reply a text Msg")
        return
    text, buttons = pb(replied.text)
    try:
        await userge.bot.send_message(
            chat_id=msg.chat.id, text=text,
            reply_to_message_id=replied.message_id,
            reply_markup=buttons)
    except UserIsBot:
        await msg.err("oops, your Bot is not here to send Msg!")
    except BadRequest:
        await msg.err("Check Syntax of Your Message for making buttons!")
    except MessageEmpty:
        await msg.err("Message Object is Empty!")
    except Exception as error:
        await msg.edit(f"`Something went Wrong! 😁`\n\n**ERROR:** `{error}`")
    else:
        await msg.delete()


@userge.on_cmd("ibutton", about={
     'header': "Creates Button Via Inline bot in any chat",
     'flags': {
     "c": "replace all () bracket to [] "},
    'usage': "{tr}ibutton [ reply to message]\n"
              "{tr}ibutton -c [ reply to message]"})
async def inline_buttons(message: Message):
    replied = message.reply_to_message
    if not (replied and replied.text):
         await message.err("Reply a text Msg")
         return
    text = replied.text
    # Lmao Weird code but works xD
    if '-c' in message.flags:
        unmatch = re.sub(BTN, '', text)
        textx = ""
        for m in BTNX.finditer(text):
            if m.group(1):
                word = m.group(0)
            else:
                change = m.group(6).replace('(', '[').replace(')', ']')
                word = "[" + m.group(5) + "]"
                word += change
            textx += word 
        text = unmatch + textx
    BUTTON_BASE = get_collection("TEMP_BUTTON")
    BUTTON_BASE.insert_one({'msg_data': text})
    bot = await userge.bot.get_me()
    x = await userge.get_inline_bot_results(bot.username, "buttonnn")
    await userge.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id=x.results[1].id)
    await BUTTON_BASE.drop()
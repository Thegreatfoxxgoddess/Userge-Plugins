from google_trans_new import google_translator
from userge import Message, userge

translator = google_translator()


@userge.on_cmd(
    "rom",
    about={
        "header": "Romaji Converter",
        "usage": "reply to message or text after cmd",
        "examples": "{tr}rom こんばんは　or　{tr}reply to msg",
    },
)
async def romaji_(message: Message):
    x = str(message.input_str or message.reply_to_message.text)
    if not x:
        await message.err("No Input Found")
    else:
        y = x.split("\n")
        result = translator.translate(y, lang_src="ja", lang_tgt="en", pronounce=True)
        k = result[1]
        await message.reply(k.replace("', '", "\n").replace("['", "").replace("']", ""))
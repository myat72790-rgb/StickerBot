import os
import logging
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# =========================================================
# ဒီအောက်က နေရာမှာ BotFather ဆီကရတဲ့ Token ကို စာအုပ်ကွင်း ' ' ထဲ ထည့်ပါ
TOKEN = '8721156786:AAFq7y74PqmnUfpe4s9JL1NhxlGKNXkKdd8'
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ! ဓာတ်ပုံတစ်ပုံ ပို့ပေးပါ၊ Sticker အဖြစ် ပြန်ပြောင်းပေးပါ့မယ်။")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("ဓာတ်ပုံကို Sticker ပြောင်းနေပါတယ်၊ ခဏစောင့်ပါ...")
    
    # ဓာတ်ပုံ ဒေါင်းလုဒ်ဆွဲခြင်း
    photo_file = await update.message.photo[-1].get_file()
    input_path = "temp_photo.jpg"
    output_path = "sticker.webp"
    
    await photo_file.download_to_drive(input_path)

    # ဓာတ်ပုံကို Telegram Sticker Size (512x512, WEBP format) ပြောင်းခြင်း
    img = Image.open(input_path)
    img.thumbnail((512, 512))
    img.save(output_path, "WEBP")

    # Sticker ပြန်ပို့ပေးခြင်း
    await update.message.reply_sticker(sticker=open(output_path, 'rb'))
    await status_msg.delete()

    # ဖိုင်အဟောင်းများ ပြန်ရှင်းခြင်း
    if os.path.exists(input_path): os.remove(input_path)
    if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()
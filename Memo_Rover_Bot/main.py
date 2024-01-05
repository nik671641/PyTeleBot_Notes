import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL, Note

bot = Bot('6835721657:AAHvkOW686NtlUf1RLUrA9APmL-8xhdsINw')
dp = Dispatcher()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@dp.message(Command("start"))
async def cmd_add(message: Message):
    await message.answer(f"Hello {message.from_user.first_name} \n Я телеграмм бот для заметок \n /add-добавить заметку \n/getall-просмотреть все заметки ")



@dp.message(Command("add"))
async def cmd_add(message: types.Message, command: CommandObject):
    commands = command.args.split('\n')
    for cmd_text in commands:
        if cmd_text.startswith('/add'):
            note_text = cmd_text[len('/add'):].strip()

            if note_text:
                with SessionLocal() as db:
                    new_note = Note(text=note_text)
                    db.add(new_note)
                    db.commit()
                print(note_text)
            else:
                await message.answer(f"Заметка не добавлена")


@dp.message(Command("getall"))
async def get_all_notes(message: types.Message):

    with SessionLocal() as db:
        notes = db.query(Note).all()

    if notes:
        notes_text = "\n".join(note.text for note in notes)
        await message.answer(f"Ваши заметки:\n{notes_text}")
    else:
        await message.answer("У вас нет заметок.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
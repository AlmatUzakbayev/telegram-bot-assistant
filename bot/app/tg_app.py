import asyncio
import logging
import sys
from os import getenv
from pathlib import Path

import aiohttp

from pydub import AudioSegment
import speech_recognition as sr

from config import TELEGRAM_BOT_TOKEN

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, File
from pydub.utils import which
from aiogram.enums.content_type import ContentType

dp = Dispatcher()

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def _convert_audio_format(input_path: str, source_audio_format: str) -> str:
    """
    Convert an audio file to WAV format.
    Args:
        input_path: The input path of the audio file.
        source_audio_format: The format of the input audio file.
    Returns:
        The output path of the converted audio file.
    """
    AudioSegment.converter = "C:\\ffmpeg\\ffmpeg.exe"
    # AudioSegment.converter = which("ffmpeg")
    try:
        output_path = input_path.replace(f".{source_audio_format}", ".wav")
        audio = AudioSegment.from_file(input_path, format=source_audio_format)
        audio.export(output_path, format="wav", codec="pcm_s16le")
        print(f"Converted {input_path} to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error during conversion: {e}")


async def voice_to_text(voice_file_path: str) -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(voice_file_path) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language="ru-RU")  # Поддержка русского языка
    except Exception as e:
        print(f"Error during voice recognition: {e}")
        return "Ошибка при распознавании аудио"


async def download_audio(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}.ogg")

async def download_image(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}.jpg")


@dp.message(F.voice)
async def ask_chat_bot_voice(message: Message) -> None:
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = f"audio_files/{message.from_user.id}"

    file_name = f"{file_path}/{file_id}.ogg"

    await download_audio(file=file, file_name=file_id, path=file_path)

    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/chat/voice"
        async with session.post(url, json={"file_path": file_name}) as response:
            response_data = await response.text()
            await message.answer(response_data)

@dp.message(F.photo)
async def ask_chat_bot_photo(message: Message) -> None:
    photo_file = message.photo[-1].file_id
    new_file = await bot.get_file(photo_file)

    file_path = f"Image_files/{message.from_user.id}"
    file_name = f"{file_path}/{photo_file}.jpg"

    await download_image(file=new_file, file_name=photo_file, path=file_path)

    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/chat/image"
        async with session.post(url, json={"image_input": file_name}) as response:
            response_data = await response.text()
            await message.answer(response_data)



@dp.message()
async def ask_chat_bot(message: Message) -> None:
    # if message.text:
    user_text = message.text
    """
    # elif message.voice:
    #    file_id = message.voice.file_id
    #    file = await bot.get_file(file_id)
    #    file_path = f"audio_files/{message.from_user.id}"
    #
    #    file_name = f"{file_path}/{file_id}.ogg"
    #
    #    await download_audio(file=file, file_name=file_id, path=file_path)
    #
    #    # Скачиваем и конвертируем голосовое сообщение
    #    wav_path = _convert_audio_format(file_name, "ogg")
    #    if wav_path:
    #        user_text = await voice_to_text(wav_path)
    #        Path(wav_path).unlink()  # Удаляем WAV файл после обработки
    #    else:
    #        await message.answer("Ошибка при обработке голосового сообщения.")
    #        return
    # else:
    # await message.answer("Пожалуйста, отправьте текст или голосовое сообщение.")
    #   return
"""
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/chat/ask"
        async with session.post(url, json={"user_input": user_text}) as response:
            response_data = await response.text()
            await message.answer(response_data)


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

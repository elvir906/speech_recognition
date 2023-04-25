"""
Детектор команд будет направлять виртуальный автомобиль по командам
'налево', 'направо', 'назад', 'вперёд', 'поехали', 'стоп'
"""

import os

import pyaudio
from vosk import KaldiRecognizer, Model

if not os.path.exists("vosk-model-small-ru-0.22"):
    print(
        'Скачайте "vosk-model-small-ru-0.22" по ссылке '
        + 'https://alphacephei.com/vosk/models и '
        + 'распакуйте в текущюю директорию.'
    )
    exit(1)


model = Model(r"vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=16000
)
stream.start_stream()

movements = {
    'налево': 'машина поворачивает налево',
    'направо': 'машина поворачивает направо',
    'назад': 'машина начинает движение назад',
    'вперёд': 'машина начинает движение вперёд',
    'поехали': 'машина начинает движение вперёд',
    'стоп': 'машина останавливается'
}


def result(record):
    words = record.split()
    w = [x.replace('"', '') for x in words]
    try:
        movement = list(set(w) & movements.keys())
        return (movements.get(movement[0]))
    except Exception:
        res = ' '.join(words)
        if res != '{ "text" : "" }':
            return f"прозвучала неизвестная команда {res}"


while True:
    data = stream.read(16000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = result(rec.Result())
        if res is not None:
            print(res)

print(rec.FinalResult())

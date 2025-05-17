import os
from datetime import datetime as dt

def clean_logs():
    with open('logs.txt', 'w+') as f:
        f.write('')
    pass

if not os.path.isfile('logs.txt'):
    clean_logs()

def func_msg(msg):
    print(dt.now(), msg) 
    with open('logs.txt', mode='a', encoding='latin-1') as f:
        f.write(f'{dt.now()} {msg}\n')

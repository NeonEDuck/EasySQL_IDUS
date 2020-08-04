import os
import json
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.abspath( os.path.dirname(sys.executable) )
elif __file__:
    BASE_DIR = os.path.abspath( os.path.dirname(__file__) )

def save(setting):
    with open( os.path.join( BASE_DIR, 'sqlSetting.cfg' ), mode='w' ) as savf:
        savf.write( json.dumps(setting) )

def load():
    setting = {}
    if os.path.exists(os.path.join( BASE_DIR, 'sqlSetting.cfg' )):
        with open( os.path.join( BASE_DIR, 'sqlSetting.cfg' ), mode='r' ) as savf:
            setting = json.loads(savf.read())
    return setting
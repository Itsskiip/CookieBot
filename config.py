from IO import file_io
from discord.ext import commands

def save_config(): file_io('config.json', 'save', config)
def load_config(): return file_io('config.json', 'load')

config = load_config()
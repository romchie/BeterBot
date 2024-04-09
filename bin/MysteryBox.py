import random
import time
import discord
import json
from operator import itemgetter
import pprint

from pysondb import db

class MysteryBox:
    def __init__(self):
        self.INVENTORY_FILE = 'data/inventories.json'
        # self.client = client
        self.db = db.getDb('data/inventories.json')
        self.assault_rifles = ['AK47', 'AUG A1', 'FG42', 'M4A4', 'STG-44', 'M16-M', 'Famas F1']
        self.carbines = ['Gewer 43', 'M1A1 Carbine', 'M1 Garand', 'M14']
        self.smgs = ['AK-74u', 'MP40', 'MP5', 'PPSH', 'M1 Thompson', 'Type 100']
        self.lmgs = ['B.A.R', 'M1919 Browning', 'LSAT', 'MG42', 'RPK']
        self.shotguns = ['Sawed-Off', 'Model 680 Shotgun', 'Saiga-12', 'Trench Shotgun', 'Super-Shorty']
        self.snipers = ['Kar98k', 'PTRS-41']
        self.side_arms = ['B93 Raffica', 'M1911 Colt', '.357 Magnum', 'Mauser C96', 'Walther P99', 'Desert Eagle']
        self.specials = ['M2 Flamethrower', 'Panzerschrek', 'Raygun', 'Wunderwaffe DG-2']
        self.melees = ['Knife', 'Bowie Knife', 'Oar', 'Frying Pan']
        self.items = self.assault_rifles + self.carbines + self.smgs + self.lmgs + self.shotguns + self.snipers + self.side_arms + self.specials + self.melees

    def readDataBase(self) -> any:
        with open(self.INVENTORY_FILE, 'r') as file:
            return json.load(file)
        
    def writeDataBase(self, data) -> None:
        with open(self.INVENTORY_FILE, 'w') as file:
            json.dump(data, file, indent=4)

    def clearDataBase(self, t:str='all'):
        """Types: `all`, `guns`, `mpoints`"""
        db = self.readDataBase()
        if t == 'all':
            print('clearing all')
            db['users'] = {}
        elif t == 'guns':
            print('clearing guns')
            for user in db['users']:
                db['users'][user]['guns'] = []
        elif t == 'mpoints':
            print('clearing michael points')
            for user in db['users']:
                user['mpoints'] = 0
        self.writeDataBase(db)

    def addUser(self, user: discord.User, database) -> None:
        if str(user) not in database['users']:
            database['users'][str(user)] = {
                "id": user.id,
                "mpoints": 0,
                "guns": [],
            }

    def spinBox(self, user: discord.User) -> str:
        db = self.readDataBase()
        self.addUser(user, db)
        item = random.choice(self.items)
        if item in db['users'][str(user)]['guns']:
            return f'You rolled a {item}... but you\'ve already GYAT one!'
        db['users'][str(user)]['guns'].append(item)
        self.writeDataBase(db)
        return f'You rolled a {item}!'
    
    def showInventory(self, user: discord.User) -> str:
        db = self.readDataBase()
        if str(user) not in db['users'] or len(db['users'][str(user)]['guns']) == 0:
            return f'ya shit\'s EMPTY'
        user_guns = db['users'][str(user)]['guns']
        gun_list = '```'
        for gun in user_guns:
            gun_list += f'• {gun}\n'
        gun_list += '```'
        return f'**{str(user)}\'s Inventory: ({len(user_guns)}/{len(self.items)} collected)**\n{gun_list}'

    def getMichaelPoints(self, user: discord.User) -> int:
        db = self.readDataBase()
        self.addUser(user, db)
        michael_points = db['users'][str(user)]['mpoints']
        return michael_points
    
    def updateMichaelPoints(self, user: discord.User, val: int) -> str:
        db = self.readDataBase()
        self.addUser(user, db)
        db['users'][str(user)]['mpoints'] += val
        self.writeDataBase(db)
        if val > 0:
            return f'+{val} Michael Points'
        elif val < 0:
            return f'{val} Michael Points'

    # TODO
    def showLeaderboard(self) -> str:
        db = self.readDataBase()
        mpoints_arr = []
        for data in list(db['users'].items()):
            mpoints_arr.append({'user': data[0], 'mpoints': data[1]['mpoints']})
        sorted_order = sorted(mpoints_arr, key=lambda x: x['mpoints'], reverse=True)
        leaderboard_str = '**Michael Points Leaderboard**\n```'
        rank = 1
        for data in sorted_order:
            username = data['user']
            mpoints = data['mpoints']
            leaderboard_str += f'{rank}) {mpoints} Mpts - {username}\n'
            rank += 1
        leaderboard_str += '```'
        return leaderboard_str

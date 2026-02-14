import json
import os
import sys


def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


class DataManager:
    def __init__(self):
        base_path = get_base_path()
        self.file_path = os.path.join(base_path, 'game_data.json')
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except:
                return {'total_coins': 0, 'high_score': 0}
        return {'total_coins': 0, 'high_score': 0}

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

    def add_coins(self, amount):
        self.data['total_coins'] += amount
        self.save_data()

    def get_total_coins(self):
        return self.data.get('total_coins', 0)

    def update_high_score(self, score):
        if score > self.data.get('high_score', 0):
            self.data['high_score'] = score
            self.save_data()

    def get_high_score(self):
        return self.data.get('high_score', 0)


data_manager = DataManager()
import random
import re
import hashlib
from typing import List, Dict

class NicknameGenerator:
    def __init__(self):
        self.adjectives = [
            "Shadow", "Dark", "Ghost", "Phantom", "Steel", "Iron", "Golden",
            "Silent", "Swift", "Deadly", "Epic", "Mystic", "Furious", "Royal",
            "Lunar", "Solar", "Cyber", "Neon", "Void", "Blood", "Night", "Wolf"
        ]
        
        self.nouns = [
            "Hunter", "Killer", "Slayer", "Warrior", "Assassin", "Reaper",
            "Soldier", "Guardian", "Wraith", "Spectre", "Ninja", "Samurai",
            "Viking", "Knight", "Dragon", "Wolf", "Eagle", "Tiger", "Phoenix",
            "Storm", "Blade", "Arrow", "Bullet", "Sniper", "Predator"
        ]
        
        self.prefixes = ["xX", "Pro", "Mr", "Lord", "King", "Sir", "Dr"]
        self.suffixes = ["Xx", "YT", "TV", "GG", "OP", "God", "Master"]
        
        self.generated_hashes = set()
    
    def generate_unique_hash(self, nickname: str, game: str) -> str:
        combined = f"{game}:{nickname.lower()}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def check_game_rules(self, nickname: str, game_rules: Dict) -> bool:
        if len(nickname) > game_rules["max_length"]:
            return False
        
        if re.search(game_rules["forbidden_chars"], nickname):
            return False
        
        if not nickname.strip():
            return False
        
        return True
    
    def generate_simple(self, game_rules: Dict) -> str:
        adj = random.choice(self.adjectives)
        noun = random.choice(self.nouns)
        nickname = f"{adj}{noun}"
        
        if random.random() > 0.7:
            nickname += str(random.randint(1, 999))
        
        return nickname
    
    def generate_with_symbols(self, game_rules: Dict) -> str:
        adj = random.choice(self.adjectives)
        noun = random.choice(self.nouns)
        
        if "underscore" in game_rules["allowed_patterns"]:
            separator = "_"
        elif "dash" in game_rules["allowed_patterns"]:
            separator = "-"
        elif "dot" in game_rules["allowed_patterns"]:
            separator = "."
        else:
            separator = ""
        
        nickname = f"{adj}{separator}{noun}"
        
        if random.random() > 0.5:
            if random.random() > 0.5:
                nickname = random.choice(self.prefixes) + nickname
            else:
                nickname = nickname + random.choice(self.suffixes)
        
        return nickname
    
    def generate_number_style(self, game_rules: Dict) -> str:
        adj = random.choice(self.adjectives)
        noun = random.choice(self.nouns)
        
        leet_dict = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0',
            's': '5', 't': '7', 'l': '1', 'z': '2'
        }
        
        combined = adj + noun
        nickname = ""
        for char in combined.lower():
            if char in leet_dict and random.random() > 0.7:
                nickname += leet_dict[char]
            else:
                nickname += char
        
        return nickname.title()
    
    def generate(self, game: str, game_rules: Dict, user_id: int, max_attempts: int = 100) -> List[str]:
        results = []
        attempts = 0
        
        while len(results) < 5 and attempts < max_attempts:
            attempts += 1
            
            style = random.choice([
                self.generate_simple,
                self.generate_with_symbols,
                self.generate_number_style
            ])
            
            nickname = style(game_rules)
            
            if not self.check_game_rules(nickname, game_rules):
                continue
            
            nick_hash = self.generate_unique_hash(nickname, game)
            if nick_hash in self.generated_hashes:
                continue
            
            self.generated_hashes.add(nick_hash)
            results.append(nickname)
        
        return results
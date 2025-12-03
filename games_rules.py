GAMES_RULES = {
    "PUBG MOBILE": {
        "max_length": 15,
        "forbidden_chars": r"[!@#$%^&*()+=<>?/\|{}~`]",
        "allowed_patterns": ["letters", "numbers", "underscore"],
        "special_rules": "Нельзя использовать пробелы"
    },
    "Standoff 2": {
        "max_length": 20,
        "forbidden_chars": r"[!@#$%^&*()+=<>?/\|{}~`\s]",
        "allowed_patterns": ["letters", "numbers", "underscore", "dot"],
        "special_rules": "Разрешены точки и подчеркивания"
    },
    "Roblox": {
        "max_length": 20,
        "forbidden_chars": r"[<>/\\|{}]",
        "allowed_patterns": ["letters", "numbers", "underscore", "spaces"],
        "special_rules": "Можно использовать пробелы"
    },
    "Call of Duty": {
        "max_length": 16,
        "forbidden_chars": r"[<>/\\|{}]",
        "allowed_patterns": ["letters", "numbers", "underscore", "dash"],
        "special_rules": "Можно использовать дефисы"
    },
    "Arena Breakout": {
        "max_length": 12,
        "forbidden_chars": r"[!@#$%^&*()+=<>?/\|{}~`\s]",
        "allowed_patterns": ["letters", "numbers"],
        "special_rules": "Только буквы и цифры"
    },
    "Black Russia": {
        "max_length": 15,
        "forbidden_chars": r"[!@#$%^&*()+=<>?/\|{}~`]",
        "allowed_patterns": ["letters", "numbers", "underscore"],
        "special_rules": "Без специальных символов"
    }
}
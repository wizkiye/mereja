import questionary

FOREX_URL = "https://market.nbebank.com/market/banks/index.php"
SPINNERS = [
    "dots",
    "dots2",
    "dots3",
    "dots4",
    "dots5",
    "dots6",
    "dots7",
    "dots8",
    "dots9",
    "dots10",
    "dots11",
    "dots12",
    "dots8Bit",
    "line",
    "line2",
    "pipe",
    "simpleDots",
    "simpleDotsScrolling",
    "star",
    "star2",
    "flip",
    "hamburger",
    "growVertical",
    "growHorizontal",
    "balloon",
    "balloon2",
    "noise",
    "bounce",
    "boxBounce",
    "boxBounce2",
    "triangle",
    "arc",
    "circle",
    "squareCorners",
    "circleQuarters",
    "circleHalves",
    "squish",
    "toggle",
    "toggle2",
    "toggle3",
    "toggle4",
    "toggle5",
    "toggle6",
    "toggle7",
    "toggle8",
    "toggle9",
    "toggle10",
    "toggle11",
    "toggle12",
    "toggle13",
    "arrow",
    "arrow2",
    "arrow3",
    "bouncingBar",
    "bouncingBall",
    "smiley",
    "monkey",
    "hearts",
    "clock",
    "earth",
    "material",
    "moon",
    "runner",
    "pong",
    "shark",
    "dqpb",
    "weather",
    "christmas",
    "grenade",
    "point",
    "layer",
    "betaWave",
    "aesthetic",
]
STYLE = questionary.Style(
    [
        ("qmark", "fg:red bold"),
        ("question", "fg:yellow bold"),
        ("highlighted", "fg:#673AB7 bold"),
        ("answer", "fg:#2196f3 bold"),
        ("pointer", "fg:#27781e bold"),
        # ("highlighted", "fg:#27781e bold"),
        # ("selected", "fg:#cc5454 bold"),
        ("separator", "italic fg:#7c7d6b"),
        ("instruction", "fg:#f02634"),
        ("disabled", "fg:#858585 italic"),
        ("qmark", "fg:#673ab7 bold"),
        ("text", "fg:#68687d"),
    ]
)
QUESTIONS = [
    {
        "type": "select",
        "name": "answer",
        "message": "What do you want to do?",
        "choices": [
            "📈 Forex",
            "📝 News",
            "💼 Jobs",
            "🛍 Marketplace",
            "💳 Telebirr",
            "🛑 Exit",
        ],
    },
    {
        "type": "select",
        "name": "forex_choice",
        "message": "What do you want to do?",
        "choices": [
            "📈 Get forex",
            "📈 🚦 Get forex Live",
            "📂 Export forex data",
            "🔙 Back",
        ],
        "qmark": "📈",
        "when": lambda answers: answers.get("answer") == "📈 Forex",
    },
    {
        "type": "select",
        "name": "choice",
        "message": "What do you want to do with news?",
        "choices": ["📝 Get latest news", "🔍 Search for news", "🔙 Back"],
        "qmark": "📝",
        "when": lambda answers: answers.get("answer") == "📝 News",
    },
    {
        "type": "select",
        "name": "choice",
        "message": "What do you want to do with jobs?",
        "choices": ["Get latest jobs", "🔍 Search for jobs", "🔙 Back"],
        "qmark": "💼",
        "when": lambda answers: answers.get("answer") == "💼 Jobs",
    },
    {
        "type": "select",
        "name": "choice",
        "message": "What do you want to do with marketplace?",
        "choices": ["📈 Get trending products", "🔍 Search for products", "🔙 Back"],
        "qmark": "🛍",
        "when": lambda answers: answers.get("answer") == "🛍 Marketplace",
    },
    {
        "type": "select",
        "name": "telebirr_choice",
        "message": "What do you want to do with telebirr?",
        "choices": ["💳 Transaction Details", "📂 Export transaction data", "🔙 Back"],
        "qmark": "💳",
        "when": lambda answers: answers.get("answer") == "💳 Telebirr",
    },
    {
        "type": "text",
        "name": "transaction_id",
        "message": "💳 Enter your transaction ID:",
        "when": lambda answers: answers.get("telebirr_choice")
        in ["💳 Transaction Details", "📂 Export transaction data"],
    },
    {
        "type": "confirm",
        "name": "exit",
        "message": "Are you sure you want to exit?",
        "default": True,
        "when": lambda answers: answers.get("answer") == "🛑 Exit",
    },
    {
        "type": "text",
        "name": "search",
        "message": "Enter your search query:",
        "when": lambda answers: "Search" in answers.get("choice", ""),
    },
    {
        "type": "text",
        "name": "path",
        "message": "Enter the path to save the file:",
        "when": lambda answers: answers.get("forex_choice") in ["📂 Export forex data"]
        or answers.get("telebirr_choice") in ["📂 Export transaction data"],
        "validate": lambda val: (val and val.endswith(".json"))
        or "Path must end with .json",
    },
    {
        "type": "text",
        "name": "page",
        "message": "Enter the page number:",
        "when": lambda answers: answers.get("choice")
        in [
            "Get latest jobs",
            "📝 Get latest news",
            "📈 Get trending products",
            "🔍 Search for products",
        ],
        "validate": lambda val: val.isdigit() or "Page number must be a number",
        "filter": lambda val: int(val),
        "default": "1",
    },
]

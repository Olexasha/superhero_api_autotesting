DATA_FOR_POST_CHARACTER_BY_BODY = [
    {
        "education": "High school (unfinished)",
        "height": 180,
        "identity": "Publicly known",
        "name": "Hawkeye",
        "universe": "Marvel Universe",
        "weight": 87
    },
    {
        "education": "University",
        "height": 178,
        "identity": "Secret",
        "name": "Spider-Man",
        "other_aliases": "Daily Bugle, Fantastic Four, New Avengers, Secret Avengers",
        "universe": "Marvel Universe, Earth-TRN701, Earth-13",
        "weight": 76.1
    },
    {
        "education": "University",
        "height": 185.0,
        "identity": "Known as Tony Kark",
        "name": "Iron-Man",
        "universe": "Marvel Universe, Earth-199999, Earth-616",
        "weight": 90
    }
]

DATA_CHANGED_NAME_FOR_PUT = [{"result": {
    "education": "University",
    "height": 178,
    "identity": "Absolutely not Spider-Man",
    "name": "Spider-Man",
    "other_aliases": "Daily Bugle, Fantastic Four, New Avengers, Secret Avengers",
    "universe": "Marvel Universe, Earth-TRN701, Earth-13",
    "weight": 76.1
}}]

DATA_FOR_MANY_CHARS_MANIPULATIONS = [
    {
        "result": {
            "education": "Unrevealed",
            "height": 170,
            "identity": "Secret (known to the U.S. government)",
            "name": "Avalanche",
            "other_aliases": "Jon Bloom",
            "universe": "Marvel Universe",
            "weight": 87.75
        }
    },
    {
        "result": {
            "education": "Unrevealed",
            "height": 218,
            "identity": "Secret, known to select underworld crime bosses.",
            "name": "Russian",
            "other_aliases": "The Ivan",
            "universe": "Marvel Universe",
            "weight": 257.85
        }
    },
    {
        "result": {
            "education": "Unrevealed",
            "height": 198,
            "identity": "Known to various government officials",
            "name": "Sabretooth (House of M)",
            "other_aliases": "Der Schlächter (\"The Butcher\" in German), Slasher, El Tigre, others",
            "universe": "Marvel Universe",
            "weight": 123.75
        }
    }
]

WRONG_ORDER_OF_FIELDS = {"result": {
    "identity": "Secret, known to select underworld crime bosses.",
    "height": 218,
    "universe": "Marvel Universe",
    "education": "Unrevealed",
    "other_aliases": "The Ivan",
    "weight": 257.85,
    "name": "Belorussian"
}}

WRONG_ORDER_OF_FIELDS_EXPECTED = {'result': {
    'education': 'Unrevealed',
    'height': 218.0,
    'identity': 'Secret, known to select underworld crime bosses.',
    'name': 'Belorussian',
    'other_aliases': 'The Ivan',
    'universe': 'Marvel Universe',
    'weight': 257.85}}

MIN_LENGTH_FIELD = {"result": {
    "education": "University",
    "height": 178,
    "identity": "Secret",
    "name": "",
    "other_aliases": "Daily Bugle, Fantastic Four, New Avengers, Secret Avengers",
    "universe": "Marvel Universe, Earth-TRN701, Earth-13",
    "weight": 76.1
}}

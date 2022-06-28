SCHEMA = {
        "id": "http://json-schema.org/draft-04/schema#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Tests the received fields for some checks",
        "type": "object",
        "properties": {
            "education": {
                "description": "Identifies hero's education",
                "type": "string", "minLength": 1, "maxLength": 350},
            "height": {
                "description": "Identifies hero's height",
                "type": "number", "minimum": 30, "maximum": 500},
            "identity": {
                "description": "Identifies hero's identity",
                "type": "string", "minLength": 1, "maxLength": 350},
            "name": {
                "description": "Identifies hero's name",
                "type": "string", "minLength": 1, "maxLength": 350},
            "other_aliases": {
                "description": "Identifies hero's aliases",
                "type": "string", "minLength": 1, "maxLength": 350},
            "universe": {
                "description": "Identifies hero's universes",
                "type": "string", "minLength": 1, "maxLength": 350},
            "weight": {
                "description": "Identifies hero's weight",
                "type": "number", "minimum": 2, "maximum": 1500}},
        "required": ["name"]
}
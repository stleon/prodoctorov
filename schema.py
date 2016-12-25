import json

from jsonschema import validate

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "profession": {
            "type": "string"
        },
        "grade": {
            "type": "string"
        },
        "category": {
            "type": "string"
        },
        "experience": {
            "type": "string"
        },
        "rating": {
            "type": "string"
        },
        "recommend": {
            "type": "number"
        },
        "effectiveness": {
            "type": "number"
        },
        "informing": {
            "type": "number"
        },
        "quality": {
            "type": "number"
        },
        "attitude": {
            "type": "number"
        },
        "sms": {
            "type": "object",
            "properties": {
                "plus": {
                    "type": "integer"
                },
                "minus": {
                    "type": "integer"
                }
            },
            "required": ["plus", "minus"]
        },
        "views": {
            "type": "integer"
        },
        "info": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string"
                },
                "company": {
                    "type": "string"
                }
            },
            "required": ["address", "company"]
        }
    },
    "required": [
        "name", "profession", "grade", "category", "experience", "rating",
        "recommend", "effectiveness", "informing", "quality", "attitude",
        "sms", "views", "info"
    ]
}


def get_doctors():
    with open('doctors.json') as f:
        return json.load(f)


if __name__ == '__main__':
    for doctor in get_doctors():
        validate(doctor, schema)

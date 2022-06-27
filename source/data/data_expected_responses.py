RESPONSE_WRONG_FIELD = {"error": "name: ['Missing data for required field.'], weight: ['Not a valid number.']"}

RESPONSE_FULL_DB = {"error": "Collection can't contain more than 500 items"}

RESPONSE_NO_SUCH_NAME_CHARACTER = {"error": "No such name"}

RESPONSE_NEEDED_AUTHORIZATION = {"error": "You have to login with proper credentials"}

RESPONSE_SLICE_LOGIN = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>500 Internal Server ' \
              'Error</title>\n<h1>Internal Server Error</h1>\n<p>The server encountered an internal error and was ' \
              'unable to complete your request.  Either the server is overloaded or there is an error in the ' \
              'application.</p>\n'

RESPONSE_MIN_LENGTH = {'error': "name: ['Length must be between 1 and 350.']"}

RESPONSE_INVALID_INPUT = {'error': "_schema: ['Invalid input type.']"}

RESPONSE_MISSING_REQUIRED_FIELD = {'error': "name: ['Missing data for required field.']"}

RESPONSE_WRONG_ORDER_OF_FIELDS = {"error": "Payload must be a valid json"}
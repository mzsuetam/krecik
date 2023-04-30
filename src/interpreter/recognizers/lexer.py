from antlr.KrecikLexer import KrecikLexer
from interpreter.recognizers.syntax_error_listener import RecognizerWithCustomListener


class CustomLexer(KrecikLexer, RecognizerWithCustomListener):
    pass

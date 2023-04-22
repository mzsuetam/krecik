from antlr.KrecikLexer import KrecikLexer
from interpreter.syntax_error_listener import RecognizerWithCustomListener


class CustomLexer(KrecikLexer, RecognizerWithCustomListener):
    pass

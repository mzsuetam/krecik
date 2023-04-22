from antlr.KrecikParser import KrecikParser
from interpreter.syntax_error_listener import RecognizerWithCustomListener


class CustomParser(KrecikParser, RecognizerWithCustomListener):
    pass

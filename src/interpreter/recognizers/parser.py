from antlr.KrecikParser import KrecikParser
from interpreter.recognizers.syntax_error_listener import RecognizerWithCustomListener


class CustomParser(KrecikParser, RecognizerWithCustomListener):
    pass

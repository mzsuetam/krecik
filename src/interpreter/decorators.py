from typing import TYPE_CHECKING

from interpreter.exceptions import KrecikException

if TYPE_CHECKING:
    from typing import Any, Callable
    from antlr4 import ParserRuleContext
    from interpreter.visitor.visitor import Visitor


def handle_exception(method: "Callable") -> "Callable":
    def inner(visitor_reference: "Visitor", ctx: "ParserRuleContext") -> "Any":
        try:
            return method(visitor_reference, ctx)
        except KrecikException as exc:
            exc.inject_context_to_exc(ctx)
            raise exc

    return inner

from unittest.mock import Mock, create_autospec

import pytest

from board.board import Board
from display.board_publisher import BoardPublisher, EventType


@pytest.fixture()
def board_publisher_mock() -> Mock:
    return create_autospec(BoardPublisher)


def check_publisher_notify(
    board_publisher_mock: Mock,
    event_type: EventType,
    should_notify: bool = True,
) -> bool:
    try:
        if not should_notify:
            board_publisher_mock.notify.assert_not_called()
            return True
        board_publisher_mock.notify.assert_called_once_with(event_type)
        return True
    except AssertionError:
        return False

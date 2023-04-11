import pytest

from board.krecik import Krecik
from board.krecik import Position as Pos
from board.krecik import Rotation as Rot


@pytest.mark.parametrize(
    ("initial_position", "initial_rotation", "expected_position"),
    [
        (Pos(col=0, row=0), Rot.N, Pos(col=0, row=-1)),
        (Pos(col=0, row=0), Rot.E, Pos(col=1, row=0)),
        (Pos(col=0, row=0), Rot.S, Pos(col=0, row=1)),
        (Pos(col=0, row=0), Rot.W, Pos(col=-1, row=0)),
        (Pos(col=5, row=-8), Rot.N, Pos(col=5, row=-9)),
        (Pos(col=5, row=-8), Rot.E, Pos(col=6, row=-8)),
        (Pos(col=5, row=-8), Rot.S, Pos(col=5, row=-7)),
        (Pos(col=5, row=-8), Rot.W, Pos(col=4, row=-8)),
    ],
)
def test_krecik_next_position(
    initial_position: Pos,
    initial_rotation: Rot,
    expected_position: Pos,
) -> None:
    krecik = Krecik(
        position=initial_position,
        rotation=initial_rotation,
    )
    pos = krecik.next_position()
    assert pos == expected_position


@pytest.mark.parametrize(
    ("initial_rotation", "rotate_number", "expected_rotation"),
    [
        (Rot.N, -1, Rot.W),
        (Rot.N, 0, Rot.N),
        (Rot.N, 1, Rot.E),
        (Rot.N, 2, Rot.S),
        (Rot.N, 3, Rot.W),
        (Rot.N, 4, Rot.N),
        (Rot.N, 5, Rot.E),
        (Rot.E, -1, Rot.N),
        (Rot.E, 0, Rot.E),
        (Rot.E, 1, Rot.S),
        (Rot.E, 2, Rot.W),
        (Rot.E, 3, Rot.N),
        (Rot.E, 4, Rot.E),
        (Rot.E, 5, Rot.S),
    ],
)
def test_krecik_rotate(
    initial_rotation: Rot,
    rotate_number: int,
    expected_rotation: Rot,
) -> None:
    krecik = Krecik(rotation=initial_rotation)
    krecik.rotate(rotate_number)
    assert krecik.rotation == expected_rotation

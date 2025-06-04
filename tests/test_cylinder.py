import pytest

from cylinder import Cylinder


def test_2_position_transitions():
    cyl = Cylinder(mode="2-position")

    assert cyl.position == Cylinder.POS_RETRACTED
    assert cyl.get_position_signals() == {
        Cylinder.POS_RETRACTED: True,
        Cylinder.POS_EXTENDED: False,
    }

    cyl.extend()
    assert cyl.position == Cylinder.POS_EXTENDED
    assert cyl.get_position_signals() == {
        Cylinder.POS_RETRACTED: False,
        Cylinder.POS_EXTENDED: True,
    }

    cyl.retract()
    assert cyl.position == Cylinder.POS_RETRACTED

    with pytest.raises(ValueError):
        cyl.intermediate()


def test_3_position_transitions():
    cyl = Cylinder(mode="3-position")

    cyl.extend()
    assert cyl.position == Cylinder.POS_EXTENDED
    assert cyl.get_position_signals() == {
        Cylinder.POS_RETRACTED: False,
        Cylinder.POS_EXTENDED: True,
        Cylinder.POS_INTERMEDIATE: False,
    }

    cyl.intermediate()
    assert cyl.position == Cylinder.POS_INTERMEDIATE
    assert cyl.get_position_signals() == {
        Cylinder.POS_RETRACTED: False,
        Cylinder.POS_EXTENDED: False,
        Cylinder.POS_INTERMEDIATE: True,
    }

    cyl.retract()
    assert cyl.position == Cylinder.POS_RETRACTED
    assert cyl.get_position_signals() == {
        Cylinder.POS_RETRACTED: True,
        Cylinder.POS_EXTENDED: False,
        Cylinder.POS_INTERMEDIATE: False,
    }

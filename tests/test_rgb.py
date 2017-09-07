from nose.tools import *
from uvhue.rgb import *

def test_rgb_to_xy():
    assert_equal(rgb_to_xy((255, 0, 100)), (0.6464418804969204, 0.22715583071502674))

def test_rgb_to_decimal():
    assert_equal(rgb_to_decimal((255, 0, 100)), (1.0, 0.0, 0.39215686274509803))

def test_gamma_correct():
    assert_equal(gamma_correct(0.5), 0.21404114048223255)
    assert_equal(gamma_correct(0.03), 0.0023219814241486067)

def test_decimal_to_xyz():
    rgb = rgb_to_decimal((255, 0, 100))
    rgb = gamma_correct_rgb(rgb)

    assert_equal(decimal_to_xyz(rgb), (0.67504511375299, 0.23720683670248477, 0.13199523420106749))

def test_xyz_to_xy():
    assert_equal(xyz_to_xy((0.67504511375299, 0.23720683670248477, 0.13199523420106749)), (0.6464418804969204, 0.22715583071502674))

def test_is_grey():
    assert_equal(is_grey((100, 100, 100)), True)
    assert_equal(is_grey((101, 100, 99)), True)
    assert_equal(is_grey((110, 100, 90)), True)
    assert_equal(is_grey((111, 100, 90)), False)
    assert_equal(is_grey((121, 100, 100)), False)

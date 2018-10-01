#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `langevin` package."""
import sys
sys.path.append('../')

import unittest
import pytest

from click.testing import CliRunner

from langevin import langevin
from langevin import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'langevin.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

class test_ckhr(unittest.TestCase):
    def test_calc_vis_force(self):
        velocity = 10
        res = langevin.calc__vis_force(velocity)
        assert res == -10

    def test_cal_rand_force(self):
        #self.assertEqual(langevin.calc_rand_force(), 1)
        # assert travis_test.c == 9

        pass


if __name__ == '__main__':
    unittest.main()


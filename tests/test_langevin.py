#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `langevin` package."""
import sys
sys.path.append('../')

import unittest
import pytest
import random
import numpy as np

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
        #unittest for the function calc_vis_force(velocity)
        velocity = 10
        res = langevin.calc__vis_force(velocity)
        assert res == -10

    def test_cal_rand_force(self):
        #unittest for the function calc_rand_force()
        # pute seed as zero 
        random.seed(0)
        mean = 0.0
        variance = 2 #default value of variance in project
        standard_deviation = np.sqrt(variance)
        # generate a random number with the calculated mean and standard deviation
        zeta = random.normalvariate(mean,standard_deviation)

        #again put the same seed as zero
        random.seed(0)
        self.assertEqual(langevin.calc_rand_force(), zeta)

    def test_acc(self):
        #unittest for the function acc(velocity)
        random.seed(0)
        velocity = 1
        acc = langevin.calc__vis_force(velocity) + langevin.calc_rand_force()
        random.seed(0)
        self.assertEqual(langevin.acc(velocity), acc)

    def test_update_velocity(self):
        #unittest for the function update_velocity
        velocity = 0
        dt = 0.1
        random.seed(0)
        #calculate updated velocity from RK4 method
        k1 = dt * langevin.acc(velocity)
        k2 = dt * langevin.acc(velocity + k1/2)
        k3 = dt * langevin.acc(velocity * k2/2)
        k4 = dt * langevin.acc(velocity + k3)

        updated_velocity = velocity + 1/6 * k1 + 1/3 * k2  +1/3 * k3 + 1/6 * k4

        random.seed(0)
        self.assertEqual(langevin.update_velocity(velocity), updated_velocity)


    def test_update_pos(self):
        #unittest to test function update_pso(velocity)
        velocity = 0
        dt = 0.1
        position = 1    
        #calculate updated position from RK4 method

        k1 = dt * velocity
        k2 = dt * velocity
        k3 = dt * velocity
        k4 = dt * velocity

        updated_position = position + 1/6 * k1 + 1/3 * k2  +1/3 * k3 + 1/6 * k4
        self.assertEqual(langevin.update_pos(velocity,position), updated_position)

    def test_main(self):
        #unittest to test main() funciton

        # this checks if the files are written or not

        import os
        #call main function from the project
        langevin.main()
        
        #Checking if the finalposition files has generated
        finalpos = os.path.isfile("../langevin/finalpositions.txt")
        self.assertEqual(finalpos,True)

        #Checking if the historgram.png files has generated
        hist = os.path.isfile("../langevin/histogram.png")
        self.assertEqual(hist,True)

        #Checking if the trajectory.png file has generated
        trajec = os.path.isfile("../langevin/trajectory.png")
        self.assertEqual(trajec,True)


        
        


if __name__ == '__main__':
    unittest.main()


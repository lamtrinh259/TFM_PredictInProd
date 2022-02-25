# pylint: disable-all

import numpy
import pandas as pd
import unittest
from TaxiFareModel.data import get_data_from_gcp

def this_run():
    print('This runs!')


def test_get_data():
    assert len(get_data_from_gcp()) > 0

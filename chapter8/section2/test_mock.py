# coding=utf-8
import unittest
import pytest

import mock

import client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.result = {'review': {'author': 'dongwm'}}

    def test_request(self):
        api_result = mock.Mock(return_value=self.result)
        client.api_request = api_result
        self.assertEqual(client.get_review_author(
            'http://api.dongwm.com/review/123'), 'dongwm')


def test_side_effect():
    mock_ = mock.Mock()

    def effect(*args, **kwargs):
        raise IndexError

    mock_.side_effect = effect
    with pytest.raises(IndexError):
        mock_(1, 2, a=3)

    side_effect = lambda value, length=1: value * length
    mock_.side_effect = side_effect
    assert mock_(1) == 1
    assert mock_('*', 2) == '**'

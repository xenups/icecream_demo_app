import rootpath
import unittest

rootpath.append()
from ICECREAM.test import Client


class TestFunctions(unittest.TestCase):
    def test_add_room(self):
        response = Client().get_api('/rooms')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()

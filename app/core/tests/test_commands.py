from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):

    def test_wait_for_db_ready_method_1(self):
        """Tests waiting for db when db is available with patch function"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('django.db.utils.ConnectionHandler.__getitem__', return_value=True)
    def test_wait_for_db_ready_method_2(self, mock_db_handler):
        """Test waiting for db when db is available with patch decorator"""
        call_command('wait_for_db')
        self.assertEqual(mock_db_handler.call_count, 1)

    @patch('django.db.utils.ConnectionHandler.__getitem__',
           side_effect=[OperationalError] * 5 + [True])
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, mock_sleep, mock_db_handler):
        """Test waiting for db using patch decorator raising
        OperationalError
        """
        call_command('wait_for_db')
        self.assertEqual(mock_db_handler.call_count, 6)

import unittest
import mock
import tictactoe.model

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.model = tictactoe.model.TicTacToe()
        self.status_observer = mock.Mock()
        self.error_observer = mock.Mock()

        def update_status():
            self.status_observer(**self.model.get_status(''))

        self.model.on_status_update += update_status
        self.model.on_invalid_operation += self.error_observer

    def test_should_allow_x_to_play_first(self):
        self.model.play("00", "x")
        self.assertTrue(self.status_observer.called)
        args, kwargs = self.status_observer.call_args
        self.assertEqual(kwargs["status"], "continue")
    
    def test_should_prevent_x_to_play_twice(self):
        self.model.play("00", "x")
        self.model.play("01", "x")
        self.assertTrue(self.error_observer.called)
    
    def test_should_allow_x_then_o_to_play(self):
        self.model.play("00", "x")
        self.model.play("01", "o")
        self.assertTrue(self.status_observer.called)
        args, kwargs = self.status_observer.call_args
        self.assertEqual(kwargs["status"], "continue")

    def test_should_declare_if_there_is_a_winner(self):
        self.model.play("00", "x")
        self.model.play("01", "o")
        self.model.play("10", "x")
        self.model.play("11", "o")
        self.model.play("20", "x")
        args, kwargs = self.status_observer.call_args
        self.assertEqual(kwargs["status"], "player x wins")

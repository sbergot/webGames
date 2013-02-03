import unittest
import tictactoe.model

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.model = tictactoe.model.TicTacToe(object())

    def test_should_allow_x_to_play_first(self):
        status = self.model.play("00", "x")
        self.assertEqual(status["type"], "continue")
    
    def test_should_prevent_x_to_play_twice(self):
        self.model.play("00", "x")
        status = self.model.play("01", "x")
        self.assertEqual(status["type"], "error")
    
    def test_should_allow_x_then_o_to_play(self):
        self.model.play("00", "x")
        status = self.model.play("01", "o")
        self.assertEqual(status["type"], "continue")

    def test_should_declare_if_there_is_a_winner(self):
        self.model.play("00", "x")
        self.model.play("01", "o")
        self.model.play("10", "x")
        self.model.play("11", "o")
        status = self.model.play("20", "x")
        self.assertEqual(status["status"], "player x wins")

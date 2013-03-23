import unittest
import mock
import player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.connections = [mock.Mock() for _ in range(10)]
        self.player = player.Player("my symbol")
        [self.player.connect(conn) for conn in self.connections]
    
    def test_should_allow_to_push_to_all_connections_of_a_player(self):
        self.player.emit("toto", {"name" : "titi"})
        for conn in self.connections:
            conn.emit.assert_called_with(
                "toto",
                {"name" : "titi"})
        

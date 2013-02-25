import unittest
import player
from FakeConnection import FakeConnection

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.connections = [FakeConnection() for _ in range(10)]
        self.player = player.Player()
        [self.player.connect(conn) for conn in self.connections]
    
    def test_should_allow_to_push_to_all_connections_of_a_player(self):
        self.player.emit("toto", {"name" : "titi"})
        for conn in self.connections:
            self.assertTrue(conn.emit_called)
        

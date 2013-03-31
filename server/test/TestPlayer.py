import unittest
import mock
import player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = player.Player("my symbol")

    def test_should_allow_to_add_a_connection(self):
        connection = mock.Mock()
        self.player.connect(connection)
        self.assertEqual(len(self.player.connections), 1)
        self.assertIn(connection, self.player.connections)
    
    def test_should_allow_to_remove_a_connection(self):
        connections = [mock.Mock() for _ in range(10)]
        [self.player.connect(conn) for conn in connections]
        to_remove = connections[6]
        self.player.disconnect(to_remove)
        self.assertNotIn(to_remove, self.player.connections)

    def test_should_tell_if_its_alive(self):
        self.assertFalse(self.player.is_alive())
        connection = mock.Mock()
        self.player.connect(connection)
        self.assertTrue(self.player.is_alive())
        self.player.disconnect(connection)
        self.assertFalse(self.player.is_alive())
        

    def test_should_allow_to_push_to_all_connections_of_a_player(self):
        connections = [mock.Mock() for _ in range(10)]
        [self.player.connect(conn) for conn in connections]
        self.player.emit("toto", {"name" : "titi"})
        for conn in connections:
            conn.emit.assert_called_with(
                "toto",
                {"name" : "titi"})
        

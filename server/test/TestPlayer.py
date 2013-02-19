import unittest

class FakeConnection:

    def __init__(self):
        self.emit_called = False
        
    def emit(self, name, data):
        self.emit_called = True

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.connections = [FakeConnection() for _ in range(10)]
    
    def test_should_allow_to_push_to_all_connections_of_a_player(self):
        for conn in self.connections:
            conn.emit("toto", {"foo" : "bar"})
        for conn in self.connections:
            self.assertTrue(conn.emit_called)
        

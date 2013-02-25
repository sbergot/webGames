import unittest
import session
import game
import player
from FakeConnection import FakeConnection

class MyModel(game.Game):
    pass

class TestSession(unittest.TestCase):

    def setUp(self):
        self.session = session.Session(MyModel)

    def test_should_be_initially_empty(self):
        self.assertEqual(self.session.players, {})

    def test_should_allow_to_add_players(self):
        playerInstance = player.Player()
        self.session.addPlayer('tata', playerInstance)
        self.assertEqual(self.session.players['tata'], playerInstance)

    def test_should_receive_connection_of_players(self):
        playerInstance = player.Player()
        self.session.addPlayer('tata', playerInstance)
        self.session.connect(FakeConnetion, "tata")
        self.assertEqual(
            length(self.session.players['tata'].connections),
            1)
        
class TestSessionBroker(unittest.TestCase):

    def setUp(self):
        self.session_broker = session.SessionBroker()
        self.session_broker.registerGame('my-game', MyModel)

    def test_should_allow_to_create_a_session(self):
        self.session_broker.get_session('my-game', 'toto')

    def test_should_create_a_session_with_a_model(self):
        session = self.session_broker.get_session('my-game', 'toto')
        self.assertIsInstance(session.model, MyModel)

    def test_should_return_an_existing_session_if_possible(self):
        session1 = self.session_broker.get_session('my-game', 'toto')
        session2 = self.session_broker.get_session('my-game', 'toto')
        self.assertIs(session1, session2)

    def test_should_provide_the_list_of_session(self):
        sessions = {
            "toto" : {"game" : "my-game", "id" : "toto"},
            "tata" : {"game" : "my-game", "id" : "tata"},
            }
        self.session_broker.get_session('my-game', 'toto')
        self.session_broker.get_session('my-game', 'tata')
        self.assertEqual(self.session_broker.getSessions(), sessions)


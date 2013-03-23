import unittest
import mock
import session
import game
import player

class MyModel(game.Game):

    def __init__(self, model_factory):
        self.symbols = [
            "fake symbol 1",
            "fake symbol 2",
            "fake symbol 3",
            ]

    def pop_symbol(self):
        return self.symbols.pop()

    def get_status(self, symbol):
        return "status for {}".format(symbol)

class TestSession(unittest.TestCase):

    def setUp(self):
        self.session = session.Session(MyModel)

    def test_should_be_initially_empty(self):
        self.assertEqual(self.session.players, {})

    def test_should_receive_connection_of_players(self):
        self.session.connect(mock.Mock(), "tata")
        self.assertEqual(
            len(self.session.players['tata'].connections),
            1)

    def test_should_allow_to_push_data_to_a_player(self):
        conn = mock.Mock()
        self.session.connect(conn, "tata")
        self.session.emit("event", {"toto" : "titi"}, "tata")
        conn.emit.assert_called_with("event", {"toto" : "titi"})

    def test_should_allow_to_broadcast_data_to_all_players(self):
        conn_tata = mock.Mock()
        self.session.connect(conn_tata, "tata")
        conn_robert = mock.Mock()
        self.session.connect(conn_robert, "robert")
        self.session.broadcast("event", {"key" : "value"})
        conn_tata.emit.assert_called_with("event", {"key" : "value"})
        conn_robert.emit.assert_called_with("event", {"key" : "value"})
        
    def test_should_allow_player_to_get_a_symbol(self):
        self.session.connect(mock.Mock(), "tata")
        self.session.connect(mock.Mock(), "titi")
        self.assertEqual(
            self.session.get_symbol("tata"),
            "fake symbol 3")
        self.assertEqual(
            self.session.get_symbol("tata"),
            "fake symbol 3")
        self.assertEqual(
            self.session.get_symbol("titi"),
            "fake symbol 2")

    def test_should_provide_a_status(self):
        conn_tata = mock.Mock()
        self.session.connect(conn_tata, "tata")
        self.assertEqual(
            self.session.get_status("tata"),
            "status for fake symbol 3")

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


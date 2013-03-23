import unittest
import mock
import session
import game
import player

class MyModel(game.Game):
    name = "my model"
    slot_nbr = 3

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

    def test_should_allow_to_add_a_player(self):
        self.session.add_player("tata")
        self.assertIn("tata", self.session.players)

    def test_should_receive_connection_of_players(self):
        self.session.add_player("tata")
        self.session.connect(mock.Mock(), "tata")
        self.assertEqual(
            len(self.session.players['tata'].connections),
            1)

    def test_should_allow_to_push_data_to_a_player(self):
        conn = mock.Mock()
        self.session.add_player("tata")
        self.session.connect(conn, "tata")
        self.session.emit("event", {"toto" : "titi"}, "tata")
        conn.emit.assert_called_with("event", {"toto" : "titi"})

    def test_should_allow_to_broadcast_data_to_all_players(self):
        conn_tata = mock.Mock()
        self.session.add_player("tata")
        self.session.connect(conn_tata, "tata")
        conn_robert = mock.Mock()
        self.session.add_player("robert")
        self.session.connect(conn_robert, "robert")
        self.session.broadcast("event", {"key" : "value"})
        conn_tata.emit.assert_called_with("event", {"key" : "value"})
        conn_robert.emit.assert_called_with("event", {"key" : "value"})
        
    def test_should_allow_player_to_get_a_symbol(self):
        self.session.add_player("tata")
        self.session.add_player("titi")
        self.assertEqual(
            self.session.get_symbol("tata"),
            "fake symbol 3")
        self.assertEqual(
            self.session.get_symbol("titi"),
            "fake symbol 2")

    def test_should_provide_a_status_of_the_game(self):
        conn_tata = mock.Mock()
        self.session.add_player("tata")
        self.session.connect(conn_tata, "tata")
        self.assertEqual(
            self.session.get_status("tata"),
            "status for fake symbol 3")

    def test_should_provide_the_list_of_players(self):
        self.session.add_player("tata")
        self.session.add_player("titi")

        def toDict(aList):
            return {elt["id"] : elt for elt in aList}

        self.assertEqual(
            toDict(self.session.get_players()),
            toDict([{"id" : "tata", "symbol" : "fake symbol 3"},
                    {"id" : "titi", "symbol" : "fake symbol 2"}]))

    def test_should_provide_a_structured_description_for_the_lobby(self):
        self.session.add_player("tata")
        self.session.add_player("titi")
        self.assertEqual(
            self.session.get_description(),
            {"name" : "my model",
             "players" : 2,
             "slots" : 3})


class TestSessionBroker(unittest.TestCase):

    def setUp(self):
        self.session_broker = session.SessionBroker()
        self.session_broker.registerGame('my-game', MyModel)

    def test_should_allow_to_create_a_session(self):
        self.session_broker.create_session('my-game')

    def test_should_create_a_session_with_a_model(self):
        session = self.session_broker.create_session('my-game')
        self.assertIsInstance(session.model, MyModel)

    def test_should_get_a_session_by_its_id(self):
        session = self.session_broker.create_session('my-game')
        id = self.session_broker.sessions.keys()[0] # the only one
        self.assertIs(session, self.session_broker.get_session(id))

    def test_should_provide_the_list_of_session(self):
        self.session_broker.create_session('my-game')
        self.session_broker.create_session('my-game')
        sessions = self.session_broker.getSessions()
        self.assertEqual(len(sessions.values()), 2)
        self.assertEqual(
            sessions.values()[0],
            {"players" : 0,
             "slots" : 3,
             "name" : "my model"})


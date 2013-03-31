import unittest
import mock
import session
from FakeModel import MyModel

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

    def test_should_allow_to_remove_a_connection(self):
        self.session.add_player("tata")
        connection = mock.Mock()
        self.session.connect(connection, "tata")
        self.session.connect(mock.Mock(), "tata")
        self.session.disconnect(connection, "tata")
        self.assertNotIn(
            connection,
            self.session.players['tata'].connections)

    def test_should_allow_to_remove_a_connection(self):
        self.session.add_player("tata")
        connection = mock.Mock()
        self.session.connect(connection, "tata")
        self.session.connect(mock.Mock(), "tata")
        self.session.disconnect(connection, "tata")
        self.assertNotIn(
            connection,
            self.session.players['tata'].connections)

    def test_should_allow_to_remove_a_player(self):
        self.session.add_player("tata")
        self.session.remove("tata")
        self.assertNotIn("tata", self.session.players)

    def test_should_tell_if_its_alive(self):
        self.assertFalse(self.session.is_alive())
        self.session.add_player("tata")
        self.assertTrue(self.session.is_alive())
        self.session.remove("tata")
        self.assertFalse(self.session.is_alive())

    def test_should_remove_a_player_if_its_not_alive_anymore(self):
        conn = mock.Mock()
        self.session.add_player("tata")
        self.session.connect(conn, "tata")
        self.session.disconnect(conn, "tata")
        self.assertNotIn("tata", self.session.players)

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
            toDict([{"occupied" : True,
                     "id" : "tata",
                     "symbol" : "fake symbol 3"},
                    {"occupied" : True,
                     "id" : "titi",
                     "symbol" : "fake symbol 2"}]))

    def test_should_provide_the_slot_status(self):
        self.session.add_player("tata")
        self.session.add_player("titi")

        def toDict(aList):
            return {elt["id"] : elt for elt in aList}

        self.assertEqual(
            toDict(self.session.get_slot_status()),
            toDict([{"occupied" : True,
                     "id" : "tata",
                     "symbol" : "fake symbol 3"},
                    {"occupied" : True,
                     "id" : "titi",
                     "symbol" : "fake symbol 2"},
                    {"occupied" : False,
                     "id" : None,
                     "symbol" : None}]))

    def test_should_provide_a_structured_description_for_the_lobby(self):
        self.session.add_player("tata")
        self.session.add_player("titi")
        self.assertEqual(
            self.session.get_description(),
            {"name" : "my model",
             "players" : 2,
             "slots" : 3})




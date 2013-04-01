import mock
import unittest
import event

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.event = event.Event()

    def test_should_allow_to_be_observed(self):
        self.event += mock.Mock()

    def test_should_allow_to_be_fired(self):
        observer = mock.Mock()
        self.event += observer
        self.event.fire()
        observer.assert_called_with()

    def test_should_allow_to_be_fired_arguments(self):
        observer = mock.Mock()
        self.event += observer
        self.event.fire("foo", bar=10)
        observer.assert_called_with("foo", bar=10)

    def test_should_allow_to_remove_observer(self):
        observer = mock.Mock()
        self.event += observer
        self.event -= observer
        self.event.fire()
        self.assertFalse(observer.called)

    def test_should_allow_to_remove_all_observers_from_an_object(self):
        fail = self.fail
        class MyObject(object):
            def foo(self):
                fail("foo should not be called")
            def bar(self):
                fail("bar should not be called")
        observer = MyObject()
        self.event += observer.foo
        self.event += observer.bar
        self.event.clear_observer(observer)
        self.event.fire()

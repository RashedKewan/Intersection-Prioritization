import unittest
from TrafficSignal import TrafficSignal

class TestTrafficSignal(unittest.TestCase):
    def setUp(self):
        self.signal = TrafficSignal(30, 5, 25, 10, 50)

    def test_signal_text(self):
        self.assertEqual(self.signal.signal_text, "30")

    def test_total_green_time(self):
        self.assertEqual(self.signal.total_green_time, 0)

if __name__ == '__main__':
    unittest.main()

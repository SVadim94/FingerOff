import unittest

from models.DebtGraph import DebtGraph, DebtGraphModel

from tutils import make_transaction

class TestDebtGraph(unittest.TestCase):
    def setUp(self):
        self.graph = DebtGraphModel()

    def test_transitive(self):
        a = make_transaction('@Pupa', '@Lupa', 10)
        b = make_transaction('@Lupa', '@Buhg', 10)
        c = make_transaction('@Pupa', '@Buhg', 2)

        self.graph.add_debt(a)
        self.graph.add_debt(b)
        self.graph.add_debt(c)

        self.assertTrue(self.graph.transitive())

        self.assertEqual(self.graph.graph["@Pupa"]["@Buhg"]["weight"], 12)
        self.assertNotIn(('@Pupa', '@Lupa'), self.graph.graph.edges())
        self.assertNotIn(('@Lupa', '@Buhg'), self.graph.graph.edges())

    def tearDown(self):
        pass

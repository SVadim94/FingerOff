from pickle import dumps, loads

import networkx as nx
from peewee import BlobField, ForeignKeyField

from . import BaseModel
from .Chat import Chat
from .User import User


class DebtGraphModel:
    def __init__(self):
        self.graph = nx.DiGraph()

    def no_debt(self, node):
        for a, b, w in self.graph.edges(node, data='weight'):
            if w == 0:
                self.graph.remove_edge(a, b)

    def self_debt(self):
        for a, b in self.graph.edges():
            if a == b:
                self.graph.remove_edge(a, b)

    def transitive(self, first, second):
        for node in [first, second]:
            debts = self.graph.out_edges(node, data='weight')
            lends = self.graph.in_edges(node, data='weight')

            for b, c, weight_b_c in debts:
                for a, b, weight_a_b in lends:
                    if weight_a_b == weight_b_c:
                        # delete (a, b) and (b, c)
                        self.graph.remove_edge(a, b)
                        self.graph.remove_edge(b, c)
                        # add (a, c)
                        self.graph.add_edge(a, c, weight=weight_a_b)

    def optimize(self, first, second):
        self.transitive(first, second)
        # self.no_debt(self)

    def add_debt(self, debt):
        creditor = debt.creditor.username
        debtor = debt.debtor.username

        if debtor == creditor or debt.amount == 0:
            return

        if self.graph.has_edge(debtor, creditor):
            self.graph.edge[debtor][creditor]['weight'] += debt.amount
        elif self.graph.has_edge(creditor, debtor):
            self.graph.edge[creditor][debtor]['weight'] -= debt.amount

            if self.graph.edge[creditor][debtor]['weight'] < 0:
                weight = -self.graph.edge[creditor][debtor]['weight']
                self.graph.remove_edge(creditor, debtor)
                self.graph.add_edge(debtor, creditor, weight=weight)
        else:
            self.graph.add_edge(debtor, creditor, weight=debt.amount)

        self.optimize(debtor, creditor)


class DebtGraph(BaseModel):
    chat = ForeignKeyField(Chat)
    graph = BlobField(default=dumps(DebtGraphModel()))

    @staticmethod
    def load_graph(chat):
        debt_graph, _ = DebtGraph.get_or_create(chat=chat)
        return loads(debt_graph.graph)

    @staticmethod
    def save_graph(chat, graph):
        debt_graph, _ = DebtGraph.get_or_create(chat=chat)
        debt_graph.graph = dumps(graph)

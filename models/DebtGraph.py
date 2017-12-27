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

    def transitive(self):
        changes = False

        for node in self.graph.nodes():
            debts = self.graph.out_edges(node, data='weight')
            lends = self.graph.in_edges(node, data='weight')

            for b, c, weight_b_c in debts.copy():
                for a, b, weight_a_b in lends.copy():
                    if weight_a_b == weight_b_c:
                        # delete (a, b) and (b, c)
                        self.graph.remove_edge(a, b)
                        self.graph.remove_edge(b, c)
                        # add (a, c)
                        self.merge(a, c, weight_a_b)

                        changes = True

        return changes

    def optimize(self, first, second):
        while self.transitive():
            pass

        # self.no_debt(self)

    def merge(self, creditor, debtor, weight):
        if self.graph.has_edge(debtor, creditor):
            self.graph.get_edge_data(debtor, creditor)['weight'] += weight
        elif self.graph.has_edge(creditor, debtor):
            self.graph.get_edge_data(creditor, debtor)['weight'] -= weight

            if self.graph.get_edge_data(creditor, debtor)['weight'] < 0:
                weight = -self.graph.get_edge_data(creditor, debtor)['weight']
                self.graph.remove_edge(creditor, debtor)
                self.graph.add_edge(debtor, creditor, weight=weight)
        else:
            self.graph.add_edge(debtor, creditor, weight=weight)

    def add_debt(self, debt):
        creditor = debt.creditor.username
        debtor = debt.debtor.username

        if debtor == creditor or debt.amount == 0:
            return

        self.merge(creditor, debtor, debt.amount)

        # self.optimize(debtor, creditor)

    def print_graph(self):
        pass


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

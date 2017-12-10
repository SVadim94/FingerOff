from peewee import ForeignKeyField, DecimalField, BlobField
from decimal import Decimal
from . import BaseModel
from .User import User
from .Chat import Chat
import networkx as nx


class Blueprint:
    heuristics = []

    def __init__(self):
        self.graph = nx.DiGraph()

    @staticmethod
    def heuristic(foo):
        Blueprint.heuristics.append(foo)

    @heuristic
    def no_debt(self):
        for a, b, w in self.graph.edges(data='weight'):
            if w == 0:
                self.graph.remove_edge(a, b)

    @heuristic
    def self_debt(self):
        for a, b in self.graph.edges():
            if a == b:
                self.graph.remove_edge(a, b)

    @heuristic
    def transitive(self):
        for node in self.graph:
            debts = self.graph.out_edges(node, data='weight')
            lends = self.graph.in_edges(node, data='weight')

            for b, c, weight_b_c in debts:
                for a, b, weight_a_b in lends:
                    if weight_a_b == weight_b_c:
                        # delete (a, b) and (b, c)
                        self.graph.delete()
                        # add (a, c)

    def add_debt(self, debt):
        lender = debt.lender.username
        debtor = debt.debtor.username

        if self.graph.has_edge(debtor, lender):
            self.graph.edge[debtor][lender]['weight'] += debt.amount
        elif self.graph.has_edge(lender, debtor):
            self.graph.edge[debtor][lender]['weight'] -= debt.amount
        else:
            self.graph.add_edge(debtor, lender, weight=debt.amount)

        for heuristic in Blueprint.heuristics:
            heuristic(self)



# TODO: Weighted Oriented Graph
class DebtGraph(BaseModel):
    chat = ForeignKeyField(Chat)
    first = ForeignKeyField(User, related_name='first')
    second = ForeignKeyField(User, related_name='second')
    amount = DecimalField(decimal_places=2, default=Decimal("0"))

    def __str__(self):
        return "[ %(first)s --[%(amount)d%(currency)s]-->  %(second)s ]" % {
            "first": self.first.username,
            "second": self.second.username,
            "amount": self.amount,
            "currency": self.chat.currency
        }

    def merge(self, debt):
        if self.chat == debt.chat:
            if (self.first, self.second) == (debt.lender, debt.debtor):
                self.amount -= debt.amount
            elif (self.first, self.second) == (debt.debtor, debt.lender):
                self.amount += debt.amount
            else:
                return

    @staticmethod
    def add(debt):
        opt_debt = DebtGraph.get_corresponding_optimized_debt(debt)
        opt_debt.merge(debt)
        opt_debt.save()

        # run heuristics here
        for heuristic in heuristics:
            heuristic(DebtGraph.select())

    @staticmethod
    def get_corresponding_optimized_debt(debt):
        first, second = sorted((debt.lender, debt.debtor), key=lambda x: x.username)

        return DebtGraph.get_or_create(
            chat=debt.chat,
            first=first,
            second=second
        )[0]


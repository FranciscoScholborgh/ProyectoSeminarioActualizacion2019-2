from __future__ import annotations
from abc import ABCMeta, abstractmethod


class Subject(metaclass=ABCMeta):

    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass

class Observer(metaclass=ABCMeta):

    @abstractmethod
    def update(self, state):
        pass
from dataclasses import dataclass

from model.actor import Actor


@dataclass
class Arco:
    Actor1: Actor
    Actor2: Actor
    Peso: int

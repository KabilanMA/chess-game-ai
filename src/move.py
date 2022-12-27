from square import Square

class Move:

    def __init__(self, initial: Square, final: Square) -> None:
        self.initial = initial
        self.final = final

    def __str__(self) -> str:
        s=''
        s+=f'({self.initial.col}, {self.initial.row})'
        s+=f' -> ({self.final.col}, {self.final.row})'

        return s

    def __eq__(self, __o: object) -> bool:
        return self.initial == __o.initial and self.final == __o.final
class NimState:
    # Representerer en tilstand av Nim. NimState tar inn spillets regler og antall steiner som er gjenværende.

    def __init__(self, game_setting, stones):
        self.stones_remaining = stones
        self.player_just_moved = game_setting.P
        self.game_setting = game_setting

    def clone(self):
        """
        Lager en deep clone av game state
        """
        st = NimState(self.game_setting, self.stones_remaining)
        st.player_just_moved = self.player_just_moved
        return st

    def do_move(self, move):
        """
        Oppdaterer spillet ved å utføre move
        player_just_moved oppdaterer seg deretter
        """
        self.stones_remaining -= move
        self.player_just_moved = 3 - self.player_just_moved

    def get_moves(self):
        """
        Returnerer alle tilgjengelige moves
        """
        K = self.game_setting.K

        if K > self.stones_remaining:
            return [i for i in range(1, self.stones_remaining + 1)]
        else:
            return [i for i in range(1, K + 1)]

    def get_result(self, playerjm):
        """
        Returnerer resultatet fra playerjm sitt ståsted
        """
        assert self.stones_remaining == 0
        if self.player_just_moved == playerjm:
            return 1.0
        else:
            return 0.0
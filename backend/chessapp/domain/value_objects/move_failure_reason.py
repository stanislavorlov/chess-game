from dataclasses import dataclass


@dataclass(frozen=True)
class MoveFailureReason:
    code: str
    message: str

    @classmethod
    def game_not_started(cls):
        return cls("GAME_NOT_STARTED", "The game has not started yet.")

    @classmethod
    def game_finished(cls):
        return cls("GAME_FINISHED", "The game has already finished.")

    @classmethod
    def not_your_turn(cls):
        return cls("NOT_YOUR_TURN", "Wait for your turn.")

    @classmethod
    def king_in_check(cls):
        return cls("KING_IN_CHECK", "You cannot move this piece while your king is in check.")

    @classmethod
    def state_mismatch(cls):
        return cls("STATE_MISMATCH", "Current move doesn't match current state.")

    @classmethod
    def illegal_move(cls):
        return cls("ILLEGAL_MOVE", "This move is not allowed by chess rules.")

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message
        }

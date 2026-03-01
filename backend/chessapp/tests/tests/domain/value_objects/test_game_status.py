import unittest
from chessapp.domain.value_objects.game_status import GameStatus

class TestGameStatus(unittest.TestCase):
    def test_status_equality(self):
        self.assertEqual(GameStatus.created(), GameStatus.created())
        self.assertEqual(GameStatus.started(), GameStatus.started())
        self.assertNotEqual(GameStatus.created(), GameStatus.started())

    def test_rank_logic(self):
        created = GameStatus.created()
        started = GameStatus.started()
        finished = GameStatus.finished()
        aborted = GameStatus.aborted()

        # CREATED (0) <= STARTED (1)
        self.assertTrue(started.is_following_rank(created))
        self.assertFalse(created.is_following_rank(started))

        # STARTED (1) <= FINISHED (2)
        self.assertTrue(finished.is_following_rank(started))
        
        # STARTED (1) <= ABORTED (3)
        self.assertTrue(aborted.is_following_rank(started))

        # FINISHED (2) and ABORTED (3) are both >= STARTED (1)
        self.assertTrue(finished.is_following_rank(created))
        self.assertTrue(aborted.is_following_rank(created))

    def test_string_representation(self):
        self.assertEqual(str(GameStatus.created()), "CREATED")
        self.assertEqual(str(GameStatus.started()), "STARTED")
        self.assertEqual(str(GameStatus.finished()), "FINISHED")
        self.assertEqual(str(GameStatus.aborted()), "ABORTED")

if __name__ == "__main__":
    unittest.main()

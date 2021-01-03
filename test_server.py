import unittest
import server

class TestServer(unittest.TestCase):
    # Useful varibles for test methods.
    players = [
        server.Entity("player", [1,1], 100),
        server.Entity("player", [2,2], 100),
    ]

    enemies = [
        server.Entity("enemy", [1,1], 100),
        server.Entity("enemy", [2,2], 100),
        server.Entity("enemy", [3,3], 100),
    ]
    

    def test_enemies_pos_to_str(self):
        formattet_str = server.enemies_pos_to_str(self.enemies)

        self.assertEqual(formattet_str, "1 1;2 2;3 3")


    def test_players_pos_to_str(self):
        formatted_str_p1 = server.players_pos_to_str(0, self.players)
        formatted_str_p2 = server.players_pos_to_str(1, self.players)

        self.assertEqual(formatted_str_p1, "1,1 2,2")
        self.assertEqual(formatted_str_p2, "2,2 1,1")


    def test_generate_enemies(self):
        generated_enemies = server.generate_enemies(3, self.players)

        for enemy in generated_enemies:
            self.assertNotEqual(enemy.pos, self.players[0].pos)
            self.assertNotEqual(enemy.pos, self.players[1].pos)


    # missing tests for:
    # client_thread
    # Entity.update_player_pos
    # Entity.update_enemy_pos


if __name__ == "__main__":
    unittest.main()

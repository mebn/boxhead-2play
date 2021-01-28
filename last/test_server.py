import unittest
import server

class TestServer(unittest.TestCase):
    # Useful varibles for test methods.
    players = [
        server.Entity("player", [100, 200], 100),
        server.Entity("player", [200, 100], 50),
    ]

    enemies = [
        server.Entity("enemy", [10, 20], 100),
        server.Entity("enemy", [30, 40], 90),
        server.Entity("enemy", [50, 60], 80),
    ]
    

    def test_enemies_pos_to_str(self):
        formattet_str = server.enemies_pos_to_str(self.enemies)

        self.assertEqual(formattet_str, "10 20;30 40;50 60")


    def test_players_pos_to_str(self):
        formatted_str_p1 = server.players_pos_to_str(0, self.players)
        formatted_str_p2 = server.players_pos_to_str(1, self.players)

        self.assertEqual(formatted_str_p1, "100,200 200,100")
        self.assertEqual(formatted_str_p2, "200,100 100,200")


    def test_generate_enemies(self):
        generated_enemies = server.generate_enemies(3, self.players)

        for enemy in generated_enemies:
            self.assertNotEqual(enemy.pos, self.players[0].pos)
            self.assertNotEqual(enemy.pos, self.players[1].pos)

    
    def test_players_hp_as_str(self):
        formatted_str_p1 = server.players_hp_as_str(0, self.players)
        formatted_str_p2 = server.players_hp_as_str(1, self.players)

        self.assertEqual(formatted_str_p1, "100 50")
        self.assertEqual(formatted_str_p2, "50 100")


    # missing tests for:
    # client_thread
    # Entity.update_player_pos
    # Entity.update_enemy_pos


if __name__ == "__main__":
    unittest.main()

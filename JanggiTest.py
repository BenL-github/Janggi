import unittest
import JanggiGame

class MyTestCase(unittest.TestCase):
    def test_diagonal_extended(self):
        board = JanggiGame.JanggiBoard()
        tile = board.get_tile("b", 3)

        up = tile.get_diagonal_tiles_extended("UP")
        down = tile.get_diagonal_tiles_extended("DOWN")
        right = tile.get_diagonal_tiles_extended("RIGHT")
        left = tile.get_diagonal_tiles_extended("LEFT")
        print()

    def test_elephant(self):
        board = JanggiGame.JanggiBoard()
        tile = board.get_tile("e", 2)

        elephant = JanggiGame.Elephant(tile, "RED", board)
        tile.set_piece(elephant)

        paths = elephant.find_paths()

        board = JanggiGame.JanggiBoard()
        board.set_up()

        tile = board.get_tile("b", 10)
        elephant = tile.get_piece()

        valid_moves = elephant.get_valid_moves()

        print()

    def test_guard(self):
        board = JanggiGame.JanggiBoard()
        board.set_up()

        guard = board.get_piece_at_tile("f", 10)
        valid_moves = guard.get_valid_moves()

        guard2 = board.get_piece_at_tile("d", 1)
        valid_moves2 = guard2.get_valid_moves()

        print()

    def test_soldier(self):
        #
        game = JanggiGame.JanggiGame()
        board = game.get_board()
        board.set_up()

        piece = board.get_tile("a", 4).get_piece()

        possible_paths = piece.get_valid_moves()
        self.assertEqual(possible_paths, [('a', 5), ('b', 4)])

        # test for valid moves when soldier is blocked in one potential path
        game = JanggiGame.JanggiGame()
        board = game.get_board()
        board.set_up()

        blocked_tile = board.get_tile("a", 5)

        test_soldier = JanggiGame.Soldier(blocked_tile, "RED", board)
        blocked_tile.set_piece(test_soldier)

        tile = board.get_tile("a", 4)
        soldier = tile.get_piece()

        possible_paths = soldier.get_valid_moves()
        self.assertEqual(possible_paths, [("b", 4)])

        # test for valid moves when soldier is in blue palace
        game = JanggiGame.JanggiGame()
        board = game.get_board()

        tile = board.get_tile("e",9)
        soldier = JanggiGame.Soldier(tile, "RED", board)
        tile.set_piece(soldier)
        possible_moves = soldier.get_valid_moves()
        board = game.get_board()


    def test_print_board(self):
        board = JanggiGame.JanggiBoard()
        board.set_up()

        # board.print_board()

    def test_chariot(self):
        board = JanggiGame.JanggiBoard()
        ctile = board.get_tile("f", 1)

        chariot = JanggiGame.Chariot(ctile, "RED", board)
        ctile.set_piece(chariot)
        paths1 = chariot.get_valid_moves()

        cornertile = board.get_tile("f", 8)
        guard = JanggiGame.Guard(cornertile, "BLUE", board)
        cornertile.set_piece(guard)
        paths1 = guard.get_valid_moves()


        cornertile2 = board.get_tile("d", 10)
        soldier = JanggiGame.Soldier(cornertile2, "RED", board)
        cornertile2.set_piece(soldier)
        paths1 = soldier.get_valid_moves()


        paths2 = chariot.get_valid_moves()

        soldier_path = soldier.get_valid_moves()



    def test_cannon(self):

        board = JanggiGame.JanggiBoard()
        center = board.get_tile("e", 9)
        corner = board.get_tile("h", 8)
        other = board.get_tile("f", 8)

        general = JanggiGame.General(center, "BLUE", board)
        center.set_piece(general)

        cannon = JanggiGame.Cannon(corner, "BLUE", board)
        corner.set_piece(cannon)

        paths = cannon.get_valid_moves()
        print()

    def test_pass_turn(self):
        game = JanggiGame.JanggiGame()
        self.assertTrue(game.make_move("a7", "b7"))
        self.assertTrue(game.make_move("a4", "a4"))
        self.assertTrue(game.make_move("b7", "b6"))

    def test_horse(self):
        board = JanggiGame.JanggiBoard()
        tile = board.get_tile("b", 2)
        horse = JanggiGame.Horse(tile, "RED", board)
        valid_moves = horse.get_valid_moves()

        print()

    def test_sample_game1(self):
        game = JanggiGame.JanggiGame()
        self.assertFalse(game.make_move("a7", "a8"))
        game.get_board().print_board()
        self.assertTrue(game.make_move("a7", "b7"))
        game.get_board().print_board()
        self.assertTrue(game.make_move("a4", "b4"))
        game.get_board().print_board()
        self.assertTrue(game.make_move("a10", "a2"))
        game.get_board().print_board()
        self.assertFalse(game.make_move("e4", "e5"))
        game.get_board().print_board()
        self.assertTrue(game.make_move("a1", "a2"))
        game.get_board().print_board()


    def test_sample_game2(self):
        game = JanggiGame.JanggiGame()
        game.make_move("c10", "d8")

        # red horse
        game.make_move("c1", "d3")

        game.make_move("e7", "e6")
        game.make_move("e4", "e5")
        game.make_move("c7", "c6")
        game.make_move("c4", "c5")
        game.make_move("c6", "c5")
        game.make_move("e5", "e6")

        game.make_move("d8", "e6")

        # red
        game.make_move("d3", "c5")


        game.make_move("h10", "g8")

        # red
        game.make_move("h1", "i3")

        game.make_move("g7", "h7")
        game.make_move("g4", "f4")
        game.make_move("h7", "h6")
        game.make_move("i4", "i5")
        game.make_move("h6", "h5")
        game.make_move("i5", "i6")

        game.make_move("g8", "g8")
        game.make_move("i3", "h5")

        pass

    def test_sample_game3(self):
        game = JanggiGame.JanggiGame()

        self.assertTrue(game.make_move("c7", "c6"))
        self.assertTrue(game.make_move("c1", "d3"))
        self.assertTrue(game.make_move("b10", "d7"))
        self.assertTrue(game.make_move("b3", "e3"))

        self.assertTrue(game.make_move("c10", "d8"))
        self.assertTrue(game.make_move("h1", "g3"))

        game.make_move("e7", "e6")
        game.make_move("e3", "e6")

    def test_sample_game4(self):
        game = JanggiGame.JanggiGame()
        game.make_move('e7', 'e6')
        game.make_move('e2', 'e2')
        game.make_move('e6', 'e5')
        game.make_move('e2', 'e2')
        game.make_move('e5', 'e4')
        game.make_move('e2', 'e2')
        game.make_move('e4', 'd4')
        game.make_move('e2', 'e2')
        game.make_move('d4', 'c4')
        game.make_move('e2', 'e2')
        game.make_move('a10', 'a9')
        game.make_move('e2', 'e2')
        game.make_move('a9', 'd9')
        game.make_move('e2', 'e2')
        game.make_move('d9', 'd8')
        game.make_move('e2', 'e2')
        game.make_move('d8', 'd7')
        game.make_move('e2', 'e2')
        game.make_move('d7', 'd6')
        game.make_move('i1', 'i2')
        game.make_move('e9', 'e9')
        game.make_move('i2', 'g2')
        game.make_move('e9', 'e9')
        game.make_move('i4', 'h4')
        game.make_move('e9', 'e9')
        game.make_move('h3', 'h5')
        game.make_move('i10', 'i9')
        game.make_move('e2', 'e2')
        game.make_move('i9', 'g9')
        game.make_move('e2', 'e2')
        game.make_move('g9', 'g8')
        game.make_move('e2', 'e2')
        game.make_move('h8', 'f8')
        game.make_move('f1', 'e1')
        game.make_move('g7', 'f7')
        game.make_move('e2', 'e2')
        game.make_move('i7', 'i6')
        game.make_move('e2', 'e2')
        game.make_move('g10', 'i7')
        game.make_move('e2', 'e2')
        game.make_move('i7', 'f5')
        game.make_move('e2', 'e2')
        game.make_move('f5', 'd8')
        game.make_move('e2', 'e2')
        game.make_move('d8', 'd8')
        game.make_move('e2', 'e2')
        game.make_move('c4', 'd4')
        game.make_move('e2', 'e2')
        game.make_move('d4', 'e4')
        game.make_move('e2', 'e2')

        game.make_move('e4', 'e3')
        self.assertEqual(game.get_game_state(), "UNFINISHED")

    def test_sample_game5(self):
        game = JanggiGame.JanggiGame()
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        game.make_move('a7', 'b7')
        game.make_move('i4', 'h4')
        game.make_move('h10', 'g8')
        game.make_move('c1', 'd3')
        game.make_move('h8', 'e8') #
        game.make_move('i1', 'i2')
        game.make_move('e7', 'f7')
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        game.make_move('b3', 'e3')
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('g10', 'e7'))
        self.assertTrue(game.make_move('e4', 'd4'))
        self.assertTrue(game.make_move('c10', 'd8'))
        self.assertTrue(game.make_move('g1', 'e4'))
        self.assertTrue(game.make_move('f10', 'f9'))
        self.assertTrue(game.make_move('h1', 'g3'))
        self.assertTrue(game.make_move('a10', 'a6'))
        self.assertTrue(game.make_move('d4', 'd5'))
        self.assertTrue(game.make_move('e9', 'f10'))
        self.assertTrue(game.make_move('h3', 'f3'))
        self.assertTrue(game.make_move('e8', 'h8')) #
        self.assertTrue(game.make_move('i2', 'h2'))
        self.assertTrue(game.make_move('h8', 'f8')) #
        self.assertTrue(game.make_move('f1', 'f2'))
        self.assertTrue(game.make_move('b8', 'e8'))
        self.assertTrue(game.make_move('f3', 'f1'))
        self.assertTrue(game.make_move('i7', 'h7'))
        self.assertTrue(game.make_move('f1', 'c1'))
        self.assertTrue(game.make_move('d10', 'e9'))
        self.assertTrue(game.make_move('a4', 'b4'))
        self.assertTrue(game.make_move('a6', 'a1'))
        self.assertTrue(game.make_move('c1', 'a1'))
        self.assertTrue(game.make_move('f8', 'd10')) #
        self.assertTrue(game.make_move('d5', 'c5'))
        self.assertTrue(game.make_move('i10', 'i6'))
        self.assertTrue(game.make_move('b1', 'd4'))
        self.assertTrue(game.make_move('c7', 'c6'))
        self.assertTrue(game.make_move('c5', 'b5'))
        self.assertTrue(game.make_move('b10', 'd7'))
        self.assertTrue(game.make_move('d4', 'f7'))
        self.assertTrue(game.make_move('g7', 'f7'))
        self.assertTrue(game.make_move('a1', 'f1'))
        self.assertTrue(game.make_move('g8', 'f6'))
        self.assertTrue(game.make_move('f1', 'f5'))
        self.assertTrue(game.make_move('f6', 'd5'))
        self.assertTrue(game.make_move('e3', 'e5'))
        self.assertTrue(game.make_move('f7', 'f6'))
        self.assertTrue(game.make_move('f5', 'f7'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('f10', 'e10'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('e2', 'f1'))
        self.assertTrue(game.make_move('i6', 'i3'))
        self.assertTrue(game.make_move('h2', 'g2'))
        self.assertTrue(game.make_move('i3', 'i1'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('f1', 'e2'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('f6', 'f5'))
        self.assertTrue(game.make_move('c4', 'd4'))
        self.assertTrue(game.make_move('f5', 'e5'))
        self.assertTrue(game.make_move('f7', 'd7'))
        self.assertTrue(game.make_move('e7', 'g4'))
        self.assertTrue(game.make_move('d4', 'd5'))
        self.assertTrue(game.make_move('e5', 'e4'))
        self.assertTrue(game.make_move('d3', 'e5'))
        self.assertTrue(game.make_move('e4', 'e3'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('e2', 'd2'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('e3', 'e2'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        print(game.make_move('d2', 'd3'))
        print(game.is_in_check('red'))
        print(game.is_in_check('blue'))
        self.assertTrue(game.make_move('e8', 'e4'))
        self.assertTrue(game.make_move('f2', 'e2'))
        self.assertTrue(game.make_move('i1', 'd1'))
        self.assertTrue(game.make_move('e2', 'd2'))
        print(game.make_move('d1', 'f3'))
        print(game.get_game_state())


    def test_game2(self):
        game = JanggiGame.JanggiGame()

        print(game.make_move("b10", "d7"))
        print(game.make_move("b1", "d4"))

        print(game.make_move("c10", "d8"))
        print(game.make_move("c1", "d3"))
        print(game.make_move("h10", "g8"))
        print(game.make_move("h1", "g3"))
        print(game.make_move("b8", "e8"))
        print(game.make_move("b3", "e3"))
        print(game.make_move("h8", "f8"))
        print(game.make_move("h3", "f3"))
        print(game.make_move("d10", "d9"))
        print(game.make_move("d1", "d2"))
        print(game.make_move("f10", "f9"))
        print(game.make_move("f1", "f2"))
        print(game.make_move("e9", "e10"))
        print(game.make_move("e2", "e1"))

        print("false stuff ")

        print("2")

        print(game.make_move("i7", "i6"))

        print("3")

        print(game.make_move("e3", "e5"))

        print(game.make_move("e1", "e1"))
        print()
        print(game.make_move("e1", "e1"))
        print()
        print("4")
        print()
        print()
        print()
        print()
        print()
        print(game.make_move("e10", "e10"))
        print()
        print()
        print()
        print("5")
        print(game.make_move("d4", "f7")) # red turn
        print(game.make_move("d9", "d10"))
        print(game.make_move("f7", "d10")) # red
        print(game.make_move("e8", "c8")) # red
        print(game.make_move("e1", "d1")) # red
        print(game.make_move("f10", "e8")) # blue
        print(game.make_move("c8", "c1"))
        print(game.make_move("d2", "e2"))
        print(game.make_move("e10", "e10"))
        print("6")
        print(game.make_move("e5", "e3")) # red
        print(game.make_move("f2", "f1")) # blue
        print(game.make_move("e10", "d10"))
        print(game.make_move("e2", "e1"))
        print(game.make_move("c4", "e1"))
        print(game.make_move("e3", "e10"))
        print(game.make_move("a7", "a2"))
        print(game.make_move("e4", "c7"))
        print(game.make_move("f2", "e2"))
        print(game.make_move("d1", "d2"))
        print(game.make_move("e2", "d1"))
        print(game.get_game_state())
    def test_game1(self):
        game = JanggiGame.JanggiGame()
        game.make_move("c10", "d8")
        game.make_move("i4", "h4")
        game.make_move("g7", "h7")
        game.make_move("h3", "h7")
        game.make_move("i7", "h7")
        game.make_move("i1", "i10")
        game.make_move("h10", "g8")
        game.make_move("i10", "g10")
        game.make_move("f10", "e10")
        game.make_move("g10", "g9")
        print(game.is_in_check("blue"))
        self.assertFalse(game.make_move("e9", "f9"))

        game.make_move("d8", "f9")
        game.make_move("h1", "g3")
        game.make_move("a7", "b7")
        game.make_move("b1", "d4")
        game.make_move("g8", "h6")
        game.make_move("g4", "f4")
        game.make_move("a10", "a6")
        game.make_move("d4", "b7")
        game.make_move("b10", "d7")
        game.make_move("b7", "d4")
        game.make_move("e7", "f7")
        game.make_move("a4", "a5")
        game.make_move("a6", "c6")
        game.make_move("g9", "i9")
        Janggi = game
        Janggi.make_move("c7", "b7")
        Janggi.make_move("c1", "d3")
        Janggi.make_move("c6", "c4")
        Janggi.make_move("e2", "e1")



        Janggi.make_move("e9", "f8")
        Janggi.make_move("i9", "g9")
        Janggi.make_move("e10", "e9")
        Janggi.make_move("b3", "e3")
        Janggi.make_move("f7", "f6")
        Janggi.make_move("d1", "e2")
        Janggi.make_move("b7", "b6")
        Janggi.make_move("a5", "b5")
        Janggi.make_move("b6", "b5")
        Janggi.make_move("a1", "a6")
        Janggi.make_move("b5", "c5")
        Janggi.make_move("g9", "g8")
        Janggi.make_move("b8", "g8")
        Janggi.make_move("a6", "f6")
        Janggi.make_move("h6", "f7")
        Janggi.make_move("f6", "f7")

        print(Janggi.get_game_state())


if __name__ == '__main__':
    unittest.main()

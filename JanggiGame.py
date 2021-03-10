# Name: Benny Li
# Date:
# Description:

class Piece():
    def __init__(self, tile, player, board):
        self._tile = tile
        self._player = player
        self._board = board
        self._captured = False

    def get_location(self):
        return self._tile.get_location()

    def get_tile(self):
        return self._tile

    def set_tile(self, tile):
        self._tile = tile

    def get_player(self):
        return self._player

    def isCaptured(self):
        return self._captured

    def set_Captured(self):
        self._captured = True

class Cannon(Piece):
    def __init__(self, tile, player, board):
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        paths = list()
        orthogonal = self._tile.get_all_orthogonal_tiles()
        current = self._tile.get_location()

        direction = list()
        for step_one in orthogonal:
            if step_one[0] < current[0]:
                direction.append("LEFT")
            elif step_one[0] > current[0]:
                direction.append("RIGHT")
            elif step_one[1] < current[1]:
                direction.append("UP")
            elif step_one[1] > current[1]:
                direction.append("DOWN")

        index = 0
        for tile in orthogonal:

            col = tile[0]
            row = tile[1]

            tile_obj = self._board.get_tile(col, row)

            tiles_in_direction = self.rec_find_vertical_tiles(tile_obj, direction[index])

            if tiles_in_direction != []:
                paths.append(tiles_in_direction)
            index += 1

        return paths

    def rec_find_vertical_tiles(self, tile, direction, jumpable = False, tile_list = None):

        if tile_list is None:
            tile_list = list()

        piece = tile.get_piece()

        if jumpable is False and piece is not None and type(piece).__name__ != "Cannon":
            jumpable = True

            # checks next tile exists
            next_tile = tile.get_orthogonal_tiles(direction)

            # end of board
            if next_tile == []:
                return tile_list

            # recursively call next tile
            col = next_tile[0][0]
            row = next_tile[0][1]
            next_tile_obj = self._board.get_tile(col, row)

            return self.rec_find_vertical_tiles(next_tile_obj, direction, jumpable, tile_list)

        # if there was a piece to jump over and current tile has no piece, add current tile to list
        if jumpable and piece is None:
            tile_list.append(tile.get_location())
        # if jumpable and current tile has a piece
        elif jumpable:
            # finds the piece type and player of the piece on current tile
            piece_type = type(piece).__name__
            player = piece.get_player()

            # checks if the piece is a cannon
            isCannon = piece_type == "Cannon"
            # checks if the piece is from current player
            samePlayer = player == self.get_player()


            # stop recursive call and return list if current tile has a cannon or a piece from same player
            if isCannon or samePlayer:
                return tile_list
            # if not a cannon and not same player
            else:
                tile_list.append(tile.get_location())

        # checks next tile exists
        next_tile = tile.get_orthogonal_tiles(direction)

        # end of board
        if next_tile == []:
            return tile_list

        # recursively call next tile
        col = next_tile[0][0]
        row = next_tile[0][1]
        next_tile_obj = self._board.get_tile(col, row)

        return self.rec_find_vertical_tiles(next_tile_obj, direction, jumpable, tile_list)

class Chariot(Piece):
    def __init__(self, tile, player, board):
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        paths = list()
        orthogonal = self._tile.get_all_orthogonal_tiles()
        current = self._tile.get_location()

        direction = list()
        for step_one in orthogonal:
            if step_one[0] < current[0]:
                direction.append("LEFT")
            elif step_one[0] > current[0]:
                direction.append("RIGHT")
            elif step_one[1] < current[1]:
                direction.append("UP")
            elif step_one[1] > current[1]:
                direction.append("DOWN")

        index = 0
        for tile in orthogonal:
            # retrieve tile piece is currently on
            col = self.get_location()[0]
            row = self.get_location()[1]
            tile_obj = self._board.get_tile(col, row)

            # recursively add valid tiles to move to from each direction
            tiles_in_direction = self.rec_find_vertical_tiles(tile_obj, direction[index])
            index += 1

            # does not add the tile the piece is on
            for x in tiles_in_direction:
                if x != self.get_location():
                    paths.append(x)

        return paths

    def rec_find_vertical_tiles(self, tile, direction, tile_list = None):
        if tile_list is None:
            tile_list = list()

        current_tile = tile.get_location()
        tile_list.append(current_tile)

        next_tile = tile.get_orthogonal_tiles(direction)

        current_tile_obj = self._board.get_tile(current_tile[0], current_tile[1])
        piece = current_tile_obj.get_piece()
        # if current tile has opponent's piece, stop
        if piece is not None and piece.get_player() != self.get_player():
            return tile_list

        # reached end of board
        if next_tile == []:
            return tile_list

        next_tile_obj = self._board.get_tile(next_tile[0][0], next_tile[0][1])

        # piece from same player blocks the next tile
        if next_tile_obj.get_piece() is not None and next_tile_obj.get_piece().get_player() == self.get_player():
            return tile_list

        else:
            next_tile_obj = self._board.get_tile(next_tile[0][0], next_tile[0][1])
            return self.rec_find_vertical_tiles(next_tile_obj, direction, tile_list)

class Elephant(Piece):
    def __init__(self, tile, player, board):
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        valid_moves = list()
        potential_paths = self.find_paths()

        for path in potential_paths:
            for step in range(0,3):
                col = path[step][0]
                row = path[step][1]
                tile = self._board.get_tile(col, row)
                piece = tile.get_piece()
                player = ""

                # if there is a piece in the first two steps of elephant's path, path is not valid
                if (step == 0 or step == 1) and piece is not None:
                    break
                # if end of path is obstructed by player's own piece, path is not valid
                if step == 2 and piece is not None and piece.get_player() == self.get_player():
                    break

                # if end of path is unobstructed or contains opponent's piece, path is valid
                elif step == 2 and (piece is None or piece.get_player() != self.get_player()):
                    valid_moves.append(path[step])

        return valid_moves

    def find_paths(self):
        # find any available orthog tiles
        orthogonal = self._tile.get_all_orthogonal_tiles()
        current = self.get_location()
        direction = list()
        paths = list()

        for step_one in orthogonal:
            if step_one[0] < current[0]:
                direction.append("LEFT")
            elif step_one[0] > current[0]:
                direction.append("RIGHT")
            elif step_one[1] < current[1]:
                direction.append("UP")
            elif step_one[1] > current[1]:
                direction.append("DOWN")

        # find the diagonals of the orthogonal tiles
        index = 0
        for orthog_tile in orthogonal:
            col = orthog_tile[0]
            row = orthog_tile[1]
            tile = self._board.get_tile(col, row)


            fork = tile.get_diagonal_tiles_extended(direction[index])

            for diagonal in fork:
                paths.append([orthog_tile, diagonal[0], diagonal[1]])

            index += 1

        return paths

class Guard(Piece):
    def __init__(self, title, player, board):
        super().__init__(title, player, board)

    def get_valid_moves(self):
        paths = self.get_paths()
        valid_moves = list()
        for path in paths:
            col = path[0]
            row = path[1]
            piece = self._board.get_piece_at_tile(col, row)
            if piece is not None and piece.get_player() == self._player:
                continue
            valid_moves.append(path)

        return valid_moves

    def get_paths(self):
        paths = list()
        adjacent = self._tile.get_adjacent_tiles()
        for tile in adjacent:
            col = tile[0]
            row = tile[1]
            if col >= 'd' and col <= 'f' and (row <= 3 or row >= 8):
                paths.append(tile)

        return paths

class General(Guard):
    def __init__(self, tile, player, board):
        super().__init__(tile, player, board)

class Horse(Piece):
    def __init__(self, tile, player, board):
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        possible_paths = self.find_paths()
        valid_paths = list()
        for x in possible_paths:
            # x is a list containing the two tiles the horse must traverse through
            # x[0] is the tuple (col, row) -- the first tile that is traversed
            first_col = x[0][0]
            first_row = x[0][1]
            first_tile = self._board.get_tile(first_col, first_row)
            piece = first_tile.get_piece()

            # x[1] is the second tile that is traversed
            second_col = x[1][0]
            second_row = x[1][1]
            second_tile = self._board.get_tile(second_col, second_row)
            piece_2 = second_tile.get_piece()

            # checks if the first tile is blocked and second tile does not contain a piece of same player
            if piece is None and (piece_2 is None or piece_2.get_player() != self.get_player()):
                valid_paths.append(x[1])

        return valid_paths

    def find_paths(self):
        """ Finds potential paths that the horse can move to. Does not check if anything is blocking """
        orthogonal = self._tile.get_all_orthogonal_tiles()
        current = self.get_location()
        direction = list()
        for step_one in orthogonal:
            if step_one[0] < current[0]:
                direction.append("LEFT")
            elif step_one[0] > current[0]:
                direction.append("RIGHT")
            elif step_one[1] < current[1]:
                direction.append("UP")
            elif step_one[1] > current[1]:
                direction.append("DOWN")

        # paths has a list containing list of paths.
        # paths = [ path1, path2, path3, etc. ]

        pathing = list()

        index = 0
        for position in orthogonal:
            # obtains the tile object at the position
            tile = self._board.get_tile(position[0], position[1])

            # obtain the diagonals at that tile (if any)
            second_tiles = tile.get_diagonal_tiles(direction[index])

            # adds all the branching paths to variable 'pathing'
            for x in second_tiles:
                pathing.append([tile.get_location(), x])

            index += 1

        return pathing

class Soldier(Piece):
    def __init__(self, tile, player, board):
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        # list containing tuples
        possible_paths = self.find_paths()
        valid_path = list()

        for path in possible_paths:
            col = path[0]
            row = path[1]
            tile = self._board.get_tile(col, row)
            piece = tile.get_piece()

            if piece is None or piece.get_player() != self._player:
                valid_path.append(path)

        return valid_path

    def find_paths(self):
        """
        Finds potential paths that the soldier can move to. Does not check if any pieces or blocking
        :return: list containing paths
        """
        current_tile = self._tile
        orthogonal = current_tile.get_all_orthogonal_tiles()

        upper_tile = current_tile.get_orthogonal_tiles("UP")[0]
        lower_tile = current_tile.get_orthogonal_tiles("DOWN")[0]

        # if the soldier is in the palace, it can also move diagonally

        # Red soldier can only move DOWN, LEFT, RIGHT
        if self._player == "RED":
            paths = [tile for tile in orthogonal if tile != upper_tile]

            # if the red soldier is in the blue palace, it may also move diagonally
            if current_tile.get_location() == ("d", 8):
                paths.append(("e", 9))
            elif current_tile.get_location() == ("f", 8):
                paths.append(("e", 9))
            elif current_tile.get_location() == ("e", 9):
                diagonal_tiles = current_tile.get_diagonal_tiles("DOWN")
                for tile in diagonal_tiles:
                    paths.append(tile)

        # Blue soldier can only move UP, LEFT, RIGHT
        if self._player == "BLUE":
            paths = [tile for tile in orthogonal if tile != lower_tile]

            # if the blue soldier is in the red palace, it may also move diagonally
            if current_tile.get_location() == ("f", 3):
                paths.append([("f", 3), ("e", 2)])
            elif current_tile.get_location() == ("d", 3):
                paths.append([("d", 3), ("e", 2)])
            elif current_tile.get_location == ("e", 2):
                paths.append(current_tile.get_diagonal_tiles("UP"))

        return paths

class JanggiTile():
    def __init__(self, board, col, row):
        self._board = board
        self._col = to_alphabetical(col)
        self._row = row
        self._piece = None

    def get_location(self):
        return (self._col, self._row)

    def get_piece(self):
        return self._piece

    def set_piece(self, piece):
        self._piece = piece

    def get_adjacent_tiles(self):
        """ Returns a list containing all coordinates of adjacent tiles """

        # create empty set
        adjacentTiles = list()
        # coordinate of current tile
        currentTile = (to_numerical(self._col), self._row)

        # nested loop to find coordinates of adjacent tiles
        for col in range(-1, 2):
            for row in range(-1, 2):

                # calculates coordinate
                adjCol = to_numerical(self._col) + col
                adjRow = self._row + row

                # checks if the tile is a valid tile
                if adjCol in range(0, 9) and adjRow in range(1, 11) \
                        and (adjCol, adjRow) != currentTile:
                    # add adjacent tile to set
                    adjCol = to_alphabetical(adjCol)
                    adjacentTiles.append((adjCol, adjRow))

        return adjacentTiles

    def get_all_diagonal_tiles(self):

        adjacent_tiles = self.get_adjacent_tiles()

        current_location = self.get_location()

        diagonal_tiles = list()

        for tile in adjacent_tiles:
            if tile[0] not in current_location and tile[1] not in current_location:
                diagonal_tiles.append(tile)

        return diagonal_tiles

    def get_diagonal_tiles(self, direction):
        """
        Returns a list containing adjacent tiles that are diagonal from current tile in a
        specified direction
        """

        all_diagonal = self.get_all_diagonal_tiles()

        current_location = self.get_location()

        tiles_in_direction = list()
        for tile in all_diagonal:

            if direction == "UP" and tile[1] < current_location[1]:
                tiles_in_direction.append(tile)

            elif direction == "DOWN" and tile[1] > current_location[1]:
                tiles_in_direction.append(tile)

            elif direction == "LEFT" and tile[0] < current_location[0]:
                tiles_in_direction.append(tile)

            elif direction == "RIGHT" and tile[0] > current_location[0]:
                tiles_in_direction.append(tile)

        return tiles_in_direction

    def get_diagonal_tiles_single(self, direction):
        all_diagonal = self.get_all_diagonal_tiles()

        current_location = self.get_location()
        tiles_in_direction = list()
        for tile in all_diagonal:
            if direction == "UL" and tile[1] < current_location[1] and tile[0] < current_location[0]:
                tiles_in_direction.append(tile)

            elif direction == "UR" and tile[1] < current_location[1] and tile[0] > current_location[0]:
                tiles_in_direction.append(tile)

            elif direction == "LL" and tile[1] > current_location[1] and tile[0] < current_location[0]:
                tiles_in_direction.append(tile)

            elif direction == "LR" and tile[1] > current_location[1] and tile[0] > current_location[0]:
                tiles_in_direction.append(tile)


        return tiles_in_direction

    def get_diagonal_tiles_extended(self, direction):
        dict = {"UP": ("UL", "UR"), "DOWN": ("LL", "LR"), "LEFT": ("UL", "LL"), "RIGHT": ("UR", "LR")}
        dir = dict[direction]

        paths = list()

        # UP => UL and UR
        first_dir_tile1 = self.get_diagonal_tiles_single(dir[0])
        if first_dir_tile1 != []:
            first_dir_tile1 = first_dir_tile1[0]
            col = first_dir_tile1[0]
            row = first_dir_tile1[1]
            tile_obj = self._board.get_tile(col, row)
            first_dir_tile2 = tile_obj.get_diagonal_tiles_single(dir[0])
            if first_dir_tile2 != []:
                first_dir_tile2 = first_dir_tile2[0]
                paths.append([first_dir_tile1, first_dir_tile2])

        second_dir_tile1 = self.get_diagonal_tiles_single(dir[1])
        if second_dir_tile1 != []:
            second_dir_tile1 = second_dir_tile1[0]
            col = second_dir_tile1[0]
            row = second_dir_tile1[1]
            tile_obj = self._board.get_tile(col, row)
            second_dir_tile2 = tile_obj.get_diagonal_tiles_single(dir[1])
            if second_dir_tile2 != []:
                second_dir_tile2 = second_dir_tile2[0]
                paths.append([second_dir_tile1, second_dir_tile2])


        return paths

    def get_all_orthogonal_tiles(self):

        adjacent_tiles = self.get_adjacent_tiles()

        current_tile = self.get_location()

        all_orthogonal = list()

        for tile in adjacent_tiles:
            # same column or same row
            if tile[0] == current_tile[0] or tile[1] == current_tile[1]:
                all_orthogonal.append(tile)
        return all_orthogonal

    def get_orthogonal_tiles(self, direction):

        all_orthogonal = self.get_all_orthogonal_tiles()

        current_tile = self.get_location()

        tiles_in_direction = list()

        for tile in all_orthogonal:
            if direction == "UP" and tile[1] < current_tile[1]:
                tiles_in_direction.append(tile)
            elif direction == "LEFT" and tile[0] < current_tile[0]:
                tiles_in_direction.append(tile)
            elif direction == "RIGHT" and tile[0] > current_tile[0]:
                tiles_in_direction.append(tile)
            elif direction == "DOWN" and tile[1] > current_tile[1]:
                tiles_in_direction.append(tile)

        return tiles_in_direction


    def rec_find_vertical_tiles(self, tile, direction, tile_list=None):
        if tile_list is None:
            tile_list = list()

        current_tile = tile.get_location()
        tile_list.append(current_tile)

        next_tile = tile.get_orthogonal_tiles(direction)

        if next_tile == []:
            return tile_list
        else:
            next_tile_obj = self._board.get_tile(next_tile[0][0], next_tile[0][1])
            return self.rec_find_vertical_tiles(next_tile_obj, direction, tile_list)


class JanggiBoard():
    def __init__(self):
        self._tiles = [[JanggiTile(self, col, row) for col in range(0, 9)] for row in range(1, 11)]
        self._red_pieces = []
        self._blue_pieces = []
        self._red_general = None
        self._blue_general = None
        self._captured = []

        self._red_set_up = {"a1": "CHARIOT", "i1": "CHARIOT",
                            "a4": "SOLDIER", "c4": "SOLDIER", "e4": "SOLDIER", "g4": "SOLDIER", "i4": "SOLDIER",
                            "b1": "ELEPHANT", "g1": "ELEPHANT",
                            "c1": "HORSE", "h1": "HORSE",
                            "d1": "GUARD", "f1": "GUARD",
                            "b3": "CANNON", "h3": "CANNON",
                            "e2": "GENERAL"}
        self._blue_set_up = {"a10": "CHARIOT", "i10": "CHARIOT",
                             "a7": "SOLDIER", "c7": "SOLDIER", "e7": "SOLDIER", "g7": "SOLDIER", "i7": "SOLDIER",
                             "b10": "ELEPHANT", "g10": "ELEPHANT",
                             "c10": "HORSE", "h10": "HORSE",
                             "d10": "GUARD", "f10": "GUARD",
                             "b8": "CANNON", "h8": "CANNON",
                             "e9": "GENERAL"}

    def add_red(self, piece):
        self._red_pieces.append(piece)

    def add_blue(self, piece):
        self._blue_pieces.append(piece)

    def set_blue_general(self, general):
        self._blue_general = general

    def get_captured(self):
        """
        Returns list of captured pieces
        :return: list object. Contains list of captured pieces
        """
        return self._captured

    def is_player_in_check(self, player, captured_pieces):
        """
        Checks if a player is in check.

        :param player:
        :param captured_pieces:
        :return: Boolean value
        """
        is_in_check = False

        # finds opponent's pieces
        opponent_pieces = None

        # general of the player to check
        general = None

        if player == "BLUE":
            opponent_pieces = self._red_pieces
            general = self._blue_general
        else:
            opponent_pieces = self._blue_pieces
            general = self._red_general

        # finds pieces belonging to the opponent that are not captured
        non_captured = [x for x in opponent_pieces if x not in captured_pieces]

        # checks if general can be captured in opponent's next turn
        # iterates through every non-captured piece
        for piece in non_captured:
            # iterates through every valid move for the opponent piece
            for move in piece.get_valid_moves():
                # if the opponent piece is able to capture player's general, player is in check
                if move == general.get_location():
                    is_in_check = True

        # return True if player is in check, False otherwise
        return is_in_check

    def get_tile(self, col, row):
        """
        returns a tile at specified coordinates

        :param col: The column of the specified tile. Must be a character between 'a' and 'i'
        :param row: The row of the specified tile

         """
        board = self._tiles

        col = to_numerical(col)

        return board[row - 1][col]

    def get_piece_at_tile(self, col, row):
        tile = self.get_tile(col, row)
        piece = tile.get_piece()
        return piece

    def move_piece(self, piece, col, row):
        """
        Moves a piece to a target location

        :param piece:
        :param col:
        :param row:
        :return:
        """

        destination_tile = self.get_tile(col, row)
        checked_piece = destination_tile.get_piece()

        # if there is a piece at the tile, it is captured (and removed from tile)
        if checked_piece is not None:
            checked_piece.set_tile(None)
            self._captured.append(checked_piece)

        # remove new_piece from old tile location
        old_tile = piece.get_tile()
        old_tile.set_piece(None)

        # set new_piece on new tile location
        destination_tile.set_piece(piece)
        piece.set_tile(destination_tile)

    def is_valid_move(self, piece, col, row):
        """
        Tests if a move places a player's general in check.
        :return: True if the move does not put player's general in check, False if it does
        """

        destination_tile = self.get_tile(col, row)
        captured_piece = destination_tile.get_piece()

        temporary_capture = self._captured.copy()
        # if there is a piece at the tile, temporarily remove from board
        if captured_piece is not None:
            captured_piece.set_tile(None)
            temporary_capture.append(captured_piece)

        # remove new_piece from old tile location
        old_tile = piece.get_tile()
        old_tile.set_piece(None)

        # set new_piece on new tile location
        destination_tile.set_piece(piece)
        piece.set_tile(destination_tile)

        # check if current player is in check after the move is made
        in_check = self.is_player_in_check(piece.get_player(), temporary_capture)

        # reverse move (restore board state)

        # captured piece (if exists) is placed back on tile
        if captured_piece is not None:
            captured_piece.set_tile(destination_tile)
            destination_tile.set_piece(captured_piece)
        # if no piece was captured, destination tile is empty
        else:
            destination_tile.set_piece(None)

        # target piece is placed back on starting tile
        old_tile.set_piece(piece)
        piece.set_tile(old_tile)

        # return True if the move placed player in check
        # return False if move does not place player in check
        return not in_check

    def set_up(self):
        """ Sets up the game board """
        for x in self._red_set_up:
            # obtains the tile the piece will be placed on
            col = x[0]
            row = int(x[1:])
            tile = self.get_tile(col, row)

            # creates the piece object for the red player
            piece_type = self._red_set_up[x]
            piece = self.create_piece(piece_type, tile, "RED", self)

            if piece_type == "GENERAL":
                self._red_general = piece

            self._red_pieces.append(piece)
            tile.set_piece(piece)

        for x in self._blue_set_up:
            # obtains the tile the piece will be placed on
            col = x[0]
            row = int(x[1:])
            tile = self.get_tile(col, row)

            # creates the piece object for the red player
            piece_type = self._blue_set_up[x]
            piece = self.create_piece(piece_type, tile, "BLUE", self)

            if piece_type == "GENERAL":
                self._blue_general = piece

            self._blue_pieces.append(piece)
            tile.set_piece(piece)

    def create_piece(self, type, tile, player, board):
        piece = None
        if type == "CHARIOT":
            piece = Chariot(tile, player, board)
        elif type == "SOLDIER":
            piece = Soldier(tile, player, board)
        elif type == "ELEPHANT":
            piece = Elephant(tile, player, board)
        elif type == "HORSE":
            piece = Horse(tile, player, board)
        elif type == "GUARD":
            piece = Guard(tile, player, board)
        elif type == "CANNON":
            piece = Cannon(tile, player, board)
        elif type == "GENERAL":
            piece = General(tile, player, board)

        return piece

    def print_board(self):
        with open("JanggiBoard_state.csv", "w") as outfile:
            for row in self._tiles:
                for col in row:
                    piece = col.get_piece()
                    player = ""
                    piece_name = ""
                    if piece is not None:
                        player = piece.get_player()
                        piece_name = type(col.get_piece()).__name__

                    outfile.write(player + piece_name)
                    if col.get_location()[0] < "i":
                        outfile.write(",")
                outfile.write("\n")

class JanggiGame():
    def __init__(self):
        self._board = JanggiBoard()
        self._board.set_up()

        self._game_state = "UNFINISHED"
        self._current_player = "BLUE"

    def get_game_state(self):
        return self._game_state

    def get_board(self):
        return self._board

    def is_in_check(self, player):
        return self._board.is_player_in_check(player.upper(), self._board.get_captured())

    def valid_col(self, col):
        """
        Checks if column input is within valid range
        :param col:
        :return:
        """
        valid_col = col >= 'a' and col <= 'i'
        return valid_col

    def valid_row(self, row):
        """
        Checks if row input is within valid range
        :param row:
        :return:
        """
        valid_row = row >= 1 and row <= 10

    def make_move(self, start, end):
        print("Attempting: ", start, "->", end)
        # if start or end is not a valid location, return false
        start_col = start[0]
        start_row = int(start[1:])
        end_col = end[0]
        end_row = int(end[1:])

        if (not self.valid_col(start_col)) and (not self.valid_row(start_row)) \
            and (not self.valid_col(end_col)) and (not self.valid_row(end_row)):

            return False

        # finds piece at start tile
        target_piece = self._board.get_piece_at_tile(start_col, start_row)

        # if no piece on start tile, return False
        if target_piece is None:
            return False

        # if target piece does not belong to current player, return False
        if target_piece.get_player() != self._current_player:
            return False

        # if end tile is not a valid move for piece, return False
        valid_moves = target_piece.get_valid_moves()
        if (end_col, end_row) not in valid_moves:
            return False

        """ UNFINISHED """
        # if move leaves general in check, return False UNLESS *************** IT IS A GAME WINNING MOVE
        # forces player to protect general if already in check
        # does not matter if in check or not... next move must not make general stay in check
        if not self._board.is_valid_move(target_piece, end_col, end_row):
            return False

        # checks if there are no moves a player can make that prevent general from being captured

        # makes move if valid
        self._board.move_piece(target_piece, end_col, end_row)

        # switch player turn
        self.switch_player()

        # return true if move was successful
        return True

    def switch_player(self):
        if self._current_player == "BLUE":
            self._current_player = "RED"
        else:
            self._current_player = "BLUE"

# must be moved inside a class
def to_alphabetical(num):
    num += 97
    return chr(num)

def to_numerical(character):
    column_dict = {}
    num = 0
    for char in range(97, 106):
        column_dict[chr(char)] = num
        num += 1

    integer = column_dict[character]
    return integer


def main():
    return

if __name__ == '__main__':
    main()
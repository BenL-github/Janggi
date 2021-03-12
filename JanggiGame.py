# Name: Benny Li
# Date: March 11, 2021
# Description: This module contains the framework for the traditional korean "chess" game of Janggi.
# Janggi is a two player game where each player takes turns to eventually capture the opponent's
# general. Each player has  general, guard, soldier, cannon, horse, chariot, and elephant pieces
# which can all move differently.

class Piece():
    """ Represents a piece on the board """

    def __init__(self, tile, player, board):
        """
        Initializes the piece
        :param tile: the tile the piece is on
        :param player: the player the piece belongs to
        :param board: the board the piece is on
        """
        self._tile = tile
        self._player = player
        self._board = board
        self._captured = False

    def get_location(self):
        """
        Returns the location of the piece
        :return: a set containing the col and row of the  pieces’s location
        """

        return self._tile.get_location()

    def get_tile(self):
        """
        Returns the tile object that the piece is on
        :return: a tile object
        """
        return self._tile

    def set_tile(self, tile):
        """
        Sets the tile object that the piece is on
        :param tile: The new tile that the piece is on
        :return: None
        """
        self._tile = tile

    def get_player(self):
        """
        Returns the player that the piece belongs to
        :return: String containing player name
        """
        return self._player


class Cannon(Piece):
    """ Represents a piece that is a cannon """

    def __init__(self, tile, player, board):
        """ Initializes the cannon piece

        :param tile: The tile that the cannon is on
        :param player: the player that the cannon belongs to
        :param board: the board that the cannon is on
        """
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        """
        Returns all possible moves the cannon is able to take
        :return: a list. The list contains tuples of each location the cannon is able to move to.
        The cannon is able to move any amount of tiles in orthogonal directions as long as there is
        a non-cannon piece to “jump” over. The cannon can only captures piece that are non-cannon.
        """

        paths = list()
        # obtains tiles in orthogonal directions
        orthogonal = self._tile.get_all_orthogonal_tiles()
        # obtains the cannon’s current location
        current = self._tile.get_location()

        # finds the direction of the orthogonal tile relative to the current position
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

        # finds all valid tiles the cannon is able to move to in a specific direction
        # index tracks the direction of the orthogonal tile
        index = 0
        for tile in orthogonal:
            # obtains the tile object at the orthogonal location
            col = tile[0]
            row = tile[1]
            tile_obj = self._board.get_tile(col, row)

            # recursively find all tiles that the cannon is able to move to in a specific direction
            tiles_in_direction = self.rec_find_vertical_tiles(tile_obj, direction[index])

            # if there are any tiles in the specific direction, append the tile to the list of
            # valid locations the cannon can move to
            if tiles_in_direction != []:
                for valid_location in tiles_in_direction:
                    paths.append(valid_location)
            #
            index += 1

        # cannon may also move diagonally within palace, if there is a piece to jump over
        if current == ("d", 1) or current == ("d", 8):
            diagonal_paths = self.rec_find_diagonal_tiles(current, "LR")
            for path in diagonal_paths:
                paths.append(path)
        elif current == ("d", 3) or current == ("d", 10):
            diagonal_paths = self.rec_find_diagonal_tiles(current, "UR")
            for path in diagonal_paths:
                paths.append(path)
        elif current == ("f", 1) or current == ("f", 8):
            diagonal_paths = self.rec_find_diagonal_tiles(current, "LL")
            for path in diagonal_paths:
                paths.append(path)
        elif current == ("f", 3) or current == ("f", 10):
            diagonal_paths = self.rec_find_diagonal_tiles(current, "UL")
            for path in diagonal_paths:
                paths.append(path)

        return paths

    def rec_find_diagonal_tiles(self, tile, direction, jumpable = False, tile_list = None):
        """
        Recursively finds the diagonal tiles if the cannon is in a palace
        :param tile: the current tile
        :param direction: the direction the cannon can move on the diagonal
        :param jumpable: boolean. True if the cannon has a piece to jump over
        :param tile_list: list of tiles the cannon can move to
        :return:
        """
        # gets current tile object
        current_tile_obj = self._board.get_tile(tile[0], tile[1])

        # stops the recursion at these tiles
        stop_tiles = [("c", 4), ("c", 7), ("g", 4), ("g", 7)]
        if tile in stop_tiles:
            return tile_list

        # initializes the tile list. Skips the first tile of the recursion because
        # it is the tile that the cannon is currently on
        if tile_list is None:
            tile_list = list()
            next_tile = current_tile_obj.get_diagonal_tiles_single(direction)
            return self.rec_find_diagonal_tiles(next_tile[0], direction, jumpable, tile_list)

        # the piece on the current tile
        piece = current_tile_obj.get_piece()

        # checks if the cannon has a piece to jump over
        if not jumpable and piece is not None:
            jumpable = True

            next_tile = current_tile_obj.get_diagonal_tiles_single(direction)

            if next_tile != []:
                return self.rec_find_diagonal_tiles(next_tile[0], direction, jumpable, tile_list)
            else:
                return tile_list
        elif not jumpable and piece is None:
            next_tile = current_tile_obj.get_diagonal_tiles_single(direction)

            if next_tile != []:
                return self.rec_find_diagonal_tiles(next_tile[0], direction, jumpable, tile_list)
            else:
                return tile_list

        elif jumpable and piece is not None:
            if piece.get_player() == self._player:
                return tile_list
            else:
                tile_list.append(tile)
                return tile_list
        elif jumpable and piece is None:
            tile_list.append(tile)
            next_tile = current_tile_obj.get_diagonal_tiles_single(direction)
            if next_tile != []:
                return self.rec_find_diagonal_tiles(next_tile[0], direction, jumpable, tile_list)
            else:
                return tile_list


    def rec_find_vertical_tiles(self, tile, direction, jumpable=False, tile_list=None):
        """
        Recursively checks if a tile in a specific direction is a valid move for the cannon
        :param tile: the current tile to check
        :param direction: the direction of next tile relative to current tile
        :param jumpable: determines if the cannon has a piece to jump over
        :param tile_list: the list of tiles that the cannon is able to move to
        :return: a list. Contains all valid locations the cannon may move to. The locations are represented as tuples.
        """
        # initializes the list to return
        if tile_list is None:
            tile_list = list()

        # finds the piece on current tile

        piece = tile.get_piece()

        # if algorithm has not found a piece to “jump” over yet, check if piece on current
        # tile is a valid piece to jump over. The piece must not be a cannon
        if jumpable is False and piece is not None and type(piece).__name__ != "Cannon":
            jumpable = True

            # checks if next tile exists
            next_tile = tile.get_orthogonal_tiles(direction)

            # if end of board is reached, stop recursion
            if next_tile == []:
                return tile_list

            # set next tile the function will check for
            col = next_tile[0][0]
            row = next_tile[0][1]
            next_tile_obj = self._board.get_tile(col, row)

            # recursively check if next tile is a valid move
            return self.rec_find_vertical_tiles(next_tile_obj, direction, jumpable, tile_list)

        # if there was a piece to jump over and current tile has no piece, current tile is a valid location
        if jumpable and piece is None:
            tile_list.append(tile.get_location())

        # if jumpable (there was a piece to jump over) and current tile has a piece,
        # check if piece is able to be captured
        elif jumpable:
            # finds the piece type and player of the piece on current tile
            piece_type = type(piece).__name__
            player = piece.get_player()

            # checks if the piece is a cannon
            isCannon = piece_type == "Cannon"
            # checks if the piece is from current player
            samePlayer = player == self.get_player()

            # stop recursive call and return list if current tile has a cannon or a
            # piece from same player (cannot capture a cannon or piece from same player)
            if isCannon or samePlayer:
                return tile_list

            # if not a cannon and not same player, tile has a piece that is able to be captured.
            else:
                tile_list.append(tile.get_location())
                return tile_list

        # checks if next tile exists
        next_tile = tile.get_orthogonal_tiles(direction)

        # if end of board is reached, return the list of available moves
        if next_tile == []:
            return tile_list

        # recursively call next tile
        col = next_tile[0][0]
        row = next_tile[0][1]
        next_tile_obj = self._board.get_tile(col, row)

        return self.rec_find_vertical_tiles(next_tile_obj, direction, jumpable, tile_list)


class Chariot(Piece):
    """ UNFINISHED THE CHARIOT NEEDS TO BE ABLE TO MOVE IN THE DIAGONALS OF THE PALACE """

    """ Represents a Chariot piece. The Chariot starts at the corners of the board. The 
    chariot can move to any space in orthogonal directions. The chariot may also move along 
    the diagonals of the palaces. """


    def __init__(self, tile, player, board):
        """ """
        super().__init__(tile, player, board)


    def get_valid_moves(self):
        """
        Returns the valid moves the chariot can take

        :return: a list. Contains all the moves the chariot can take. The moves are
        represented as a tuple containing the col and row of the tile the chariot can move to
        """
        # initialize the list to be returned
        paths = list()
        # finds the tiles that are adjacent to the piece in orthogonal directions
        orthogonal = self._tile.get_all_orthogonal_tiles()
        # finds the tile that the current piece is on
        current = self._tile.get_location()

        # direction keeps track of the direction each orthogonal tile is, relative to the current tile
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

        # finds every tile in orthogonal directions that the chariot is able to move to
        index = 0
        for tile in orthogonal:
            # retrieve tile piece is currently on
            col = self.get_location()[0]
            row = self.get_location()[1]
            tile_obj = self._board.get_tile(col, row)

            # recursively finds valid tiles to move to in each direction
            tiles_in_direction = self.rec_find_vertical_tiles(tile_obj, direction[index])
            index += 1

            # adds the valid tile to the list to be returned
            for x in tiles_in_direction:
                if x != self.get_location():
                    paths.append(x)

        # if chariot is within a palace, they can move along the diagonals

        # chariot is at the center tile of palace
        if current == ("e", 2) or current == ("e", 9):
            diagonal_tiles = self._tile.get_all_diagonal_tiles()
            for tile in diagonal_tiles:
                piece = self._board.get_piece_at_tile(tile[0], tile[1])
                if piece is None:
                    paths.append(tile)
                elif piece.get_player() != self.get_player():
                    paths.append(tile)

        # chariot is on the corner tiles of palace
        elif current == ("d", 1) or current == ("d", 8):
            diagonal_tiles = self.rec_find_diagonal_tile(current, "LR")
            for tile in diagonal_tiles:
                if tile in [("e", 2), ("f", 3), ("e", 9), ("f", 10)]:
                    paths.append(tile)

        elif current == ("f", 1) or current == ("f", 8):
            diagonal_tiles = self.rec_find_diagonal_tile(current, "LL")
            for tile in diagonal_tiles:
                if tile in [("e", 2), ("d", 3), ("e", 9), ("d", 10)]:
                    paths.append(tile)

        elif current == ("d", 3) or current == ("d", 10):
            diagonal_tiles = self.rec_find_diagonal_tile(current, "UR")
            for tile in diagonal_tiles:
                if tile in [("e", 2), ("f", 1), ("e", 9), ("f", 8)]:
                    paths.append(tile)

        elif current == ("f", 10) or current == ("f", 3):
            diagonal_tiles = self.rec_find_diagonal_tile(current, "UL")
            for tile in diagonal_tiles:
                if tile in [("e", 2), ("d", 1), ("e", 9), ("d", 8)]:
                    paths.append(tile)

        return paths

    def rec_find_diagonal_tile(self, tile, direction, tile_list = None):
        """
        Recursively finds valid diagonal tiles to move to within palace

        :param tile: current tile
        :param direction: direction of diagonal
        :param tile_list: list of tiles chariot can move to on diagonal
        :return: a list. Contains valid itles to move to
        """

        # initialize list to return
        # if first tile in recursion, skip all checks (it is the tile that the chariot is currently on)
        if tile_list is None:
            tile_list = list()
            tile_obj = self._board.get_tile(tile[0], tile[1])
            next_tile = tile_obj.get_diagonal_tiles_single(direction)

            return self.rec_find_diagonal_tile(next_tile[0], direction, tile_list)

        # checks if there are any pieces obstructing the chariot path
        current_tile_piece = self._board.get_piece_at_tile(tile[0], tile[1])
        tile_obj = self._board.get_tile(tile[0], tile[1])
        next_tile = tile_obj.get_diagonal_tiles_single(direction)

        # if current diagonal tile does not have a piece, it is a valid tile to move to
        if current_tile_piece is None:
            tile_list.append(tile)

            if next_tile != []:
                return self.rec_find_diagonal_tile(next_tile[0], direction, tile_list)
            else:
                return tile_list
        # tile has a piece on it
        else:
            player = current_tile_piece.get_player()
            if player != self._player:
                tile_list.append(tile)
                return tile_list
            else:
                return tile_list


    def rec_find_vertical_tiles(self, tile, direction, tile_list = None):
        """
        Recursively finds the tiles the chariot is able to move to in a specific direction.
        :param tile: The current tile that will be checked as a valid tile to move to
        :param direction: the direction of relative to the starting tile
        :param tile_list: list of tiles that the chariot can move to
        :return: a list. Contains all the tiles that the chariot is able to move to.
        """

        # initializes the list to be returned
        if tile_list is None:
            tile_list = list()

        # gets the location of the current tile
        current_tile = tile.get_location()
        tile_list.append(current_tile)

        # finds the next tile in the direction relative to current tile
        next_tile = tile.get_orthogonal_tiles(direction)

        # finds the tile object of the current tile
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
    """ Represents the elephant piece. There are two elephants per player on the board. The elephant may move
    in any orthogonal direction in the first step and diagonally for the second and third steps
    (both in the same direction). In total, the elephant moves three tiles per turn. There must not be any pieces
    blocking the elephant in the first and second steps. """

    def __init__(self, tile, player, board):
        """ initializes the elephant """
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        """
        Returns all valid moves the elephant can take

        :return: a list containing all valid moves the elephant can take. The moves are represented as a tuple
        containing the col and row of the tile that the elephant can move to.
        """

        # initializes the list to be returned

        valid_moves = list()

        # finds potential paths the elephant can move to
        potential_paths = self.find_paths()

        # checks if the path is blocked by any pieces
        for path in potential_paths:
            # checks if each step in the path is not blocked
            for step in range(0, 3):
                # finds the tile at each step of the path
                col = path[step][0]
                row = path[step][1]
                tile = self._board.get_tile(col, row)

                # finds the piece object and player at the tile
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
        """
        Finds potential paths that the elephant is able to move to. Does not check if the path is blocked.

        :return: a list containing all paths the elephant can potentially take. The list contains a list of
        tuples. Each list represents a path and the tuples represents each tile in the path.
        """
        # find any available orthog tiles
        orthogonal = self._tile.get_all_orthogonal_tiles()
        current = self.get_location()

        # direction keeps track of the direction of the tiles relative to the elephant
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

        # iterates through each orthogonal tile and find the two branching paths the elephant can take (if the path is
        for orthog_tile in orthogonal:
            col = orthog_tile[0]
            row = orthog_tile[1]
            tile = self._board.get_tile(col, row)

            # finds the two branching paths that the elephant can move to
            fork = tile.get_diagonal_tiles_extended(direction[index])

            # adds the two paths to the possible paths the elephant can take
            for diagonal in fork:
                paths.append([orthog_tile, diagonal[0], diagonal[1]])

            index += 1

        return paths


class Guard(Piece):
    """ Represents a guard on the board. There are two guards per player on the board.
    The guard can only move within its palace. The guard can move one step in any direction in the palace. """

    def __init__(self, title, player, board):
        """ Initializes the guard """
        super().__init__(title, player, board)

    def get_valid_moves(self):
        """
        Finds all valid moves the Guard can make.

        :return: a list. The list contains all moves the guard can make. The moves are represented by a tuple.
        """
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
        """
        Finds all potential paths that the Guard is able to take.

        :return: a list. Contains all tiles the guard can move to (if unobstructed)
        """
        # initialize the list to be returned
        paths = list()

        # finds all adjacent tiles
        adjacent = list()

        diagonals = [("e", 2), ("e", 9), ("d", 1), ("d", 3), ("f", 1), ("f", 3), ("d", 8), ("d", 10), ("f", 8), ("f", 10)]

        if self.get_location() in diagonals:
            adjacent = self._tile.get_adjacent_tiles()
        else:
            adjacent = self._tile.get_all_orthogonal_tiles()

        # checks if adjacent tile is within the palace
        for tile in adjacent:
            col = tile[0]
            row = tile[1]
            # the range of col and row that the palaces are in
            if col >= 'd' and col <= 'f' and (row <= 3 or row >= 8):
                # adds to potential paths if tile is within palace
                paths.append(tile)

        return paths


class General(Guard):
    """ Represents a general on the board. Moves similar the two guards in the palace:
    It can move in any direction as long as it is within the palace. Additionally, each
    move must not place the general in check. """

    def __init__(self, tile, player, board):
        """ initializes the general"""
        super().__init__(tile, player, board)


class Horse(Piece):
    """ Represents the horse piece. There are two horses per player on the board. The horse
    may move in any orthogonal direction on the first step and diagonally in the second step.
    The first step must be unobstructed. In total, the horse moves two tiles per turn. """

    def __init__(self, tile, player, board):
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        """
        Finds all valid moves that the horse can make.

        :return: a list. Contains all valid moves that the horse can make.
        The moves are represented as tuples of (col, row)
        """
        # finds all paths that the horse can potentially take
        possible_paths = self.find_paths()

        # initialize the list to be returned
        valid_paths = list()

        # loops through every possible path that the horse can take and checks if there are any obstructions
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

        # returns list of valid moves
        return valid_paths

    def find_paths(self):
        """
        Finds all potential paths that the horse can make. Does not take into account any blocking pieces.

        :return: a list. Contains a list of all potential paths that the horse can take. The list contains
        lists representing the path the horse can take.
        """

        # Finds tiles orthogonal to the piece
        orthogonal = self._tile.get_all_orthogonal_tiles()

        # finds the current location of the piece
        current = self.get_location()
        # direction keeps track of the direction each orthogonal tile is, relative to the piece
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

        # initialize the list to be returned
        pathing = list()

        index = 0
        # iterate through every orthogonal tile and find their branching diagonal paths (if it exists)
        for position in orthogonal:
            # obtains the tile object at the position
            tile = self._board.get_tile(position[0], position[1])

            # obtain the diagonals at that tile (if any)
            second_tiles = tile.get_diagonal_tiles(direction[index])

            # adds all the branching paths to variable 'pathing'
            for x in second_tiles:
                pathing.append([tile.get_location(), x])

            index += 1

        # returns list of paths
        return pathing


class Soldier(Piece):
    """ Represents a soldier on the board. There are four soldiers per player on the board.
    The soldier can only move either forward or to either side. It may not move backwards.
    If the soldier is in the palace, than it may move forward along the diagonals of the palace. """

    def __init__(self, tile, player, board):
        """ """
        super().__init__(tile, player, board)

    def get_valid_moves(self):
        """
        Finds all valid moves for the soldier.

        :return: a list. Contains all valid moves the soldier can move. The moves are represented as
        a tuple with each tuple being (col, row)
        """

        # Finds all possible paths the soldier may take
        possible_paths = self.find_paths()

        # initialize the list to be returned
        valid_path = list()

        # iterate through possible paths the soldier may take. It can move to any tile directly in front or to
        # either side. The path may not be obstructed by player’s on piece.
        for path in possible_paths:
            # obtains tile object at the possible path and checks if there is an obstructing piece.
            col = path[0]
            row = path[1]
            tile = self._board.get_tile(col, row)
            piece = tile.get_piece()
            # if the path is not obstructed by player’s own piece, path is a valid move
            if piece is None or piece.get_player() != self._player:
                valid_path.append(path)

        # return list of valid moves
        return valid_path

    def find_paths(self):
        """
        Finds potential paths that the soldier can move to. Does not check if any pieces are blocking the path

        :return: a list. Contains possible paths the soldier can move to. The paths are represented as
        a tuple, (col, row).
        """

        # initialize list to be returned
        paths = list()

        # finds current tile of piece
        current_tile = self._tile

        # finds all tiles orthogonal to the piece
        orthogonal = current_tile.get_all_orthogonal_tiles()

        # Finds the orthogonal tiles that are above (UP) and below the piece.
        upper_tile = current_tile.get_orthogonal_tiles("UP")
        if upper_tile != []:
            upper_tile = current_tile.get_orthogonal_tiles("UP")[0]

        lower_tile = current_tile.get_orthogonal_tiles("DOWN")
        if lower_tile != []:
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
                paths.append(("e", 2))
            elif current_tile.get_location() == ("d", 3):
                paths.append(("e", 2))
            elif current_tile.get_location == ("e", 2):
                paths.append(current_tile.get_diagonal_tiles("UP"))


        return paths


class JanggiTile():
    """ Represents a tile on the board. Each tile has location field members, an associated piece object,
    and the board it belongs to. It has methods to find tiles adjacent to a specific tile and methods to
    find the piece on a tile. """

    def __init__(self, board, col, row):
        self._board = board
        self._col = to_alphabetical(col)
        self._row = row
        self._piece = None

    def get_location(self):
        """
        Returns the location of the tile.

        :return: a tuple. Contains the col and row of the tile on the board.
        """
        return (self._col, self._row)

    def get_piece(self):
        """
        Returns the piece on the tile.

        :return: a piece object. Returns the piece object if there is a piece on the board.
        Otherwise returns None if there is no piece occupying the tile.
        """
        return self._piece

    def set_piece(self, piece):
        """
        Sets a piece onto the tile.

        :param piece: The piece to be placed onto the tile
        :return: None
        """
        self._piece = piece

    def get_adjacent_tiles(self):
        """
        Returns all adjacent tiles.

        :return: a list. Contains a list of all adjacent tiles. The tiles are represented as a tuple (col, row)
        """

        # initialize the list to be returned
        adjacentTiles = list()
        # finds coordinate of current tile as a tuple
        currentTile = (to_numerical(self._col), self._row)

        # nested loop to find coordinates of adjacent tiles. Tiles must be at a valid coordinate on the board.
        for col in range(-1, 2):
            for row in range(-1, 2):

                # calculates the coordinates adjacent to current tile
                adjCol = to_numerical(self._col) + col
                adjRow = self._row + row

                # checks if the tile is a valid tile on the board
                if adjCol in range(0, 9) and adjRow in range(1, 11) \
                        and (adjCol, adjRow) != currentTile:
                    # add adjacent tile to set
                    adjCol = to_alphabetical(adjCol)
                    adjacentTiles.append((adjCol, adjRow))

        # returns list of adjacent tile
        return adjacentTiles

    def get_all_diagonal_tiles(self):
        """
        Finds all adjacent tiles that are diagonal to tile.

        :return: a list. Contains all tiles that are diagonal to current tile. The tiles
        are represented as a tuple (col, row)
        """

        # finds all adjacent tiles
        adjacent_tiles = self.get_adjacent_tiles()

        # finds location of current tile
        current_location = self.get_location()
        # initialize list to be returned
        diagonal_tiles = list()

        # iterates through every adjacent tile and finds tiles that are diagonal to current tile
        for tile in adjacent_tiles:
            if tile[0] not in current_location and tile[1] not in current_location:
                diagonal_tiles.append(tile)
        # returns list of diagonal tiles
        return diagonal_tiles

    def get_diagonal_tiles(self, direction):
        """
        Returns diagonal tiles in a specified direction

        :param direction: The direction of diagonal tiles relative to current tile. The
        direction can either be ‘UP’, ‘DOWN’, ‘LEFT’, and ‘RIGHT’.
        :return: Returns a list containing the diagonal tiles in a specified direction.
        """
        # finds all diagonal tiles
        all_diagonal = self.get_all_diagonal_tiles()

        # finds current location
        current_location = self.get_location()

        # initialize list to be returned
        tiles_in_direction = list()

        # iterates through all diagonal tiles and finds the tiles in the specified direction.
        for tile in all_diagonal:

            if direction == "UP" and tile[1] < current_location[1]:
                tiles_in_direction.append(tile)

            elif direction == "DOWN" and tile[1] > current_location[1]:
                tiles_in_direction.append(tile)

            elif direction == "LEFT" and tile[0] < current_location[0]:
                tiles_in_direction.append(tile)

            elif direction == "RIGHT" and tile[0] > current_location[0]:
                tiles_in_direction.append(tile)

        # returns a list containing the diagonal tiles
        return tiles_in_direction

    def get_diagonal_tiles_single(self, direction):
        """
        Returns a diagonal tile in a specified direction.

        :param direction:
        :return:
        """
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
        """
        Returns diagonal tiles that are two tiles away from current tile in a specified direction.

        :param direction: The direction of the tiles
        :return: a list. Contains
        """
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
        """
        Returns all tiles that are orthogonal to current tile.

        :return: a list. Contains all tiles that are orthogonal to current tile.
        The tiles are represented as a tuple of the location that are at.
        """

        adjacent_tiles = self.get_adjacent_tiles()

        current_tile = self.get_location()

        all_orthogonal = list()

        for tile in adjacent_tiles:
            # same column or same row
            if tile[0] == current_tile[0] or tile[1] == current_tile[1]:
                all_orthogonal.append(tile)
        return all_orthogonal

    def get_orthogonal_tiles(self, direction):
        """

        :param direction:
        :return:
        """

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
        """

        :param tile:
        :param direction:
        :param tile_list:
        :return:
        """
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
    """
    """
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
        """

        :param piece:
        :return:
        """
        self._red_pieces.append(piece)

    def add_blue(self, piece):
        """

        :param piece:
        :return:
        """
        self._blue_pieces.append(piece)

    def set_blue_general(self, general):
        """ """
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
                test = general.get_location()
                if move == general.get_location():
                    is_in_check = True
                    return is_in_check

        # return True if player is in check, False otherwise
        return is_in_check

    def get_tile(self, col, row):
        """
        returns a tile at specified coordinates

        :param col: The column of the specified tile. Must be a character between 'a' and 'i'
        :param row: The row of the specified tile
        :return: tile object
         """
        board = self._tiles

        col = to_numerical(col)

        return board[row - 1][col]

    def get_piece_at_tile(self, col, row):
        """ """
        tile = self.get_tile(col, row)
        piece = tile.get_piece()
        return piece

    def move_piece(self, piece, col, row):
        """
        Moves a piece to a target location

        :param piece: The piece to be moved
        :param col: the col of the tile
        :param row: the row of the tile
        :return: None
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

        # return True if the move does not place player in check
        # return False if the move places player in check
        return not in_check

    def is_checkmated(self, player):
        """ """
        # finds all possible moves the player can make
        player_pieces = {"BLUE": [x for x in self._blue_pieces if x not in self._captured],
                  "RED": [x for x in self._red_pieces if x not in self._captured]}
        available_pieces = player_pieces[player]

        # Boolean that determines if the player is checkmated
        is_checkmated = True

        # iterate through every piece belonging to player
        for piece in available_pieces:
            # check if any move that piece can make does not leave player's general in check
            # if there is at least one valid move, player is not check_mated
            # if no valid moves, player is checkmated
            for move in piece.get_valid_moves():
                is_valid_move = self.is_valid_move(piece, move[0], move[1])
                if is_valid_move:
                    is_checkmated = False

        return is_checkmated

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
        """
        Creates a piece and places it onto the board.
        :param type:
        :param tile:
        :param player:
        :param board:
        :return:
        """
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
        """
        Prints out the board into a csv file

        :return: None
        """

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
    """ Representation of the korean chess game named 'Janggi'. Players are able to make moves with this class.
     Additionally, players can check the state of the game. The game is over if a player is unable to make a move
     that prevents the general from being captured in the next turn. Janggi game utilizes the JanggiBoard class
     to make changes to the board. """
    def __init__(self):
        self._board = JanggiBoard()
        self._board.set_up()

        self._game_state = "UNFINISHED"
        self._current_player = "BLUE"

    def get_game_state(self):
        """
        Returns the state of the Game. Can either be 'UNFINISHED', 'RED_WON', or 'BLUE_WON'
        :return: a String. The state of the game
        """
        return self._game_state

    def get_board(self):
        """
        Returns the board object associated with the game
        :return: Board object
        """
        return self._board

    def is_in_check(self, player):
        """
        Checks if a player's general is in check.

        :param player: the player to check
        :return: Boolean. True or false depending if a player is in check
        """
        return self._board.is_player_in_check(player.upper(), self._board.get_captured())

    def valid_col(self, col):
        """
        Checks if column input is within valid range
        :param col:
        :return: a boolean. True if row is valid, false if not
        """
        valid_col = col >= 'a' and col <= 'i'
        return valid_col

    def valid_row(self, row):
        """
        Checks if row input is within valid range
        :param row: the row input
        :return: bool. True if row is valid, false if not
        """
        valid_row = row >= 1 and row <= 10
        return valid_row

    def make_move(self, start, end):
        """
        Makes a move on the Janggi board. Blue player always starts first. Returns False if move was invalid.
        Returns true if valid move. The player may skip a turn if start = end.

        :param start: the piece that will be moved
        :param end: the ending location
        :return: a boolean. True if move was successful, False if not
        """

        # if game is finished, return False
        if self._game_state != "UNFINISHED":
            return False

        # if start or end is not a valid location, return false
        start_col = start[0]
        start_row = int(start[1:])
        end_col = end[0]
        end_row = int(end[1:])

        if (not self.valid_col(start_col)) and (not self.valid_row(start_row)) \
            and (not self.valid_col(end_col)) and (not self.valid_row(end_row)):

            return False

        # checks if player is attempting to pass a turn
        if start == end and not self.is_in_check(self._current_player):
            self.switch_player()
            return True
        elif start == end:
            return False


        # finds piece at start tile
        target_piece = self._board.get_piece_at_tile(start_col, start_row)

        #print(type(target_piece))

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

        # makes move if valid
        self._board.move_piece(target_piece, end_col, end_row)

        # switch player turn
        self.switch_player()

        # checks if next player is unable to make any moves to save general
        if self._board.is_checkmated(self._current_player):
            loser_winner = {"BLUE": "RED", "RED": "BLUE"}
            self.set_winner(loser_winner[self._current_player])


        self._board.print_board()

        # return true if move was successful
        return True

    def set_winner(self, player):
        """

        :param player:
        :return:
        """
        self._game_state = player + "_WON"


    def switch_player(self):
        """

        :return:
        """
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
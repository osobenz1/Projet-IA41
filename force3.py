class Force3:

    def __init__(self):
        # Initialisation de l'état du jeu
        self.reset()

    def reset(self):
        # La carte est représentée par une grille 3x3
        # 0 représente un carré vide  
        # 1 et -1 représentent les jetons de tour des deux joueurs
        # 2 représente un jeton carré
        self.board = [
            [2, 2, 2],
            [2, 0, 2],
            [2, 2, 2]
        ]
        # Le joueur 1 commence le jeu
        self.current_player = 1
        # Gardez une trace du nombre de jetons ronds placés par chaque joueur
        self.round_tokens_placed = {1: 0, -1: 0}
        # Etat du jeu - si le jeu est terminé ou non
        self.game_over = False
        # Gagnant du jeu, None si aucun gagnant n'est encore gagnant
        self.winner = None

        # Renvoie l'état initial de la carte
        return self.board
    
    def step(self, action):
        if self.game_over:
            raise Exception("Game is over. Please reset.")

        action_type, row, col, target_row, target_col = action

        # Vérifier si l'action est valide
        if not self.is_valid_move(action_type, row, col, target_row, target_col):
            raise Exception("Invalid move.")

        if action_type == 'place_round':
            self.board[row][col] = self.current_player
            self.round_tokens_placed[self.current_player] += 1
        elif action_type == 'move_square':
            self._move_square(row, col, target_row, target_col)
        elif action_type == 'move_round':
            self._move_round(row, col, target_row, target_col)

        # Rechercher un gagnant
        self.game_over, self.winner = self.check_winner()

        # Changer le joueur actuel
        if not self.game_over:
            self.current_player = -self.current_player

        return self.board, self.game_over, self.winner

    def _move_square(self, row, col, target_row, target_col):
        # Déplacer un jeton carré de (row, col) vers (target_row, target_col)
        if self.board[row][col] == 2 and self.board[target_row][target_col] == 0:
            self.board[row][col], self.board[target_row][target_col] = 0, 2

    def _move_round(self, row, col, target_row, target_col):
        # Déplacer un jeton rond de (row, col) vers (target_row, target_col)
        if self.board[row][col] == self.current_player and self.board[target_row][target_col] == 0:
            self.board[row][col], self.board[target_row][target_col] = 0, self.current_player

    def is_valid_move(self, action_type, row, col, target_row, target_col):
        # Vérifier si les indices sont dans les limites du tableau
        if not (0 <= row < 3 and 0 <= col < 3 and 0 <= target_row < 3 and 0 <= target_col < 3):
            return False

        if action_type == 'place_round':
            # Vérifier si la cellule cible est vide et si le joueur actuel n'a pas placé tous ses jetons tour
            return self.board[target_row][target_col] == 0 and self.round_tokens_placed[self.current_player] < 3
        elif action_type == 'move_square':
            # Vérifier si la cellule source a un jeton carré et que la cellule cible est vide
            return self.board[row][col] == 2 and self.board[target_row][target_col] == 0
        elif action_type == 'move_round':
            # Vérifier si la cellule source contient le jeton de tour du joueur actuel et si la cellule cible est vide
            return self.board[row][col] == self.current_player and self.board[target_row][target_col] == 0
        else:
            # Type d'action invalide
            return False
        
    def check_winner(self):
        # Vérifier les lignes horizontales, verticales et diagonales pour gagner
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                return True, self.board[row][0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                return True, self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return True, self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return True, self.board[0][2]

        # Aucun gagnant encore
        return False, None   
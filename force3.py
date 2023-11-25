import random

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
        # Le joueur 1 ou 2 commence le jeu
        self.current_player = random.choice([1, -1]) 
        # Garder une trace du nombre de jetons ronds placés par chaque joueur
        self.round_tokens_placed = {1: 0, -1: 0}
        # Etat du jeu - si le jeu est terminé ou non
        self.game_over = False
        # Gagnant du jeu, None si aucun gagnant n'est encore gagnant
        self.winner = None
        # Mémoriser le dernier mouvement
        self.last_move = None

        # Renvoie l'état initial de la carte
        return self.board
    
    def render(self):
        # Définition des symboles pour chaque type de pion
        symbols = {0: '.', 1: 'X', -1: 'O', 2: '#'}

        # Afficher chaque ligne du plateau
        for row in self.board:
            print(' '.join(symbols[piece] for piece in row))
            
        print()
    
    def step(self, action, move_two):
        if self.game_over:
            return self.board, self.game_over, self.winner, False, "Game is over. Please reset."

        action_type, row, col, target_row, target_col = action

        # Vérifier si l'action est valide
        if not self.is_valid_move(action_type, row, col, target_row, target_col):
            return self.board, self.game_over, self.winner, False, "Invalid move."

        if action_type == 'place_round':
            self.board[target_row][target_col] = self.current_player
            self.round_tokens_placed[self.current_player] += 1
        elif action_type == 'move_square':
            self._move_square(row, col, target_row, target_col, move_two)
        elif action_type == 'move_round':
            self._move_round(row, col, target_row, target_col)

        # Rechercher un gagnant
        self.game_over, self.winner = self.check_winner()

        # Changer le joueur actuel
        if not self.game_over:
            self.current_player = -self.current_player

        return self.board, self.game_over, self.winner, True, None  # Aucune erreur

    def _move_square(self, row, col, target_row, target_col, move_two):
        # Vérifies si la position cible est sur le bord de la planche
        is_edge = target_row in [0, 2] or target_col in [0, 2]
        
        if self.board[row][col] == 2 and self.board[target_row][target_col] == 0:
            if is_edge and move_two:
                # Déplacer le premier carré
                self.board[row][col], self.board[target_row][target_col] = 0, 2

                # Trouver et déplacer le deuxième carré
                second_square = self.find_second_square(row, col, target_row, target_col)
                if second_square is not None:
                    second_row, second_col = second_square
                    self.board[second_row][second_col], self.board[row][col] = 0, 2
                # Mémoriser ce mouvement pour empêcher le mouvement inverse
                self.last_move = ('move_square', row, col, target_row, target_col)
            else:
                # Déplacer un seul carré
                self.board[row][col], self.board[target_row][target_col] = 0, 2
    
    def find_second_square(self, row, col, target_row, target_col):
        # Calculer la direction du mouvement
        direction_row = target_row - row
        direction_col = target_col - col

        # Trouver le deuxième carré à déplacer en suivant la direction du mouvement
        # Vérifier d'abord si nous sommes sur une ligne, une colonne ou une diagonale
        if direction_row == 0:  # Mouvement horizontal
            next_col = target_col + direction_col
            if 0 <= next_col < 3 and self.board[target_row][next_col] == 2:
                return target_row, next_col
        elif direction_col == 0:  # Mouvement vertical
            next_row = target_row + direction_row
            if 0 <= next_row < 3 and self.board[next_row][target_col] == 2:
                return next_row, target_col
        else:  # Mouvement diagonal
            next_row = target_row + direction_row
            next_col = target_col + direction_col
            if 0 <= next_row < 3 and 0 <= next_col < 3 and self.carte[next_row][next_col] == 2:
                return next_row, next_col

        # Si aucun carré valide n'est trouvé
        return None

    def _move_round(self, row, col, target_row, target_col):
        # Déplacer un jeton rond de (row, col) vers (target_row, target_col)
        if self.board[row][col] == self.current_player and self.board[target_row][target_col] == 2:
            self.board[row][col], self.board[target_row][target_col] = 2, self.current_player

    def is_valid_move(self, action_type, row, col, target_row, target_col):
        # Vérification pour empêcher le mouvement inverse
        if self.last_move:
            last_action_type, last_row, last_col, last_target_row, last_target_col = self.last_move
            if (action_type == last_action_type and 
            row == last_target_row and col == last_target_col and
            target_row == last_row and target_col == last_col):
                return False

        if action_type == 'place_round':
            # Vérifier si la cellule cible est carrée et si le joueur actuel n'a pas placé tous ses jetons tour
            return self.board[target_row][target_col] == 2 and self.round_tokens_placed[self.current_player] < 3
        elif action_type == 'move_square':
            # Vérifier si les indices sont dans les limites du tableau
            if not (0 <= row < 3 and 0 <= col < 3 and 0 <= target_row < 3 and 0 <= target_col < 3):
                return False
            else:
            # Vérifier si la cellule source a un jeton carré ou rond et que la cellule cible est vide
                return (self.board[row][col] == 2 or self.board[row][col] == self.current_player) and self.board[target_row][target_col] == 0 and (row==target_row or col==target_col)
        elif action_type == 'move_round':
            # Vérifier si les indices sont dans les limites du tableau
            if not (0 <= row < 3 and 0 <= col < 3 and 0 <= target_row < 3 and 0 <= target_col < 3):
                return False
            else:
                # Vérifier si la cellule source contient le jeton de tour du joueur actuel et si la cellule cible est carrée
                return self.board[row][col] == self.current_player and self.board[target_row][target_col] == 2
        else:
            # Type d'action invalide
            return False
        
    def check_winner(self):
        # Vérifier les lignes horizontales, verticales et diagonales pour gagner
        for row in range(3):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2] != 0) and (self.board[row][0] == self.board[row][1] == self.board[row][2] != 2):
                return True, self.board[row][0]
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] != 0) and (self.board[0][col] == self.board[1][col] == self.board[2][col] != 2):
                return True, self.board[0][col]
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != 0) and (self.board[0][0] == self.board[1][1] == self.board[2][2] != 2):
            return True, self.board[0][0]
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] != 0) and (self.board[0][2] == self.board[1][1] == self.board[2][0] != 2):
            return True, self.board[0][2]

        # Aucun gagnant encore
        return False, None  
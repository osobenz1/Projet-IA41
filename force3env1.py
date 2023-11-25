import gym
from gym import spaces
import numpy as np
from force3 import Force3

class Force3Env(gym.Env):
    metadata = {'render.modes': ['console']}

    def __init__(self):
        super(Force3Env, self).__init__()
        self.action_space = spaces.Tuple((
            spaces.Discrete(3),  # Type d'action: placer, déplacer rond, déplacer carré
            spaces.Discrete(9),  # Position de départ: 9 cases (3x3)
            spaces.Discrete(9)   # Position cible: 9 cases (3x3)
        ))

        # L'espace d'observation pourrait être l'état du plateau
        self.observation_space = spaces.Box(low=-1, high=2, shape=(3, 3, 1), dtype=np.int32)

        self.force3 = Force3()  # Instance de la classe de jeu

        self.current_player = self.force3.current_player # Garder la trace de l'agent

    def reset(self):
        return np.array(self.force3.reset())

    def step(self, action, move_two):
        # Convertir l'action (un entier) en une action spécifique dans le jeu
        action_type, row, col, target_row, target_col = self.convert_to_action_tuple(action)

        # Appliquer l'action dans le jeu et récupérer les informations supplémentaires
        board, game_over, winner, success, error_message = self.force3.step((action_type, row, col, target_row, target_col), move_two)


        # Calculer la récompense
        reward = self.calculate_reward(game_over, winner, action_type, row, col, target_row, target_col)


        done = game_over
        info = {'winner': winner}
        return np.array(board), reward, done, info

    def convert_to_action_tuple(self, action):
        action_type_num, start_pos, target_pos = action

        # Mapper les numéros aux types d'action
        action_mapping = {0: 'place_round', 1: 'move_round', 2: 'move_square'}

        action_type = action_mapping[action_type_num]

        if action_type == 'place_round':
            # Pour les actions de placement, seule la position cible est pertinente
            target_row, target_col = divmod(target_pos, 3)
            return action_type, None, None, target_row, target_col
        else:
            # Pour les actions de déplacement, convertir les positions de départ et cible
            start_row, start_col = divmod(start_pos, 3)
            target_row, target_col = divmod(target_pos, 3)
            return action_type, start_row, start_col, target_row, target_col

    def calculate_reward(self, game_over, winner, action_type, row, col, target_row, target_col):
        # Récompenses et pénalités de base
        WIN_REWARD = 100
        LOSE_PENALTY = -100
        INVALID_MOVE = -20
        NEUTRAL_REWARD = 0

        # Récompense pour gagner
        if game_over:
            if winner == self.current_player :
                return WIN_REWARD
            elif winner is not None:
                return LOSE_PENALTY
        elif (not self.force3.is_valid_move(action_type, row, col, target_row, target_col)):
            return INVALID_MOVE
        else:
        # Récompense neutre pour les autres cas
            return NEUTRAL_REWARD

    
    def render(self, mode='console'):
        if mode == 'console':
            self.force3.render()

    def close(self):
        pass

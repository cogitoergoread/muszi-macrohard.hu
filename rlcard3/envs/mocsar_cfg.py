"""
    Mocsár Environment, Config agents
    File name: envs/gmocsar.py
    Author: József Varga
    Date created: 3/27/2020
"""

from rlcard3 import models
from rlcard3.envs.mocsar import MocsarEnv
from rlcard3.games.mocsar.stat import MocsarStat
import numpy as np
import random


class MocsarCfgEnv(MocsarEnv):
    """
    Mocsár Environment osztály
    """

    def __init__(self, config):
        super().__init__(config=config)

    def _load_model(self):
        """
        Load pretrained/rule model based on config.
        :return: A Model object
        """
        return models.load('mocsar-cfg', num_players=self.game.get_player_num())

    def run_multi_agent(self, stat: MocsarStat, seed: int = None):
        """
        Run a game with multiple agents. Can use Raw models
        :param stat: logoláshoz szükséges osztály
        :param seed: A seed for running the game. For single-process program,
        :return: Még nem tiszta
        """
        if not self.multi_agent_mode:
            raise ValueError('run_multi_agent() can only be used in multi_agent_mode')
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        state, player_id = self.init_game()
        stat.add_startgame()

        while not self.is_over():
            if self.model.use_raw:
                action, _ = self.model.agents[player_id].eval_step(state)
            else:
                action, _ = self.model.agents[player_id].eval_step(self._extract_state(state))

            if state['is_extract']:
                # self.game.step() requires str action
                action = self._decode_action(action)
            state, player_id = self.game.step(action)

        payoffs = self.get_payoffs()
        done = True
        return state, payoffs, done
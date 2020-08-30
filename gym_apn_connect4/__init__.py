from gym.envs.registration import register

register(
    id='apn_connect4-v0',
    entry_point='gym_foo.envs:ApnConnect4Env',
)
register(
    id='apn_connect4-extrahard-v0',
    entry_point='gym_apn_connect4.envs:ApnConnect4ExtraHardEnv',
)

from pyboy import PyBoy, WindowEvent

if __name__ == "__main__":
    
    pyboy = PyBoy('rom/PokemonRed.gb', game_wrapper=True)

    pyboy.set_emulation_speed(1)

    poke_red = pyboy.game_wrapper()
    poke_red.start_game()

    print(poke_red.get_player_monster(0))

    with open('game_states/base.state', 'rb') as f:
        pyboy.load_state(f)

    while not pyboy.tick():
        pass
    pyboy.stop()

    # with open('game_states/base.state', 'wb') as f:
    #     pyboy.save_state(f)

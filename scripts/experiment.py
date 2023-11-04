from pyboy import PyBoy, WindowEvent

if __name__ == "__main__":
    
    pyboy = PyBoy('rom/PokemonRed.gb', game_wrapper=True)

    pyboy.set_emulation_speed(0)

    poke_red = pyboy.game_wrapper()
    poke_red.start_game()

    print(type(poke_red))

    with open('game_states/base.state', 'rb') as f:
        pyboy.load_state(f)

    while not pyboy.tick():
        pass
    pyboy.stop()

    # with open('game_states/base.state', 'wb') as f:
    #     pyboy.save_state(f)

from pyboy import PyBoy, WindowEvent

if __name__ == "__main__":
    
    pyboy = PyBoy('rom/PokemonRed.gb', game_wrapper=True)

    pyboy.set_emulation_speed(0)

    poke_red = pyboy.game_wrapper()
    poke_red.start_game()

    with open('game_states/base.state', 'rb') as f:
        pyboy.load_state(f)

    ticks = 100

    while not pyboy.tick():
        print(poke_red.get_player_location())
        for i in range(ticks-1):
            pyboy.tick()
    pyboy.stop()

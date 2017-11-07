
import sys
import game_engine.engine_helpers as helpers
USE_CURSES = False
if sys.platform == 'linux' or sys.platform == 'linux2':
    import curses
    USE_CURSES = True

def main():
    my_ui = helpers.ui()
    curses.wrapper(my_ui.init_windows)
    my_ui.write_main(helpers.SPLASH_MESSAGE, col=5)
    my_ui.write_input('is')
    my_ui.write_time('uncle')

    my_ui.write_stat('your')
    text = my_ui.get_input()
    print text





if __name__ == '__main__':
    main()

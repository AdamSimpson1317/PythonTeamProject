try:
    from program import main_gui
except ModuleNotFoundError:
    from .program import main_gui

if __name__ == '__main__':
    main_gui.main()

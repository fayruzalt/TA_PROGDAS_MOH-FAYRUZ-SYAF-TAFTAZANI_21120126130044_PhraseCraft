from logic import PhraseCraftManager
from ui import PhraseCraftGUI


def main():
    manager = PhraseCraftManager()
    app = PhraseCraftGUI(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
from controllers import ISDController
from entities import LocalState, FTPTap

if __name__ == '__main__':
    state = LocalState()
    controller = ISDController(state)
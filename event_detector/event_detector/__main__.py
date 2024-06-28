from controllers import ISDController
from entities import LocalState, FTPTap

if __name__ == '__main__':
    state = LocalState()
    controller = ISDController(state)
    controller.get_and_dispatch_changed_events()
    controller.write_state()
    breakpoint()
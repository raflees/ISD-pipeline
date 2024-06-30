from controllers import ISDController
from entities import CloudStorageState

if __name__ == '__main__':
    state = CloudStorageState()
    controller = ISDController(state)
    controller.get_and_dispatch_changed_events()
    controller.write_state()
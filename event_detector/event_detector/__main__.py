from controllers import ISDController
from entities import CloudStorageState, PubSubDispatcher, LocalState

if __name__ == '__main__':
    project_id = 'cellular-retina-427804-i7'
    pattern = "A(.*).gz"
    
    dispatcher = PubSubDispatcher(project_id, 'isd-pipeline-changed-files')
    state = CloudStorageState(project_id, 'isd-pipeline-state', 'state.json')

    controller = ISDController(
        pattern=pattern,
        state=state,
        dispatcher=dispatcher)
    controller.get_and_dispatch_changed_events()
    controller.write_state()
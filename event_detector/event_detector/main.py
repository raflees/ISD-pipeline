from event_detector.controllers import ISDController
from event_detector.entities import CloudStorageState, PubSubDispatcher, LocalState

def run(pattern="A(.*).gz"):
    project_id = 'cellular-retina-427804-i7'
    
    dispatcher = PubSubDispatcher(project_id, 'isd-pipeline-changed-files')
    state = CloudStorageState(project_id, 'isd-pipeline-state', 'state.json')

    controller = ISDController(
        pattern=pattern,
        state=state,
        dispatcher=dispatcher)
    controller.get_and_dispatch_changed_events()
    controller.write_state()
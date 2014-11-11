import asyncio
import locale
import os
import inspect
import sys
from asyncio.subprocess import PIPE


TARGET_PLATFORM = {
  'cygwin': 'win32',
  'darwin': 'darwin',
  'linux': 'linux',
  'win32': 'win32',
}[sys.platform]

SOURCE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
THRUST_PATH = os.path.join(SOURCE_ROOT, '..', 'vendor', 'thrust')
THRUST_EXEC = { 
    'linux': os.path.join(THRUST_PATH, 'thrust_shell'),
    'win32': os.path.join(THRUST_PATH, 'thrust_shell'),
    'darwin': os.path.join(THRUST_PATH, 'ThrustShell.app', 'Contents',
        'MacOS', 'ThrustShell')
}[TARGET_PLATFORM]

BOUNDARY = '--(Foo)++__THRUST_SHELL_BOUNDARY__++(Bar)--'

ACTIONS = {}
ACTION_ID = 0

@asyncio.coroutine
def spawn(loop=None, exec_path=None):
    global ACTIONS
    if loop is None:
        loop = asyncio.get_event_loop()
    if exec_path is None:
        exec_path = THRUST_EXEC
    print("exec_path: ", THRUST_EXEC)
    
    # start Thrust process
    proc = yield from asyncio.create_subprocess_exec(exec_path, 
                                                     stdin=PIPE, 
                                                     stdout=PIPE, 
                                                     loop=loop)
    print("pid: %s" % proc.pid)

    acc = '';
    while True:
        line = yield from proc.stdout.readline()
        if not line:
            break
        acc = acc + line.decode('utf8').rstrip();
        splits = acc.split(BOUNDARY);

        while len(splits) > 1:
            data = splits.pop(0)
            acc = splits.join(BOUNDARY)
            if data and len(data) > 0:
                try:
                    action = json.loads(data)
                    print("action: ", action['_action'])
                except Exception:
                    print("Could not parse JSON")
        try:
            proc.send_signal(signal.SIGINT)
        except ProcessLookupError:
             pass
    process.kill()
    rc = yield from process.wait()
    return rc;


@asyncio.coroutine
def perform(action, loop=None):
    global ACTIONS
    if loop is None:
        loop = asyncio.get_event_loop()
    condition = asyncio.Condition(loop=loop)
    sync = {
        'condition': condition,
        'error': None,
        'result': None
    }
    ACTIONS[str(action['_id'])] = sync
    yield from condition.acquire()
    yield from condition.wait()
    result = sync['result']
    del ACTIONS[str(action['_id'])]
    return result

def action_id():
    global ACTION_ID
    ACTION_ID = ACTION_ID + 1;
    return ACTION_ID

def register(obj):
    pass

def unregister(obj):
    pass



#if os.name == 'nt':
#    loop = asyncio.ProactorEventLoop()
#    asyncio.set_event_loop(loop)

loop = asyncio.get_event_loop()
asyncio.async(perform({ '_id': action_id() }, loop=loop))
print("TEST", str(action_id()))
asyncio.async(perform({ '_id': action_id() }, loop=loop))
print("TEST", str(action_id()))
loop.run_until_complete(spawn());




import asyncio
import locale
import os
import inspect
import sys
import json
import signal

from asyncio.subprocess import PIPE

from .window import Window

class API:
    def __init__(self, loop=None):
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.TARGET_PLATFORM = {
            'cygwin': 'win32',
            'darwin': 'darwin',
            'linux': 'linux',
            'win32': 'win32',
        }[sys.platform]
        self.SOURCE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(
            inspect.currentframe())))
        self.THRUST_PATH = os.path.join(self.SOURCE_ROOT, '..', 'vendor', 
            'thrust')
        self.THRUST_EXEC = {
            'linux': os.path.join(self.THRUST_PATH, 'thrust_shell'),
            'win32': os.path.join(self.THRUST_PATH, 'thrust_shell'),
            'darwin': os.path.join(self.THRUST_PATH, 'ThrustShell.app', 
                'Contents', 'MacOS', 'ThrustShell')
        }[self.TARGET_PLATFORM]
    
        self.BOUNDARY = '--(Foo)++__THRUST_SHELL_BOUNDARY__++(Bar)--'
    
        self.actions = {}
        self.objects = {}

        self.next_id = 0
        self.proc = None
        self.spawn_cnd = asyncio.Condition(loop=self.loop)

    @asyncio.coroutine
    def spawn(self, exec_path=None):
        if exec_path is None:
            exec_path = self.THRUST_EXEC
        print("exec_path: ", exec_path)
    
        # start Thrust process
        self.proc = yield from asyncio.create_subprocess_exec(exec_path, 
                                                              stdin=PIPE, 
                                                              stdout=PIPE, 
                                                              loop=self.loop)
        yield from self.spawn_cnd.acquire()
        print("pid: %s" % self.proc.pid)
        self.spawn_cnd.notify_all()
        self.spawn_cnd.release()

        acc = '';
        while True:
            line = yield from self.proc.stdout.readline()
            if not line:
                break
            acc = acc + line.decode('utf8').rstrip();
            splits = acc.split(self.BOUNDARY);
    
            while len(splits) > 1:
                data = splits.pop(0)
                acc = self.BOUNDARY.join(splits)
                if data and len(data) > 0:
                    action = json.loads(data)
                    print('RECEIVED: ', str(action))
                    if action['_action'] == 'reply':
                        sync = self.actions[str(action['_id'])]
                        if sync is not None:
                            sync['error'] = action['_error']
                            sync['result'] = action['_result']
                            yield from sync['condition'].acquire()
                            sync['condition'].notify_all()
                            sync['condition'].release()
                    if action['_action'] == 'event':
                        obj = self.objects[str(action['_target'])]
                        if obj is not None:
                            obj.emit(action['_type'], action['_event'])
                    if action['_action'] == 'invoke':
                        obj = self.objects[str(action['_target'])]
                        if obj is not None:
                            pass

        try:
            self.proc.kill()
        except ProcessLookupError:
            pass
        rc = yield from self.proc.wait()
        return rc;

    @asyncio.coroutine
    def pre(self):
        if self.proc is None:
            yield from self.spawn_cnd.acquire()
            yield from self.spawn_cnd.wait()
            self.spawn_cnd.release()

    @asyncio.coroutine
    def perform(self, action):
        yield from self.pre()
        condition = asyncio.Condition(loop=self.loop)
        sync = {
            'condition': condition,
            'error': None,
            'result': None
        }
        self.actions[str(action['_id'])] = sync
        print('PERFORM: ', json.dumps(action))
        data = str(json.dumps(action)) + '\n' + self.BOUNDARY + '\n'
        self.proc.stdin.write(data.encode())
        yield from condition.acquire()
        yield from condition.wait()
        condition.release()
        result = sync['result']
        del self.actions[str(action['_id'])]
        return result
    
    def action_id(self):
        self.next_id = self.next_id + 1;
        return self.next_id
    
    def register(self, obj):
        self.objects[str(obj.target)] = obj;

    def unregister(self, obj):
        del self.objects[str(obj.target)];

    def window(self, args):
        return Window(self, args, loop=self.loop)


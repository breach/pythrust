import asyncio
import pyee

class Base(pyee.EventEmitter):
    def __init__(self, api, type, args, loop=None):
        super().__init__()
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop
        print('BASE CONSTRUCTOR')
        self.api = api
        self.type = type
        self.target = None
        self.destroyed = False
        self.create_cnd = asyncio.Condition(loop=loop)
        asyncio.async(self.create(args))

    @asyncio.coroutine
    def create(self, args):
        result = yield from self.api.perform({
            '_id': self.api.action_id(),
            '_action': 'create',
            '_type': self.type,
            '_args': args
        })
        self.target = result['_target']
        self.api.register(self)
        yield from self.create_cnd.acquire()
        self.create_cnd.notify_all()
        self.create_cnd.release()
    
    @asyncio.coroutine
    def destroy(self):
        result = yield from self.api.perform({
            '_id': self.api.action_id(),
            '_action': 'delete',
            '_target': self.target
        }, loop=self.loop)
        self.destroyed = True
        self.api.unregister(self)

    @asyncio.coroutine
    def pre(self):
        if self.target is None:
            yield from self.create_cnd.acquire()
            yield from self.create_cnd.wait()
            self.create_cnd.release()

    @asyncio.coroutine
    def call(self, method, args):
        yield from self.pre()
        result = yield from self.api.perform({
            '_id': self.api.action_id(),
            '_action': 'call',
            '_target': self.target,
            '_method': method,
            '_args': args
        })
        return result

    @asyncio.coroutine
    def invoke(self, method, args):
        yield from self.pre()
        if self['invoke_' + method] is not None:
            raise NameError('Method not found [', self.type, ']: ', method)
        result = yield from self['infoke_' + method]()
        return result






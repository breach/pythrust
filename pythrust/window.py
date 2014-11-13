import asyncio
from base import Base

class Window(Base):
    def __init__(self, api, args, loop=None):
        super().__init__(api, 'window', args, loop=loop)
        print('WINDOW CONSTRUCTOR')

    @asyncio.coroutine
    def create(self, args):
        if 'session' in args:
            yield from args.session.pre()
        yield from super().create(args)

    @asyncio.coroutine
    def show(self):
      r = yield from super().call('show', {})
      return r

    @asyncio.coroutine
    def focus(self):
      r = yield from super().call('focus', {})
      return r

    @asyncio.coroutine
    def maximize(self):
      r = yield from super().call('maximize', {})
      return r

    @asyncio.coroutine
    def unmaximize(self):
      r = yield from super().call('unmaximize', {})
      return r

    @asyncio.coroutine
    def close(self):
      r = yield from super().call('close', {})
      return r

    @asyncio.coroutine
    def set_title(self, title):
      r = yield from super().call('set_title', { 
          'title': title
      })
      return r

    @asyncio.coroutine
    def set_fullscreen(self, fullscreen):
      r = yield from super().call('set_fullscreen', { 
          'fullscreen': fullscreen 
      })
      return r

    @asyncio.coroutine
    def set_kiosk(self, fullscreen):
      r = yield from super().call('set_kiosk', { 
          'kiosk': kiosk 
      })
      return r

    @asyncio.coroutine
    def open_devtools(self):
      r = yield from super().call('open_devtools', {})
      return r

    @asyncio.coroutine
    def close_devtools(self):
      r = yield from super().call('close_devtools', {})
      return r

    @asyncio.coroutine
    def move(self, x, y):
      r = yield from super().call('move', {
          'x': x,
          'y': y
      })
      return r

    @asyncio.coroutine
    def resize(self, width, height):
      r = yield from super().call('resize', {
          'width': width,
          'width': height
      })
      return r

    @asyncio.coroutine
    def is_closed(self):
      r = yield from super().call('is_closed', {})
      return r['closed']

    @asyncio.coroutine
    def is_maximized(self):
      r = yield from super().call('is_maximized', {})
      return r['maximized']

    @asyncio.coroutine
    def is_minimized(self):
      r = yield from super().call('is_minimized', {})
      return r['minimized']

    @asyncio.coroutine
    def is_fullscreen(self):
      r = yield from super().call('is_fullscreen', {})
      return r['fullscreen']

    @asyncio.coroutine
    def is_kiosk(self):
      r = yield from super().call('is_kiosk', {})
      return r['kiosk']

    @asyncio.coroutine
    def is_devtools_opened(self):
      r = yield from super().call('is_devtools_opened', {})
      return r['opened']

    @asyncio.coroutine
    def size(self):
      r = yield from super().call('size', {})
      return r['size']

    @asyncio.coroutine
    def position(self):
      r = yield from super().call('position', {})
      return r['position']


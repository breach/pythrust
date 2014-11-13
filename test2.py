import asyncio

from pythrust import API
from pythrust import Window

#if os.name == 'nt':
#    loop = asyncio.ProactorEventLoop()
#    asyncio.set_event_loop(loop)

loop = asyncio.get_event_loop()
api = API(loop)

asyncio.async(api.spawn())

window = api.window({})

@window.on('focus')
def window_focus(evt):
  print('FOCUS!!!', str(evt))

asyncio.async(window.show())

@asyncio.coroutine
def go():
  closed = yield from window.is_closed()
  print('CLOSED: ', str(closed))
  size = yield from window.size()
  print('SIZE: ', str(size))

asyncio.async(go())

loop.run_forever()
#loop.run_until_complete(api.spawn())


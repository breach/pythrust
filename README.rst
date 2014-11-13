pythrust
========

Official Python bindings library for [Thrust](https://github.com/breach/thrust)

### Getting Started
```
import pythrust

loop = asyncio.get_event_loop()
api = pythrust.API(loop)

asyncio.async(api.spawn())

window = api.window({})
asyncio.async(window.show())

loop.run_forever()
```

pythrust
========

.. _Thrust: https://github.com/breach/thrust

Official Python bindings library for Thrust_

Getting Started
===============

::

    import pythrust
    import asyncio

    loop = asyncio.get_event_loop()
    api = pythrust.API(loop)

    asyncio.async(api.spawn())
  
    window = api.window({})
    asyncio.async(window.show())
  
    loop.run_forever()

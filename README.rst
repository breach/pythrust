pythrust
========

.. _Thrust: https://github.com/breach/thrust

Official Python bindings library for Thrust_

Getting Started
===============

``pythrust`` requires Python 3 as it relies on the ``asyncio`` module.

::

    pip3 install pythrust [--user]


::

    import pythrust
    import asyncio

    loop = asyncio.get_event_loop()
    api = pythrust.API(loop)

    asyncio.async(api.spawn())
  
    window = api.window({})
    asyncio.async(window.show())
  
    loop.run_forever()


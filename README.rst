pythrust
========

.. _Thrust: https://github.com/breach/thrust
.. _Python3: https://www.python.org/
.. _`Thrust Documentation`: https://github.com/breach/thrust/tree/master/docs

Official Python bindings library for Thrust_

Getting Started
===============

``pythrust`` requires Python3_ as it relies on the ``asyncio`` module.

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

Status
======

Support is only limited to the ``window`` object for now. Contributions are
welcomed

Support tested on Linux and MacOSX. Still a few bugs on Windows.

Documentation
=============

Pending specific pythrust documentation, full API reference is available 
in the `Thrust Documentation`_

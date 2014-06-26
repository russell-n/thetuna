The Iperf
=========

A set of convenience classes and methods for running iperf traffic.

Contents:

    * :ref:`ClientServer named tuple <iperf-client-server-namedtuple>`
    * :ref:`Iperf Class <iperf-class>`
    * :ref:`Event Timer <iperf-event-timer>`
    * :ref:`Iperf Constants (enum) <iperf-enum>`
    * :ref:`Iperf Configuration <iperf-configuration>`
    * :ref:`Iperf Metric <iperf-metric>`



.. _iperf-client-server-namedtuple:

The ClientServer NamedTuple
---------------------------

This is a namedtuple to pass around the client and server  for different directions.

::

    ClientServer = namedtuple('ClientServer', 'client server'.split())
    
    



.. _iperf-class:

The Iperf Class
---------------

.. note:: In order to allow the `Component` that the user sees to be called `Iperf` the class here is re-named `IperfClass` to both mangle the name and refer to the fact that it now returns the bandwidth rather than just recording the output. I originally called it `IperfMetric` but since I need something to interpret the directions it is just `IperfClass`.

.. uml::

   BaseClass <|-- IperfClass
   IperfClass o- EventTimer
   IperfClass o- ClientServer
   IperfClass o- HostSSH
   IperfClass o- IperfParser
   IperfClass o- FileStorage
   IperfClass o- LogWriter
   IperfClass o- IperfClientSettings
   IperfClass o- IperfServerSettings

.. currentmodule:: tuna.commands.iperf.iperf
.. autosummary::
   :toctree: api

   IperfClass
   IperfClass.event_timer
   IperfClass.client_server
   IperfClass.udp
   IperfClass.__call__
   IperfClass.downstream
   IperfClass.upstream
   IperfClass.run
   IperfClass.start_server
   IperfClass.run_client
   IperfClass.version
   IperfClass.parser
   IperfClass.aggregator
   



.. _iperf-event-timer:

Event Timer
-----------

This should go somewhere else... I normally use this class as a timer to keep periodic intervals (e.g. to read a proc file every second), but what the hell. This bundles a threading.Timer and threading.Event. The idea is someone would make it blocking::

    t = EventTimer(5)
    t.clear()
    <do something that others should wait for>

Then someone else would wait until the timer was done before proceeding::

    t.wait()
    <do something>

.. autosummary::
   :toctree: api

   EventTimer
   EventTimer.event
   EventTimer.timer
   EventTimer.set
   EventTimer.clear
   EventTimer.wait



.. _iperf-enum:

Iperf Enum
----------

A holder of constants.



.. _iperf-configuration:

Iperf Configuration
-------------------

A configuration for iperf testing.

.. currentmodule:: tuna.commands.iperf.iperf
.. autosummary::
   :toctree: api

   IperfConfiguration
   IperfConfiguration.direction
   IperfConfiguration.client_settings
   IperfConfiguration.server_settings
   IperfConfiguration.get_section_dict
   IperfConfiguration.reset
   IperfConfiguration.check_rep
   IperfConfiguration.example
   IperfConfiguration.section
   


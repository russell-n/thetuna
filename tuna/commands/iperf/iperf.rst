The Iperf
=========

A set of convenience classes and methods for running iperf traffic.

Contents:

    * :ref:`ClientServer named tuple <iperf-client-server-namedtuple>`
    * :ref:`Iperf Class <iperf-class>`
    * :ref:`Event Timer <iperf-event-timer>`



.. _iperf-client-server-namedtuple:

The ClientServer NamedTuple
---------------------------

This is a namedtuple to pass around the client and server  for different directions.

::

    ClientServer = namedtuple('ClientServer', 'client server'.split())
    
    



.. _iperf-class:

The Iperf Class
---------------

.. uml::

   BaseClass <|-- Iperf
   Iperf o- EventTimer
   Iperf o- ClientServer
   Iperf o- HostSSH
   Iperf o- IperfClientSettings
   Iperf o- IperfServerSettings

.. currentmodule:: tuna.commands.iperf.iperf
.. autosummary::
   :toctree: api

   Iperf
   Iperf.event_timer
   Iperf.client_server
   Iperf.udp
   Iperf.__call__
   Iperf.downstream
   Iperf.upstream
   Iperf.run
   Iperf.start_server
   Iperf.run_client
   Iperf.version



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
   


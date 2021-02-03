# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #

# !/usr/bin/env python
"""
Module for daemonising the queue processor.
"""
import logging
import signal
import time
from typing import Optional
from utils.clients.queue_client import QueueClient

from queue_processors.daemon import Daemon, control_daemon_from_cli
from queue_processors.queue_processor import queue_listener


class QueueListenerDaemon(Daemon):
    """ Queue Listener daemoniser """
    def __init__(self, *args, **kwargs):
        """ Initialise the queue_processor daemon """
        super().__init__(*args, **kwargs)

        self._client_handle: Optional[QueueClient] = None
        self._listener_handle: Optional[queue_listener.QueueListener] = None
        self._logger = logging.getLogger(__file__)
        self._shutting_down = False
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)

    def run(self):
        """ Run queue processor. """
        self._logger.info("Starting Queue Processor")
        self._client_handle = queue_listener.main()
        # keeps the daemon alive as the main call above does not block
        # but simply runs the connections in async. If this sleep isn't
        # here the deamon will just exit after connecting
        while True:
            time.sleep(0.5)

    def stop(self, *args):
        """
        Stops the Queue Processor Daemon, first making sure that
        the underlying client has finished
        """

        self._shutting_down = True
        if self._client_handle is None:
            self._logger.info("Cannot safely disconnect _client_handle as it is "
                              "running in original process. Messages might get lost. "
                              "This happens when the process is manually stopped from CLI.")
        else:
            self._client_handle.disconnect()
            self._logger.info("Queue Processor exited gracefully from SIGTERM")


def main():
    """ Main method. """
    daemon = QueueListenerDaemon('/tmp/QueueListenerDaemon.pid')
    control_daemon_from_cli(daemon)


if __name__ == "__main__":
    main()

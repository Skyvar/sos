# Copyright (C) 2018 Red Hat, Inc. Jake Hunsaker <jhunsake@redhat.com>

# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, RedHatPlugin


class Fibrechannel(Plugin, RedHatPlugin):
    """Collects information on fibrechannel devices, if present"""

    plugin_name = 'fibrechannel'
    profiles = ('hardware', 'storage', 'system')
    files = ('/sys/class/fc_host')

    def setup(self):
        self.add_blockdev_cmd("udevadm info -a %(dev)s", devices='fibre')

# vim: set et ts=4 sw=4 :

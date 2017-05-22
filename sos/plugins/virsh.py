# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from sos.plugins import Plugin, RedHatPlugin, UbuntuPlugin, DebianPlugin
import glob
import os


class LibvirtClient(Plugin, RedHatPlugin, UbuntuPlugin, DebianPlugin):
    """client for libvirt virtualization API
    """

    plugin_name = 'virsh'
    profiles = ('system', 'virt')

    packages = ('libvirt-client')

    def setup(self):
        # virt-manager logs
        if not self.get_option("all_logs"):
            self.add_copy_spec("/root/.virt-manager/*", sizelimit=5)
        else:
            self.add_copy_spec("/root/.virt-manager/*")

        cmd = 'virsh -r'

        # get host information
        subcmds = [
            'list --all',
            'domcapabilities',
            'capabilities',
            'nodeinfo',
            'freecell',
            'node-memory-tune',
            'version'
        ]

        for subcmd in subcmds:
            self.add_cmd_output('%s %s' % (cmd, subcmd))

        # get network, pool and nwfilter elements
        for k in ['net', 'nwfilter', 'pool']:
            self.add_cmd_output('%s %s-list' % (cmd, k))
            k_list = self.get_command_output('%s %s-list' % (cmd, k))
            if k_list and k_list['status'] == 0:
                k_lines = k_list['output'].splitlines()
                # the 'Name' column position changes between virsh cmds
                pos = k_lines[0].split().index('Name')
                for j in filter(lambda x: x, k_lines[2:]):
                    n = j.split()[pos]
                    self.add_cmd_output('%s %s-dumpxml %s' % (cmd, k, n))

        # cycle through the VMs/domains list, ignore 2 header lines and latest
        # empty line, and dumpxml domain name in 2nd column
        domains_output = self.get_command_output('%s list --all' % cmd)
        if domains_output and domains_output['status'] == 0:
            domains_lines = domains_output['output'].splitlines()[2:]
            for domain in filter(lambda x: x, domains_lines):
                d = domain.split()[1]
                for x in ['dumpxml', 'dominfo', 'domblklist']:
                    self.add_cmd_output('%s %s %s' % (cmd, x, d))
# vim: et ts=4 sw=4

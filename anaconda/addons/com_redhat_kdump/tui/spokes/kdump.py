# Kdump anaconda configuration
#
# Copyright (C) 2013 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): David Shea <dshea@redhat.com>
#

"""Kdump anaconda TUI configuration"""

import os.path
import re

from pyanaconda.core.kernel import kernel_arguments
from pyanaconda.ui.categories.system import SystemCategory
from pyanaconda.ui.tui.spokes import NormalTUISpoke
from pyanaconda.ui.tui.tuiobject import Dialog
from simpleline.render.widgets import CheckboxWidget, EntryWidget
from simpleline.render.containers import ListColumnContainer
from simpleline.render.screen import InputState
from com_redhat_kdump.common import getMemoryBounds
from com_redhat_kdump.i18n import N_, _
from com_redhat_kdump.constants import FADUMP_CAPABLE_FILE

__all__ = ["KdumpSpoke"]

class KdumpSpoke(NormalTUISpoke):
    category = SystemCategory
    help_id = "KdumpSpoke"

    def __init__(self, *args):
        super().__init__(*args)
        self.title = N_("Kdump")
        self._addon_data = self.data.addons.com_redhat_kdump

        self._lower, self._upper, self._step = getMemoryBounds()
        # Allow either "auto" or a string of digits optionally followed by 'M'
        self._reserve_check_re = re.compile(r'^((auto)|(\d+M?))$')

        self._container = None

    @classmethod
    def should_run(cls, environment, data):
        # the KdumpSpoke should run only if requested
        return kernel_arguments.get("kdump_addon", default=True) not in ["0", "off", False]

    def apply(self):
        pass

    @property
    def completed(self):
        return True

    @property
    def status(self):
        if self._addon_data.enabled:
            state = _("Kdump is enabled")
        else:
            state = _("Kdump is disabled")
        return state

    def refresh(self, args=None):
        super().refresh(args)

        self._container = ListColumnContainer(1)
        self.window.add(self._container)

        self._create_enable_checkbox()

        if self._addon_data.enabled:
            self._create_fadump_checkbox()
            self._create_reserve_amount_text_widget()

        self.window.add_separator()

    def _create_enable_checkbox(self):
        enable_kdump_checkbox = CheckboxWidget(title=_("Enable kdump"),
                                               completed=self._addon_data.enabled)
        self._container.add(enable_kdump_checkbox, self._set_enabled)

    def _create_fadump_checkbox(self):
        if not os.path.exists(FADUMP_CAPABLE_FILE):
            return

        enable_fadump_checkbox = CheckboxWidget(title=_("Enable dump mode fadump"),
                                                completed=self._addon_data.enablefadump)
        self._container.add(enable_fadump_checkbox, self._set_fadump_enable)

    def _create_reserve_amount_text_widget(self):
        title = _("Reserve amount (%d - %d MB)" % (self._lower, self._upper))
        reserve_amount_entry = EntryWidget(title=title, value=self._addon_data.reserveMB)
        self._container.add(reserve_amount_entry, self._get_reserve_amount)

    def _set_enabled(self, data):
        self._addon_data.enabled = not self._addon_data.enabled

    def _set_fadump_enable(self, data):
        self._addon_data.enablefadump = not self._addon_data.enablefadump

    def _get_reserve_amount(self, data):
        text = "Reserve amount (%d - %d MB)" % (self._lower, self._upper)
        dialog = Dialog(title=text, conditions=[self._check_reserve_valid])

        self._addon_data.reserveMB = dialog.run()

    def _check_reserve_valid(self, key, report_func):
        if self._reserve_check_re.match(key):
            if key == "auto":
                return True
            if key[-1] == 'M':
                key = key[:-1]
            key = int(key)
            if self._upper >= key >= self._lower:
                return True
        return False

    def input(self, args, key):
        if self._container.process_user_input(key):
            self.redraw()
            return InputState.PROCESSED
        else:
            return super().input(args, key)

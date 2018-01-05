# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Inspired from: https://github.com/redhat-openstack/khaleesi/blob/master/plugins/callbacks/human_log.py
# Further improved support Ansible 2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
  import simplejson as json
except ImportError:
  import json

from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):

  """
  Ansible callback plugin for result json output
  """
  CALLBACK_VERSION = 2.0
  CALLBACK_TYPE = 'notification'
  CALLBACK_NAME = 'write_out'
  CALLBACK_NEEDS_WHITELIST = False

  def __init__(self):

    super(CallbackModule, self).__init__()

    if not os.path.exists("/var/log/ansible/hosts"):
      os.makedirs("/var/log/ansible/hosts")

  def write_out(self, host, task, new_data):

    taskname = "%s" % task
    hostname = "%s" % host
    path = os.path.join("/var/log/ansible/hosts", "%s" % hostname)

    # Only the task of write_out is output
    if not taskname.startswith("TASK: write_out "):
      return

    if not os.path.exists(path):
      with open(path, "w"): pass

    with open(path, "r") as fd:
      try:
        save_data = json.load(fd)
      except:
        save_data = dict()

    if taskname not in save_data:
      save_data[taskname] = dict()

    save_data[taskname][hostname] = new_data

    with open(path, "w") as fd:
      fd.write(json.dumps(save_data, indent=2))

  def on_any(self, *args, **kwargs):
    pass

  def runner_on_failed(self, host, res, ignore_errors=False):
    pass

  def runner_on_ok(self, host, res):
    pass

  def runner_on_skipped(self, host, item=None):
    pass

  def runner_on_unreachable(self, host, res):
    pass

  def runner_on_no_hosts(self):
    pass

  def runner_on_async_poll(self, host, res, jid, clock):
    pass

  def runner_on_async_ok(self, host, res, jid):
    pass

  def runner_on_async_failed(self, host, res, jid):
    pass

  def playbook_on_start(self):
    pass

  def playbook_on_notify(self, host, handler):
    pass

  def playbook_on_no_hosts_matched(self):
    pass

  def playbook_on_no_hosts_remaining(self):
    pass

  def playbook_on_task_start(self, name, is_conditional):
    pass

  def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
    pass

  def playbook_on_setup(self):
    pass

  def playbook_on_import_for_host(self, host, imported_file):
    pass

  def playbook_on_not_import_for_host(self, host, missing_file):
    pass

  def playbook_on_play_start(self, name):
    pass

  def playbook_on_stats(self, stats):
    pass

  def on_file_diff(self, host, diff):
    pass


  ####### V2 METHODS ######
  def v2_on_any(self, *args, **kwargs):
    pass

  def v2_runner_on_failed(self, result, ignore_errors=False):
    self.write_out(result._host, result._task, result._result)

  def v2_runner_on_ok(self, result):
    self.write_out(result._host, result._task, result._result)

  def v2_runner_on_skipped(self, result):
    self.write_out(result._host, result._task, result._result)

  def v2_runner_on_unreachable(self, result):
    self.write_out(result._host, result._task, result._result)

  def v2_runner_on_no_hosts(self, task):
    pass

  def v2_runner_on_async_poll(self, result):
    self.write_out(result._host, result._task, result._result)

  def v2_runner_on_async_ok(self, host, result):
    self.write_out(result._host, result._task, result._result)

  def v2_runner_on_async_failed(self, result):
    self.write_out(result._host, result._task, result._result)

  def v2_playbook_on_start(self, playbook):
    pass

  def v2_playbook_on_notify(self, result, handler):
    pass

  def v2_playbook_on_no_hosts_matched(self):
    pass

  def v2_playbook_on_no_hosts_remaining(self):
    pass

  def v2_playbook_on_task_start(self, task, is_conditional):
    pass

  def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                   encrypt=None, confirm=False, salt_size=None,
                   salt=None, default=None):
    pass

  def v2_playbook_on_setup(self):
    pass

  def v2_playbook_on_import_for_host(self, result, imported_file):
    pass

  def v2_playbook_on_not_import_for_host(self, result, missing_file):
    pass

  def v2_playbook_on_play_start(self, play):
    pass

  def v2_playbook_on_stats(self, stats):
    pass

  def v2_on_file_diff(self, result):
    pass

  def v2_playbook_on_item_ok(self, result):
    pass

  def v2_playbook_on_item_failed(self, result):
    pass

  def v2_playbook_on_item_skipped(self, result):
    pass

  def v2_playbook_on_include(self, included_file):
    pass

  def v2_playbook_item_on_ok(self, result):
    pass

  def v2_playbook_item_on_failed(self, result):
    pass

  def v2_playbook_item_on_skipped(self, result):
    pass

''' Based on the existing Piding Plugin that comes bundled with kupfer '''
__kupfer_name__ = _("Pidgin Status")
__kupfer_actions__ = ("SetStatus",)
__description__ = _("Access to Pidgin Status")
__version__ = "0.1"
__author__ = ("Sascha Hinlang <sascha@hinlang.com>")

import dbus

from kupfer.objects import Leaf, Action, Source, TextLeaf, TextSource
from kupfer import pretty, scheduler
from kupfer import icons
from kupfer import plugin_support
from kupfer.weaklib import dbus_signal_connect_weakly

plugin_support.check_dbus_connection()

# D-Bus "addresses"
SERVICE_NAME = "im.pidgin.purple.PurpleService"
OBJECT_NAME = "/im/pidgin/purple/PurpleObject"
IFACE_NAME = "im.pidgin.purple.PurpleInterface"

# Pidgin status
STATUS_OFFLINE = 1
STATUS_AVAILABLE = 2
STATUS_UNAVAILABLE = 3
STATUS_INVISIBLE = 4
STATUS_AWAY = 5

def _create_dbus_connection(activate=False):
	interface = None
	obj = None
	sbus = dbus.SessionBus()

	try:
		#check for running pidgin (code from note.py)
		proxy_obj = sbus.get_object('org.freedesktop.DBus',
				'/org/freedesktop/DBus')
		dbus_iface = dbus.Interface(proxy_obj, 'org.freedesktop.DBus')
		if activate or dbus_iface.NameHasOwner(SERVICE_NAME):
			obj = sbus.get_object(SERVICE_NAME, OBJECT_NAME)
		if obj:
			interface = dbus.Interface(obj, IFACE_NAME)
	except dbus.exceptions.DBusException, err:
		pretty.print_debug(err)
	return interface


def _set_pidgin_status(text, present=False):

	interface = _create_dbus_connection()
	if not interface:
		return

	if text == "on":
		interface.PurpleSavedstatusActivate(interface.PurpleSavedstatusNew("", STATUS_AVAILABLE))
	elif text == "off":
		interface.PurpleSavedstatusActivate(interface.PurpleSavedstatusNew("", STATUS_OFFLINE))
	elif text == "away":
		interface.PurpleSavedstatusActivate(interface.PurpleSavedstatusNew("", STATUS_AWAY))
	elif text == "dnd":
		interface.PurpleSavedstatusActivate(interface.PurpleSavedstatusNew("", STATUS_UNAVAILABLE))
	elif text == "inv":
		interface.PurpleSavedstatusActivate(interface.PurpleSavedstatusNew("", STATUS_INVISIBLE))

class SetStatus(Action):
	""" Set status for Pidgin """

	def __init__(self):
		Action.__init__(self, _('Set Status'))

	def activate(self, leaf):
		_set_pidgin_status(leaf.object, present=True)
		
	def item_types(self):
		yield TextLeaf

	def get_description(self):
		return __description__

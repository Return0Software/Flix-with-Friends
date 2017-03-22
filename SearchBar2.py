import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

import random
import re
import datetime


class GenrePop(Gtk.Popover):
	"""Creates a popover to filter by genre"""

	__gsignals__ = {
		"genres-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self, db):
		Gtk.Popover.__init__(self)

		self.genres = []

		box = Gtk.ButtonBox(orientation = Gtk.Orientation.VERTICAL)
		for genre in db.listGenres:
			button = Gtk.ModelButton(text = genre, role = Gtk.ButtonRole.CHECK,
									centered = False)
			box.add(button)
			button.connect("clicked", self.genre_cb)
		self.add(box)

	def genre_cb(self, button):
		button.set_property("active", not button.get_property("active"))
		if button.get_property("active") is True:
			self.genres.append(button.get_property("text"))
		else:
			self.genres.remove(button.get_property("text"))
		self.emit("genres-updated", self.genres)


class RatingPop(Gtk.Popover):
	"""Creates a popover to filter by minimum rating"""

	__gsignals__ = {
		"rating-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self):
		Gtk.Popover.__init__(self)

		self.scale = Gtk.Scale(draw_value = True, has_origin = True,
								value_pos = 0).new_with_range(Gtk.Orientation.HORIZONTAL, 0, 10, 1)
		self.scale.connect("value-changed", self.scale_cb)

		i = 1
		while i <= 10:
			self.scale.add_mark(i, Gtk.PositionType.TOP)
			i += 1
		self.scale.set_size_request(150, 40)

		box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5, margin = 5)
		label = Gtk.Label(label = "Choose a\nminimum rating:", justify = Gtk.Justification.CENTER)

		box.add(ratingLabel)
		box.add(self.scale)

		self.add(box)

	def scale_cb(self, scale):
		self.emit("rating-updated", scale.get_value())


class DatePop(Gtk.Popover):
	"""Creates a popover to filter by release date"""

	__gsignals__ = {
		"switch-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)),
		"year-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self, db):
		Gtk.Popover.__init__(self)

		self.switch = Gtk.Switch(active = False, state = False)
		self.switch.connect("state-set", self.switch_cb)

		self.combo = Gtk.ComboBoxText(wrap_width = 4)
		self.combo.connect("changed", self.combo_cb)

		x = datetime.datetime.now().year
		while x >= db.oldest_year:
			self.combo.append_text(str(x))
			x -= 1
		self.dateCombo.set_active(datetime.datetime.now().year - self.db.oldest_year)

		label = Gtk.Label(label = "Search for movies produced\nonly in the year above",
						justify = Gtk.Justification.CENTER)
		switchBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
		switchBox.add(label)
		switchBox.add(self.switch)

		dateBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, margin = 5, spacing = 5)
		dateBox.add(self.combo)
		dateBox.add(switchBox)

		self.add(dateBox)

	def switch_cb(self, switch, state):
		self.emit("switch-updated", state)

	def combo_cb(self, combo):
		self.emit("year-updated", combo.get_active_text())

class ViewedByPop(Gtk.Popover):
	"""Creates a popover to filter by who has seen the movie"""

	__gsignals__ = {
		"friends-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self, db):
		Gtk.Popover.__init__(self)

		self.friends = []

		box = Gtk.ButtonBox(orientation = Gtk.Orientation.VERTICAL)
		for genre in db.friends:
			button = Gtk.ModelButton(text = genre, role = Gtk.ButtonRole.CHECK,
									centered = False)
			box.add(button)
			button.connect("clicked", self.friend_cb)
		self.add(box)

	def friend_cb(self, button):
		button.set_property("active", not button.get_property("active"))
		if button.get_property("active") is True:
			self.genres.append(button.get_property("text"))
		else:
			self.genres.remove(button.get_property("text"))
		self.emit("friends-updated", self.friends)


class SearchBar(Gtk.Revealer):
	"""Creates a search bar with an entry and filters"""

	__gsignals__ = {
		"search-ran": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self, db):
		Gtk.Revealer.__init__(self, transition_duration = 300)

		self.entry = None

		self.genres = []
		self.friends = []

		criteria = Gtk.Box(margin = 5)
		filters = Gtk.ButtonBox(layout_style = Gtk.ButtonBoxStyle.EXPAND)

		self.entry = Gtk.SearchEntry()
		self.entry.set_can_focus(True)
		self.entry.set_size_request(250, -1)
		self.entry.connect("activate", self.search_cb)
		self.entry.connect("change", self.search_cb)

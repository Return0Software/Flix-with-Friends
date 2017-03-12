import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Database import Database


class MovieDialog(Gtk.Dialog):

	def __init__(self, parent, action):
		"""Create a dialog for adding and deleting movies"""
		Gtk.Dialog.__init__(self, action + " a Movie", parent, Gtk.DialogFlags.MODAL, use_header_bar = True)

		self.db = Database(Database.location)

		self.type = action.lower()
		self.area = self.get_content_area()	 # area is a Gtk.Box
		self.area.get_style_context().add_class("linked")
		self.area.set_orientation(Gtk.Orientation.HORIZONTAL)

		self.entry = Gtk.Entry(text = "Enter the name of a movie to " + action.lower())
		self.entry.grab_focus()
		self.area.pack_start(self.entry, True, False, 0)

		self.enterButton = Gtk.Button(label = "Enter")
		self.enterButton.connect("clicked", self.enterButton_cb)
		self.area.pack_end(self.enterButton, True, False, 0)

		self.show_all()
		# if the action is deleting, create an autocompletion tree

	def enterButton_cb(self, enterButton):
		"""Reads the text entry and searches for a new movie to add"""
		if (self.type == 'add') and (self.entry.get_text() != 'Enter the name of a movie to add'):
			print('Movie to add:', self.entry.get_text())

			try:
				# self.db.newMovie(self.entry.get_text())
				# print(self.entry.get_text(), 'added as', self.db.movies[-1].title)
				search = self.db.tmdb_search(self.entry.get_text())
				print('Searh Results:\n')
				for movie in search:
					print('Title:', movie.title)
					print('Overview:', movie.overview)
					print()
			except:
				print('Error adding', self.entry.get_text())

		self.destroy()


class FriendDialog(Gtk.Dialog):

	def __init__(self, parent, action):
		Gtk.Dialog.__init__(self, action + " a Friend", parent, Gtk.DialogFlags.MODAL, use_header_bar = True)

		self.area = self.get_content_area()	 # area is a Gtk.Box
		box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		box.get_style_context().add_class("linked")

		self.entry = Gtk.Entry(text = "Enter the name of a friend to " + action.lower())
		self.entry.grab_focus()
		# self.entry.connect("activate", self.enterButton_cb, action)
		box.pack_start(self.entry, True, False, 0)

		# self.enterButton = Gtk.Button(label = "Enter")
		# self.enterButton.connect("clicked", self.enterButton_cb, action)
		# box.pack_end(self.enterButton, True, False, 0)

		self.area.pack_start(box, True, False, 0)

		self.show_all()
		# if the action is deleting, create an autocompletion tree

	# def enterButton_cb(self, enterButton, action):
	# 	if action is "Add":
	# 		addFriend(self.entry.get_text())
	# 	elif action is "Delete":
	# 		deleteFriend(self.entry.get_text())
	# 	self.destroy()

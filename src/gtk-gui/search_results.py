import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf, GLib, GObject

import os.path


INDEX_FIELD_DISPLAY = 0
INDEX_FIELD_NAME = 1
INDEX_FIELD_ICON = 2
INDEX_FIELD_ARROW = 3

class LoadingPage(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, Gtk.Orientation.VERTICAL)

		self.set_valign(Gtk.Align.CENTER)
		self.set_halign(Gtk.Align.CENTER)
		self.spinner = Gtk.Spinner()
		self.spinner.set_size_request(-1, 64)
		# self.spinner.start()
		# "Witty" loading page, loading search results
		lab = "Concentrating really hard" + u"…"
		self.label = Gtk.Label("<big>{}</big>".format(lab))
		self.label.set_use_markup(True)

		self.pack_start(self.spinner, True, True, 0)
		self.pack_start(self.label, False, False, 0)
		self.label.set_property("margin", 20)

class NotFoundPage(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, Gtk.Orientation.VERTICAL)

		self.set_valign(Gtk.Align.CENTER)
		self.set_halign(Gtk.Align.CENTER)
		# Unable to find any matching search results
		self.label = Gtk.Label("<big>{}</big>".format(
		                       "No results found"))
		self.label.set_use_markup(True)

		self.pack_start(self.label, False, False, 0)
		self.label.set_property("margin", 20)

class BlankPage(Gtk.Box):
	""" Simple placeholder page, nothing fancy. """

	label = None

	def __init__(self):
		Gtk.Box.__init__(self, Gtk.Orientation.VERTICAL)

		self.set_valign(Gtk.Align.CENTER)
		self.set_halign(Gtk.Align.CENTER)
		# Search page, prompt to begin searching
		self.label = Gtk.Label("<big>{}</big>".format(
								"Type a query to get started"))
		self.label.set_use_markup(True)

		self.pack_start(self.label, False, False, 0)
		self.label.set_property("margin", 20)

class SearchResults(Gtk.Box):

	__gsignals__ = {
		"row-activated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self): # , search_page):
		Gtk.Box.__init__(self, Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER)
		# self.search_page = search_page

		self.stack = Gtk.Stack(transition_type = Gtk.StackTransitionType.CROSSFADE)
		self.pack_start(self.stack, True, True, 0)

		self.empty_page = BlankPage()
		self.stack.add_named(self.empty_page, "empty")

		self.load_page = LoadingPage()
		self.stack.add_named(self.load_page, "loading")

		self.notfound_page = NotFoundPage()
		self.stack.add_named(self.notfound_page, "not-found")

		self.scroll = Gtk.ScrolledWindow(shadow_type = Gtk.ShadowType.ETCHED_IN, overlay_scrolling = False, kinetic_scrolling = True)
		self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.scroll.get_style_context().add_class("search-results")
		self.stack.add_named(self.scroll, "available")

		self.tview = Gtk.TreeView(activate_on_single_click = True, enable_grid_lines = False, headers_visible = False)
		self.tview.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
		self.tview.connect_after('row-activated', self.on_row_activated)
		self.scroll.add(self.tview)

		ren = Gtk.CellRendererPixbuf()
		# ren.set_property("stock-size", Gtk.IconSize.DIALOG)
		ren.set_padding(5, 2)
		column = Gtk.TreeViewColumn("Poster", ren, pixbuf = 2)
		self.tview.append_column(column)

		ren = Gtk.CellRendererText()
		ren.set_padding(5, 5)
		column = Gtk.TreeViewColumn("Movie", ren, markup = 0)
		self.tview.append_column(column)
		self.tview.set_search_column(1)

		ren = Gtk.CellRendererPixbuf()
		ren.set_padding(5, 5)
		column = Gtk.TreeViewColumn("Details", ren, icon_name = 3)
		self.tview.append_column(column)
		ren.set_property("xalign", 0.0)

		self.stack.set_visible_child_name("empty")

	def on_row_activated(self, tview, path, column):
		model = tview.get_model()
		row = model[path]

		movie_name = row[INDEX_FIELD_NAME]

		self.emit("row-activated", movie_name)

		# line 178 solus-sc/search-results...what's it do

	def set_search_view(self, results):
		model = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf, str)

		self.reset()

		for movie in results:
			desc = movie.overview
			if len(desc) > 125:
				#     i = 100
				#     j = 0
				#     z = 0
				#     while i < len(desc) and j < 2:
				#         if i % 100 is 0:
				#             if desc[i].isspace() is False:
				#                 z = 1
				#                 while i + z < len(desc) and desc[i + z].isspace() is False:
				#                     z = z + 1
				#             desc = desc[:i + z] + '\n' + desc[i + z:]
				#         i = i + 100
				#         j = j + 1
				desc = "%s..." % desc[0:125]

			desc = GLib.markup_escape_text(desc)
			text = "<b>%s</b>\n%s" % (movie.title.replace('&', '&amp;'), desc)

			poster = movie.poster + "w92.jpg"
			if os.path.isfile(poster) is True:
				image = GdkPixbuf.Pixbuf.new_from_file(poster)
			else:
				image = None

			model.append([text, movie.title, image, "go-next-symbolic"])

			while (Gtk.events_pending()):
				Gtk.main_iteration()

		if len(results) is 0:
			self.stack.set_visible_child_name("not-found")
		else:
			self.stack.set_visible_child_name("available")

		self.tview.set_model(model)
		self.load_page.spinner.stop()

	def reset(self):
		self.tview.set_model(None)
		self.stack.set_visible_child_name("loading")
		self.load_page.spinner.start()
		self.queue_draw()

	def clear_view(self):
		self.tview.set_model(None)
		self.stack.set_visible_child_name("empty")
		self.queue_draw()

import os
import sys
import tmdbsimple as tmdb
import urllib.request


class Movie:

	def __init__(self, dictionary):
		self.title = dictionary['Title']
		self.ID = dictionary['ID']
		self.viewers = dictionary['ViewedBy'].split(', ')
		self.runtime = dictionary['Runtime']
		self.genres = dictionary['Genres'].split(', ')
		self.release_date = dictionary['ReleaseDate']
		self.vote = str(dictionary['Vote'])
		self.overview = dictionary['Overview']
		self.poster_path = dictionary['Poster']
		self.actorNames = dictionary['ActorsName'].split(', ')
		self.actorChars = dictionary['ActorsChar'].split(', ')
		self.actorImg = dictionary['ActorsImg'].split(', ')
		self.directorName = dictionary['DirectorName']
		self.directorImg = dictionary['DirectorImg']
		self.trailer = dictionary['Trailer']
		self.backdrop = dictionary['Backdrop']

	def get_image(self):
		if (str(self.poster_path) != 'N/A') and str(self.poster_path) != 'None':
			# Create imagePosters directory if not present
			os.makedirs("./imagePosters", exist_ok = True)
			baseURL = 'https://image.tmdb.org/t/p/'
			posters = ['w92', 'w154', 'w185', 'w300_and_h450_bestv2', 'w342', 'w500', 'w780'] #'original']

			for p in posters:
				imagePage = baseURL + p + self.poster_path
				filename = self.title.replace(" ", "") + '_' + p + '.jpg'
				fullfilename = os.path.join('./imagePosters', filename)

				# if not already existent, download
				if not(os.path.isfile(fullfilename)):
					urllib.request.urlretrieve(imagePage, fullfilename)
					print(p, 'poster image:', imagePage)
			print('')

	def genres_string(self):
		return ', '.join(self.genres).rstrip(',')

	def bad_movie(self):
		bad_title = (self.title == 'N/A')# or (len(self.title) == 0)
		bad_ID = (self.ID == '1')# or len(self.ID) == 0)
		bad_runtime = (self.runtime == '1')# or (len(self.runtime) == 0)
		bad_overview = (self.overview == 'N/A')# or (len(self.overview) == 0)
		bad_poster = self.poster_path == 'N/A'

		return bad_ID or bad_overview or bad_runtime or bad_title or bad_poster

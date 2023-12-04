import csv

class MovieGraph:
    def __init__(self, csv_file):
        # hash maps to go between movie titles and IDs
        self.title_to_id = {}
        self.id_to_title = {}
        # stores the graph (only uses the ids not the titles)
        self.similar_movies = {}
        # read the csv file and populate the hash maps
        self._read_csv(csv_file)

    # builds similarity graph while also populating the title_to_id and id_to_title hash maps
    def _read_csv(self, csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    keyID = row[0]
                    self.title_to_id[row[1]] = keyID
                    self.id_to_title[keyID] = row[1]
                    self.similar_movies[keyID] = []
                    for i in range(2, len(row), 2):
                        movie_id = row[i]
                        if movie_id != '':
                            movie_title = row[i + 1]
                            self.title_to_id[movie_title] = movie_id
                            self.similar_movies[keyID].append((movie_id, i))
                            self.id_to_title[movie_id] = movie_title

    # getter methods for hash maps

    def get_title_to_id(self):
        return self.title_to_id

    def get_similar_movies(self):
        return self.similar_movies
    
    def get_id_to_title(self):
        return self.id_to_title


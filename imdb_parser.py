def main(url, filename):
  load_rating(url, filename)
  read_file(filename)
  df = pd.DataFrame(parse_data(filename)).transpose()
  df.columns = ['Название', 'Рейтинг IMDb', 'Число голосов']
  result = df[df['Рейтинг IMDb'] > df['Рейтинг IMDb'].quantile(0.7)]
  result = result[result['Число голосов'] < result['Число голосов'].quantile(0.15)].reset_index(drop=True)
  return result
  # формируем топ фильмов с высоким рейтингом и относительно низким числом оценок

def load_rating(url, filename):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42'
   }
  r = requests.get(url, headers = headers)
  with open(filename, 'w', encoding="utf-8") as output_file:
    output_file.write(r.text)
  # загружаем веб-страницу в html-файл

def read_file(filename):
  with open(filename, encoding='utf-8') as input_file:
    text = input_file.read()
  return text
  # читаем html-файл

def parse_data(filename):
  movie_title = []
  movie_rating = []
  movie_votes = []
  text = read_file(filename)
  soup = BeautifulSoup(text)
  film_list = soup.find('tbody', {'class': 'lister-list'})
  items = film_list.find_all('tr')
  for item in items:
    movie_number_votes = ''
    movie_title.append(item.find('td', {'class': 'titleColumn'}).find('a').text)
    movie_rating.append(float(item.find('td', {'class': 'ratingColumn'}).find('strong').text))
    votes = item.find('td', {'class': 'ratingColumn'}).find('strong').get('title')[13:]
    for i in range(len(votes)):
      if votes[i].isdigit():
        movie_number_votes += votes[i]
    movie_votes.append(int(movie_number_votes))
  return [movie_title, movie_rating, movie_votes]
  # извлекаем из файла данные о названиях, рейтинге и количестве оценок фильмов

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
filename = 'top.html'
main(url, filename)


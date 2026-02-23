class Movie {
  const Movie({required this.title, required this.url});

  final String title;
  final String url;
}

class Trilogy {
  const Trilogy({required this.title, required this.description, required this.url, required this.movies});

  final String title;
  final String description;
  final String url;
  final List<Movie> movies;
}
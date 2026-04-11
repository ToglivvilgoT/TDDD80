import 'package:logging/logging.dart';

class Movie {
  final String title;
  final String url;

  const Movie({required this.title, required this.url});

  factory Movie.fromJson(Map<String, dynamic> data) {
    try {
      return Movie(
        title: data['title'],
        url: data['url'],
      );
    }
    catch(error) {
      Logger.root.log(Level.WARNING, error);
      rethrow;
    }
  }
}

class Trilogy {
  final String title;
  final String description;
  final String url;
  final List<Movie> movies;

  const Trilogy({
    required this.title,
    required this.description,
    required this.url,
    required this.movies,
  });

  factory Trilogy.fromJson(Map<String, dynamic> data) {
    try {
      return Trilogy(
        title: data['title'],
        description: data['description'],
        url: data['url'],
        movies: (data['data'] as List)
          .cast<Map<String, dynamic>>()
          .map(Movie.fromJson)
          .toList(),
      );
    }
    catch(error) {
      Logger.root.log(Level.WARNING, error);
      rethrow;
    }
  }
}

import 'package:flutter/material.dart';
import 'package:logging/logging.dart';

class Movie {
  final String title;
  final ImageProvider? image;

  const Movie({required this.title, required this.image});

  factory Movie.fromJson(Map<String, dynamic> data) {
    try {
      return Movie(title: data['title'], image: NetworkImage(data['url']));
    } catch (error) {
      Logger.root.log(Level.WARNING, error);
      rethrow;
    }
  }
}

class Trilogy {
  final String title;
  final String description;
  final ImageProvider? image;
  final List<Movie> movies;

  const Trilogy({
    required this.title,
    required this.description,
    required this.image,
    required this.movies,
  });

  factory Trilogy.fromJson(Map<String, dynamic> data) {
    try {
      return Trilogy(
        title: data['title'],
        description: data['description'],
        image: NetworkImage(data['url']),
        movies:
            (data['data'] as List)
                .cast<Map<String, dynamic>>()
                .map(Movie.fromJson)
                .toList(),
      );
    } catch (error) {
      Logger.root.log(Level.WARNING, error);
      rethrow;
    }
  }
}

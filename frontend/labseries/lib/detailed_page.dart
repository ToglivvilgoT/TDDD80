import 'package:flutter/material.dart';
import 'package:labseries/structure.dart';

class DetailedPage extends StatelessWidget {
  const DetailedPage(this.trilogy, {super.key});

  final Trilogy trilogy;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(trilogy.title),
        backgroundColor: Colors.lime,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(10),
          child: Center(
            child: Column(
              spacing: 10,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                CircleAvatar(
                  backgroundImage: NetworkImage(trilogy.url),
                  minRadius: 25,
                  maxRadius: 100,
                ),
                Text(trilogy.description),
                MovieList(trilogy.movies),
              ],
            )
          ),
        ),
      )
    );
  }
}

class MovieList extends StatelessWidget {
  const MovieList(this.movies, {super.key});

  final List<Movie> movies;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 10,
      children: [
        for (var movie in movies) MovieCard(movie),
      ]
    );
  }
}

class MovieCard extends StatelessWidget {
  const MovieCard(this.movie, {super.key});

  final Movie movie;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(10),
        child: Column(
          spacing: 10,
          children: [
            CircleAvatar(
              backgroundImage: NetworkImage(movie.url),
              minRadius: 25,
              maxRadius: 50,
            ),
            Text(movie.title),
          ],
        ),
      ),
    );
  }
}


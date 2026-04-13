import 'package:flutter/material.dart';
import 'package:labseries/add_movie_page.dart';
import 'package:labseries/structure.dart';

class AddMoviesPage extends StatefulWidget {
  final String title;
  final String description;

  const AddMoviesPage({super.key, required this.title, required this.description});

  @override
  State<StatefulWidget> createState() => _AddMoviesPageState();
}

class _AddMoviesPageState extends State<AddMoviesPage> {
  final List<Movie> movies = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Creating: ${widget.title}"),),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: movies.length,
              itemBuilder: (context, index) => _MovieTile(movies[index]),
              shrinkWrap: true,
            ),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop<List<Movie>>(context, movies),
            child: Text("Done"),
          )
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          Movie? movie = await Navigator.push<Movie>(
            context, MaterialPageRoute<Movie>(
              builder: (context) => AddMoviePage(
                title: widget.title,
              )
            )
          );
          if (movie != null) {
            setState(() => movies.add(movie));
          }
        },
        child: Icon(Icons.add),
      ),      
    );
  }
}

class _MovieTile extends StatelessWidget {
  final Movie movie;

  const _MovieTile(this.movie);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(movie.title),
      leading: Image(image: NetworkImage(movie.url)),
    );
  }
}
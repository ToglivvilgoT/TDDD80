import 'package:flutter/material.dart';
import 'package:labseries/components/photo_picker.dart';
import 'package:labseries/structure.dart';

class AddMoviePage extends StatefulWidget {
  final String title;
  const AddMoviePage({super.key, required this.title});

  @override
  State<StatefulWidget> createState() => _AddMoviesPageState();
}

class _AddMoviesPageState extends State<AddMoviePage> {
  final _titleController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title)
      ),
      body: Form(
        key: _formKey,
        child: Column(
          children: [
            PhotoPicker(),
            TextFormField(
              controller: _titleController,
              decoration: const InputDecoration(
                hintText: "Movie title"
              ),
              validator: (value) => (value == null || value.isEmpty) ? "Please enter a title" : null,
            ),
            ElevatedButton(
              onPressed: () {
                if (_formKey.currentState!.validate()) {
                  Navigator.pop<Movie>(context, Movie(title: _titleController.text, url: "none :,("));
                }
              },
              child: Text("Add"),
            )
          ],
        ),
      ),
    );
  }
}
import 'package:flutter/material.dart';
import 'package:labseries/components/image_model.dart';
import 'package:labseries/components/photo_picker.dart';
import 'package:labseries/structure.dart';
import 'package:provider/provider.dart';

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
      body: ChangeNotifierProvider(
        create: (_) => ImageModel(),
        child: Form(
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
              Consumer<ImageModel>(
                builder: (context, imageModel, _) {
                  return ElevatedButton(
                    onPressed: () {
                      if (_formKey.currentState!.validate()) {
                        Navigator.pop<Movie>(context, Movie(title: _titleController.text, image: imageModel.getImage()));
                      }
                    },
                    child: Text("Add"),
                  );
                }
              )
            ],
          ),
        ),
      ),
    );
  }
}
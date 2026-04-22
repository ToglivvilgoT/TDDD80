import 'package:flutter/material.dart';
import 'package:labseries/add_movies_page.dart';
import 'package:labseries/components/image_model.dart';
import 'package:labseries/components/photo_picker.dart';
import 'package:labseries/structure.dart';
import 'package:provider/provider.dart';

class AddTrilogyPage extends StatefulWidget {
  const AddTrilogyPage({super.key});

  @override
  State<StatefulWidget> createState() {
    return _AddTrilogyPageState();
  }
}

class _AddTrilogyPageState extends State<AddTrilogyPage> {
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Create new trilogy"),
      ),
      body: ChangeNotifierProvider<ImageModel>(
        create: (_) => ImageModel(),
        child: Form(
          key: _formKey,
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              spacing: 8.0,
              children: [
                SizedBox(
                  width: 128,
                  height: 128,
                  child: PhotoPicker()
                ),
                TextFormField(
                  controller: _titleController,
                  decoration: InputDecoration(
                    hintText: "Trilogy title"
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter some text';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _descriptionController,
                  decoration: InputDecoration(
                    hintText: "Trilogy description"
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter some text';
                    }
                    return null;
                  },
                ),
                Consumer<ImageModel>(
                  builder: (context, imageModel, _) {
                    return ElevatedButton(
                      onPressed: () async {
                        if (_formKey.currentState!.validate()) {
                          var movies = await Navigator.push<List<Movie>>(
                            context, MaterialPageRoute<List<Movie>>(
                              builder: (context) => AddMoviesPage(
                                title: _titleController.text,
                                description: _descriptionController.text,
                              )
                            )
                          );
                          if (context.mounted) {
                            Trilogy? trilogy = movies == null ? null : Trilogy(
                              title: _titleController.text,
                              description: _descriptionController.text,
                              image: imageModel.getImage(),
                              movies: movies
                            );
                            Navigator.pop(context, trilogy);
                          }
                        }
                      },
                      child: Text("Next"),
                    );
                  }
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
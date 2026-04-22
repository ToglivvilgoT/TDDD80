import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:labseries/components/image_model.dart';
import 'package:provider/provider.dart';

class PhotoPicker extends StatelessWidget {
  const PhotoPicker({super.key});

  @override
  Widget build(BuildContext context) {
    ImageModel imageModel = Provider.of<ImageModel>(context);
    ImageProvider? image = imageModel.getImage();

    return GestureDetector(
      onTap: () => {
        ImagePicker()
        .pickImage(source: ImageSource.gallery)
        .then((imageFile) {
          if (imageFile == null) {
            return;
          }
          ImageProvider newImage = FileImage(File(imageFile.path));
          imageModel.setImage(newImage);
        })
      },
      child: CircleAvatar(
        backgroundImage: image,
        child: image == null ? Text("Add Image") : null,
      ),
    );
  }
}
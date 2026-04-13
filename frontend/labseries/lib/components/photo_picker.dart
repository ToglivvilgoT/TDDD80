import 'dart:io';

import 'package:flutter/material.dart';

class PhotoPicker extends StatefulWidget {
  const PhotoPicker({super.key});

  @override
  State<StatefulWidget> createState() {
    return _PhotoPickerState();
  }
}

class _PhotoPickerState extends State<PhotoPicker> {
  ImageProvider? image;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => image = FileImage(File("lib/components/image.png"))),
      child: CircleAvatar(
        backgroundImage: image,
        child: image == null ? Text("Add Image") : null,
      ),
    );
  }
}
import 'package:flutter/material.dart';

class ImageModel extends ChangeNotifier {
  ImageProvider? _image;

  void setImage(ImageProvider image) {
    _image = image;
    notifyListeners();
  }

  ImageProvider? getImage() => _image;
}
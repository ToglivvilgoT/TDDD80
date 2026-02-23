import 'package:labseries/structure.dart';

const Trilogy data = Trilogy(
  title: "The Lord of the Rings",
  description:
      "The Lord of the Rings trilogy is a cinematic masterpiece based on the novels by J.R.R. Tolkien. The trilogy follows the journey of Frodo Baggins and the Fellowship of the Ring as they strive to destroy the One Ring and ensure the downfall of its maker, the Dark Lord Sauron.",
  movies: [
    Movie(
      title: "The Fellowship of the Ring",
      url: "https://trilogy-server.azurewebsites.net/lord-of-the-rings/1",
    ),
    Movie(
      title: "The Two Towers",
      url: "https://trilogy-server.azurewebsites.net/lord-of-the-rings/2",
    ),
    Movie(
      title: "The Return of the King",
      url: "https://trilogy-server.azurewebsites.net/lord-of-the-rings/3",
    ),
  ],
  url: "https://trilogy-server.azurewebsites.net/lord-of-the-rings/1",
);

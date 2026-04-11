import 'package:flutter/material.dart';
import 'package:labseries/detailed_page.dart';
import 'package:labseries/structure.dart';

class ListPage extends StatelessWidget {
  const ListPage(this.trilogies, {super.key});

  final Future<List<Trilogy>> trilogies;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Trilogies")),
      bottomNavigationBar: BottomNavigationBar(items: [
        BottomNavigationBarItem(icon: Icon(Icons.place), label: "Hello"),
        BottomNavigationBarItem(icon: Icon(Icons.abc), label: "World"),
      ]),
      body: FutureBuilder(
        future: trilogies,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            var trilogies = snapshot.data!;
            return ListView.builder(
              itemCount: trilogies.length,
              itemBuilder: (context, index) => TrilogyTile(trilogies[index]),
            );
          }
          else if (snapshot.hasError) {
            return Text('An error occurred while fetching data: ${snapshot.error!}');
          }
          else {
            return LinearProgressIndicator();
          }
        }
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: (){},
        child: Icon(Icons.add),
      ),
    );
  }
}

class TrilogyTile extends StatelessWidget {
  const TrilogyTile(this.trilogy, {super.key});

  final Trilogy trilogy;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          minRadius: 10,
          maxRadius: 20,
          backgroundImage: NetworkImage(trilogy.url),
        ),
        title: Text(trilogy.title),
        onTap:
            () => Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => DetailedPage(trilogy)),
            ),
      ),
    );
  }
}

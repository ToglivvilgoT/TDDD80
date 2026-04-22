import 'package:flutter/material.dart';
import 'package:labseries/add_trilogy_page.dart';
import 'package:labseries/detailed_page.dart';
import 'package:labseries/structure.dart';

class ListPage extends StatefulWidget {
  final Future<List<Trilogy>> trilogies;

  const ListPage(this.trilogies, {super.key});

  @override
  State<ListPage> createState() => _ListPageState();
}

class _ListPageState extends State<ListPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Trilogies")),
      bottomNavigationBar: BottomNavigationBar(items: [
        BottomNavigationBarItem(icon: Icon(Icons.place), label: "Hello"),
        BottomNavigationBarItem(icon: Icon(Icons.abc), label: "World"),
      ]),
      body: FutureBuilder(
        future: widget.trilogies,
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
        onPressed: () async {
          Trilogy? trilogy = await Navigator.push<Trilogy>(
            context, MaterialPageRoute<Trilogy>(
              builder: (context) => const AddTrilogyPage()
            )
          );
          if (trilogy != null) {
            setState(() {
              widget.trilogies.then((trilogies) => trilogies.add(trilogy));
            });
          }
        },
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
          backgroundImage: trilogy.image,
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

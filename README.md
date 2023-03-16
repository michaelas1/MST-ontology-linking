### Project Description

Contains a REST-API for interactive editing of ontology graphs. The ontology ([video_games_set.owl](video_games_set.owl)) can be viewed and edited by adding triples, linking data from DBPedia as well as removing links. This project was created as part of the "Multimedia and Semantic Technologies" course at the University of Vienna in SS2022.

### How to run the application

The application requires python flask and can be run by executing "flask run" in the main directory and accessed at the displayed port at the endpoints listed below (e.g. http://127.0.0.1:5000/mst/mst:Bandai_Namco). The username is '*wZe5A^^m!!J6WjH' and the password 'A7Lny_vv5b^C?TJc' (both without the '). 

### Endpoints

`<host_name>/` - add a triple to the graph\
`<host_name>/mst` - list of individuals \
`<host_name>/mst/<prefix:name>` - detailed page of individual\
`<host_name>/rdf` - show in-memory graph in xml format \
`<host_name>/rdf/upload` - upload graph from file \
`<host_name>/rdf/download` - download in-memory graph to 'graph.ttl'

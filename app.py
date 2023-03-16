#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, Response, render_template, request, url_for
from flask_basicauth import BasicAuth
from rdflib import Graph, URIRef
from sparql_queries import Queries
import os

app = Flask(__name__)

# app configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['BASIC_AUTH_USERNAME'] = '*wZe5A^^m!!J6WjH'
app.config['BASIC_AUTH_PASSWORD'] = 'A7Lny_vv5b^C?TJc'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

# rdflib graph initialization
g = Graph().parse('video_games_set.owl')
g.namespace_manager.bind('mst',
                         URIRef('https://mis.cs.univie.ac.at/ontologies/2021SS/mst#'
                         ))


@app.route('/', methods=['GET'])
def index():
    """"Displays a form which allows users to insert triples into the ontology graph."""

    return render_template('add_triple.html')


@app.route('/triple', methods=['POST'])
def addTriple():
    """Post method to update the graph after a triple was inserted."""

    subject = request.form.get('subject')
    predicate = request.form.get('predicate')
    obj = request.form.get('object')
    try:
        g.update(Queries.PREFIX
                 + Queries.INSERT_TRIPLE.format(subject=subject,
                 predicate=predicate, obj=obj))
    except:
        return Response('There was an error in the input values.',
                        status=400, mimetype='text/html')
    return Response('The triple was added to the graph.', status=201,
                    mimetype='text/html')


@app.route('/mst', methods=['GET'])
def list_individuals():
    """Returns a list of all named individuals with hyperlinks to their pages."""

    result = g.query(Queries.PREFIX + Queries.GET_ALL_INDIVIDUALS)
    individuals = [request.url + '/'
                   + g.namespace_manager.normalizeUri(row.get('individual'
                   )) for row in result.bindings]
    return render_template('list_individuals.html', links=individuals)


@app.route('/mst/<string:name>', methods=['GET'])
def individual(name):
    """Returns information about a named individual including links to other resources, interlinked data and all predicates and
    objects the individual is linked to. In addition, allows users to search for related entries on DBPedia, add them under the
    rdfs:seeAlso relation and remove them again.
    """
    try:
        result = g.query(Queries.PREFIX
                     + Queries.GET_INDIVIDUAL_TUPLES.format(name=name))
    except:
        return Response(status=404)
                     
    tuples = [(g.namespace_manager.normalizeUri(row.get('predicate')),
              g.namespace_manager.normalizeUri(row.get('object')))
              for row in result.bindings]

    result = g.query(Queries.PREFIX
                     + Queries.GET_INDIVIDUAL_SEE_ALSO.format(name=name))
    see_also_links = [row.get('seeAlso') for row in result.bindings]

    result = g.query(Queries.PREFIX
                     + Queries.GET_INTERLINKED_INDIVIDUALS.format(name=name))
    interlinked = [(g.namespace_manager.normalizeUri(row.get('predicate'
                   )), request.url + '/'
                   + g.namespace_manager.normalizeUri(row.get('individual'
                   ))) for row in result.bindings]

    return render_template('individual.html', name=name, tuples=tuples,
                           see_also_links=see_also_links,
                           interlinked=interlinked)


@app.route('/seeAlso/add', methods=['POST'])
def addSeeAlso():
    """Adds a related resource to an existing individual."""

    subject = request.form.get('subject')
    obj = request.form.get('obj')
    g.update(Queries.PREFIX
             + Queries.INSERT_SEE_ALSO.format(subject=subject, obj=obj))
    return obj


@app.route('/seeAlso/remove', methods=['POST'])
def removeSeeAlso():
    """Removes a related resource from an individual."""

    subject = request.form.get('subject')
    obj = request.form.get('obj')
    g.update(Queries.PREFIX
             + Queries.DELETE_SEE_ALSO.format(subject=subject, obj=obj))
    return obj


@app.route('/rdf', methods=['GET'])
def showRDF():
    """Displays the graph contents in xml format."""

    xml = g.serialize(format='xml')
    return Response(xml, status=200, mimetype='text/xml')


@app.route('/rdf/download', methods=['GET'])
def downloadRDF():
    """Downloads the graph to a turtle file."""

    g.serialize(destination='graph.ttl', format='xml')
    return Response("The graph was downloaded as 'graph.ttl'.",
                    status=200, mimetype='text/html')


@app.route('/rdf/upload', methods=['GET', 'POST'])
def uploadRDF():
    """Uploads a file and adds its contents to the graph."""

    if request.method == 'GET':
        return render_template('upload_rdf.html')
    else:

        if 'rdf_file' not in request.files:
            return redirect(request.url)
            
        file = request.files['rdf_file']

        if file.filename == '':
            return redirect(request.url)
            
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                  filename))
        try:
            g.parse(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except:
            return Response('The file could not be parsed and added to the graph.',
                            status=400, mimetype='text/html')
        return Response('The file "' + filename + '" was added to the graph.', status=200,
                        mimetype='text/html')

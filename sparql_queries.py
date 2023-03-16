class Queries:

    PREFIX = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
    """

    GET_ALL_INDIVIDUALS = """
    SELECT DISTINCT ?individual
        WHERE {  ?individual rdf:type owl:NamedIndividual }
    """

    GET_INDIVIDUAL_TUPLES = """
    SELECT DISTINCT ?predicate ?object
        WHERE {{
            {name} rdf:type owl:NamedIndividual .
            {name} ?predicate ?object
            }}
    """

    GET_INDIVIDUAL_SEE_ALSO = """
    SELECT DISTINCT ?seeAlso
        WHERE {{
            {name} rdf:type owl:NamedIndividual .
            {name} rdfs:seeAlso ?seeAlso
            }}
    """

    GET_INTERLINKED_INDIVIDUALS = """
    SELECT DISTINCT ?predicate ?individual
        WHERE {{
            {name} rdf:type owl:NamedIndividual .
            ?individual rdf:type owl:NamedIndividual .
            {name} ?predicate ?individual
            }}
    """

    INSERT_TRIPLE = """
    INSERT DATA{{ {subject} {predicate} {obj} }}
    """

    INSERT_SEE_ALSO = """
    INSERT DATA {{ {subject} rdfs:seeAlso '{obj}' }}
    """

    DELETE_SEE_ALSO = """
    DELETE DATA {{ {subject} rdfs:seeAlso '{obj}' }}
    """

from rdflib import Graph, Namespace

ONTOLOGY_PATH = "ontology.ttl"

def load_ontology():
    g = Graph()
    ns = Namespace("http://example.org/fractions#")

    try:
        g.parse(ONTOLOGY_PATH, format="turtle")
        print("Ontology loaded.")
        return g, ns
    except Exception as e:
        print("Ontology failed to load:", e)
        return None, None

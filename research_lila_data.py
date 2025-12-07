import requests
import sys

def query_lila(word):
    endpoint = "https://lila-erc.eu/sparql/lila_knowledge_base/sparql"
    
    # Query to see ALL properties available for a Lemma
    sparql_query = f"""
    PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?p ?o WHERE {{
      ?lemma a lila:Lemma ;
             rdfs:label ?label ;
             ?p ?o .
      FILTER(regex(str(?label), "^rosa$", "i"))
    }}
    LIMIT 20
    """
    
    try:
        response = requests.get(endpoint, params={'query': sparql_query, 'format': 'json'})
        response.raise_for_status()
        data = response.json()
        
        print(f"--- Results for '{word}' ---")
        results = data.get('results', {}).get('bindings', [])
        
        if not results:
            print(f"No results found for {word}.")
            return

        print(f"--- Properties for '{word}' ---")
        for r in results:
            p = r.get('p', {}).get('value', 'N/A')
            o = r.get('o', {}).get('value', 'N/A')
            print(f"  {p.split('/')[-1]}: {o}")
            
    except Exception as e:
        print(f"Error querying LiLa: {e}")

if __name__ == "__main__":
    query_lila("rosa")

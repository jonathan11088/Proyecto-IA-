import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

# se cargan las variables de entorno desde .env
load_dotenv()

def cargar_grafo():
    csv_path = os.path.join("data", "archivo2_grafo.csv")
    
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    
    #este lee el cvs y lo convuerte en un dataframe 
    df = pd.read_csv(csv_path)
    
    #Conectarse a Neo4j Aura utilizando las credenciales del archivo .env
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    with driver.session() as session:
        #Limpie la base de datos para evitar dupliacados 
        session.run("MATCH (n) DETACH DELETE n")
        
        #aca se inyectan los nodos y relaciones en Neo4j 
        for _, row in df.iterrows():
            origen = row['entidad_origen'].strip()
            relacion = row['relacion'].strip().upper() 
            destino = row['entidad_destino'].strip()
            
            # Consulto a cypher para evitar nodos duplicaods 
            cypher_query = f"""
            MERGE (a:Entidad {{nombre: $origen}})
            MERGE (b:Entidad {{nombre: $destino}})
            MERGE (a)-[r:{relacion}]->(b)
            """
            session.run(cypher_query, origen=origen, destino=destino)
            
    driver.close()
    

if __name__ == "__main__":
    if not all([os.getenv("NEO4J_URI"), os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")]):
        print("POr favor ingresar credenciales ")
    else:
        cargar_grafo()
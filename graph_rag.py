import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Cargar variables de entorno (.env)
load_dotenv()

def cargar_grafo():
    csv_path = os.path.join("data", "archivo2_grafo.csv")
    
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    
    print("📊 Leyendo archivo2_grafo.csv...")
    df = pd.read_csv(csv_path)
    
    print("🌐 Conectando con la instancia de Neo4j Aura...")
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    with driver.session() as session:
        # Opcional: Limpiar la base de datos antes de cargar para evitar duplicados en pruebas
        print("🧹 Limpiando datos previos en el Grafo...")
        session.run("MATCH (n) DETACH DELETE n")
        
        print("🚀 Inyectando nodos y relaciones en Neo4j...")
        for _, row in df.iterrows():
            origen = row['entidad_origen'].strip()
            relacion = row['relacion'].strip().upper() # Buenas prácticas: relaciones en mayúsculas
            destino = row['entidad_destino'].strip()
            
            # Consulta Cypher dinámica utilizando MERGE para evitar nodos repetidos
            cypher_query = f"""
            MERGE (a:Entidad {{nombre: $origen}})
            MERGE (b:Entidad {{nombre: $destino}})
            MERGE (a)-[r:{relacion}]->(b)
            """
            session.run(cypher_query, origen=origen, destino=destino)
            
    driver.close()
    print("✅ ¡Graph RAG completado con éxito! Relaciones cargadas en Neo4j Aura.")

if __name__ == "__main__":
    if not all([os.getenv("NEO4J_URI"), os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")]):
        print("❌ Error: Faltan credenciales de Neo4j en el archivo .env")
    else:
        cargar_grafo()
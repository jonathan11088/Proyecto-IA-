import os
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Cargar variables de entorno (por si las usas más adelante)
load_dotenv()

def cargar_vector_db():
    json_path = os.path.join("data", "archivo1_documentos.json")
    persist_directory = "chroma_db"
    
    if not os.path.exists(json_path):
        print(f"❌ Error: No se encontró el archivo en {json_path}")
        return

    print("📖 Leyendo archivo1_documentos.json...")
    with open(json_path, "r", encoding="utf-8") as f:
        documentos_json = json.load(f)
    
    docs = []
    for doc in documentos_json:
        # Combinamos la información para optimizar la búsqueda semántica posterior
        texto_completo = f"Título: {doc['titulo']}\nCategoría: {doc['categoria']}\nContenido: {doc['contenido']}\nPalabras Clave: {', '.join(doc['palabras_clave'])}"
        
        metadata = {
            "id": doc["id"],
            "categoria": doc["categoria"],
            "titulo": doc["titulo"]
        }
        docs.append(Document(page_content=texto_completo, metadata=metadata))
    
    print("🧠 Inicializando HuggingFace Embeddings locales (all-MiniLM-L6-v2)...")
    # Este modelo se descargará automáticamente la primera vez y correrá gratis en tu PC
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("💾 Guardando documentos en la Base de Datos Vectorial (ChromaDB)...")
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"✅ ¡RAG Tradicional completado con éxito! Carpeta '{persist_directory}' creada localmente.")

if __name__ == "__main__":
    cargar_vector_db()
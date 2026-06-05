import chromadb

client = chromadb.PersistentClient(
    path="./my_chromadb"
)

collection = client.get_or_create_collection(
    name="research_papers"
)


def retrieve_documents(query, n_results=20):

    result = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return result
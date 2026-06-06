import chromadb #Vector database.

client = chromadb.PersistentClient(
    path="./my_chromadb" 
)

collection = client.get_or_create_collection(
    name="research_papers"
)#Loading of database get_or_create_collection is used instead of get_collection as I got the error when I tried to deploy it in the browser
#It would work for get_collection in our case.


def retrieve_documents(query, n_results=20):#retrieval of chunks from chroma db from the query with suitable semantic meaning

    result = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return result
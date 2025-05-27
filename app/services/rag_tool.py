from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from app.config import settings
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools import Tool
from app.services.process_docs import process_documents
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
import uuid
from langchain_core.tools import tool
import os



# Setup LangChain Agent
memory = MemorySaver()
model = ChatGoogleGenerativeAI(
    model=settings.GOOGLE_MODEL, 
    temperature=settings.TEMPERATURE, 
    streaming=settings.STREAMING
)
# search = DuckDuckGoSearchRun(max_results=2)
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
vectorstore = Chroma(
    collection_name="main_collection", persist_directory="shared_chroma_db", embedding_function=embeddings)

doUpdateChromaDB = False
        

async def create_retrieval_tool():
    vector_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )
    chunks = await process_documents("shared_docs")
    if doUpdateChromaDB:
        vectorstore.reset_collection()
        ids = [str(uuid.uuid4()) for _ in chunks]
        print(f"Adding {len(chunks)} documents to the vectorstore.")
        vectorstore.add_documents(documents=chunks, ids=ids)

    keyword_retriever = BM25Retriever.from_documents(chunks)
    keyword_retriever.k =  1

    retriever = EnsembleRetriever(
        retrievers=[vector_retriever, keyword_retriever],
        weights=[1.0, 0],
    )

    retriever = vector_retriever

    # 2. Create a Retrieval Tool
    def vectorstore_retrieval(query: str) -> str:
        # print(f"Query: {query}")
        """Retrieves relevant documents from the vectorstore based on the query."""

        results = retriever.invoke(query)
        print(query)
        # print(f"Results: {results}")
        # print(results)
        # Format the results (e.g., concatenate the document contents)
        if not results:
            return "No relevant documents found."
        contents = results[0].metadata["source"] + ("="*10) + "\n"
        contents += f"is the most relevant. Found total {len(results)} relevant document chunks.\n"
        contents += "\n".join([( ("="*10) + "\n" + doc.metadata["source"] + "\n" + ("="*10) + "\n" +
            doc.page_content) for doc in results])
        
        print(f"Contents: {contents}")
        return contents

    @tool
    def rag_retriever(location: str, season: str, year: str) -> str:
        """Retrieves information from user documents based on semantic search (RAG).

        Args:
            district (str): The district OR province to search for.
            season (str): The season to search for.
            year (str): The year to search for.

        Returns:
            str: The retrieved information.
        """
        try:

            #first check if season_year_location is in filespath
            #lowercase checks
            if str.lower(season) == "winter":
                season = "Jan-Apr"
            elif str.lower(season) == "summer":
                season = "Jun-Dec"
            
            filepath = "shared_docs/" + f"{season}_{year}_{location}.json"
            filename = f"{season}_{year}_{location}.json"
            print(f"Filepath: {filepath}")
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    data = f.read()
                print(f"Found: {filepath}")
                content = filename + ("="*10) + "\n"
                content += f"Land and Crop data for {location} for {season} {year}:\n"
                content += data
                return content

            return vectorstore_retrieval(f"Land and Crop data for {location} for {season} {year}")
            # return vectorstore_retrieval(f"{season}_{year}_{location}")
        except Exception as e:
            return f"An error occurred during retrieval of documents"

    # use better tool description here
    # DONE TO SOME EXTENT try a more smarter approach which is that in your tool doc-string you can prompt to enhance the input query according to extension format and tell the LLM how to provide input to that function.
    # retrieval_tool = Tool(
    #     name="vectorstore_retrieval",
    #     func=vectorstore_retrieval,
    #     description="""Useful for answering questions about information stored in the vectorstore.
    #     Input should be a fully formed query and include all relevant keyworkds to make the search more accurate.
    #     You may need to expand or pick from the User's message smartly.""",
    # )

    # return retrieval_tool
    return rag_retriever
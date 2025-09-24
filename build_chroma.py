# build_chroma.py

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# 1. Atomcamp URLs
urls = [
    # Main pages
    "https://www.atomcamp.com/",
    "https://www.atomcamp.com/about-us/",
    "https://www.atomcamp.com/ai-courses",
    "https://www.atomcamp.com/course/",

    # Bootcamps
    "https://www.atomcamp.com/dsbootcamp-2/",
    "https://www.atomcamp.com/data-analytics-bootcamp/",
    "https://www.atomcamp.com/make-your-ai-agent/",
    "https://www.atomcamp.com/summer-coding-camp/",

    # Short courses
    "https://www.atomcamp.com/courses/python-for-beginners/",
    "https://www.atomcamp.com/courses/introduction-to-data-analysis-with-excel/",
    "https://www.atomcamp.com/courses/diversity-and-inclusion/",
    "https://www.atomcamp.com/courses/linkedin/",

    # Webinars
    "https://www.atomcamp.com/webinars/"
]

# 2. Load data
print("📥 Loading webpages...")
loader = WebBaseLoader(urls)
docs = loader.load()

# 3. Split into chunks
print("✂️ Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

# 4. Generate embeddings
print("🔎 Generating embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 5. Save to Chroma
print("💾 Saving to Chroma DB...")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="chroma_db"
)
vectorstore.persist()

print("✅ Chroma DB has been built successfully!")

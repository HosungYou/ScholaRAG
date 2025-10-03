"""
Simple test script to verify the system is working
Run this after setup to ensure everything is configured correctly
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("ResearcherRAG System Test")
print("="*60)
print()

# Test 1: Import modules
print("Test 1: Checking imports...")
try:
    from backend.core.config import settings
    from backend.core.ingestion import DocumentIngestionPipeline
    from backend.core.retrieval import AdvancedRetriever
    from backend.core.rag_graph import query_literature_review
    print("✓ All modules imported successfully")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("\nPlease run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Test 2: Check configuration
print("Test 2: Checking configuration...")
try:
    # Check directories
    assert Path(settings.raw_pdfs_path).exists(), "raw_pdfs directory missing"
    assert Path(settings.processed_data_path).exists(), "processed directory missing"
    assert Path(settings.chroma_db_path).exists(), "vector_db directory missing"
    print("✓ All directories exist")

    # Check API key
    if not settings.anthropic_api_key and not settings.openai_api_key:
        print("⚠️  Warning: No API key found in .env file")
        print("   Add ANTHROPIC_API_KEY to .env to enable full functionality")
    else:
        print("✓ API key configured")

except AssertionError as e:
    print(f"✗ Configuration check failed: {e}")
    print("\nPlease run: ./setup.sh")
    sys.exit(1)

print()

# Test 3: Test embeddings
print("Test 3: Testing embeddings model...")
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Test embedding
    test_text = "This is a test sentence."
    embedding = embeddings.embed_query(test_text)

    assert len(embedding) > 0, "Embedding is empty"
    print(f"✓ Embeddings working (dimension: {len(embedding)})")

except Exception as e:
    print(f"✗ Embeddings test failed: {e}")
    sys.exit(1)

print()

# Test 4: Test vector store
print("Test 4: Testing vector store...")
try:
    from backend.core.retrieval import get_retriever

    retriever = get_retriever()
    stats = retriever.get_collection_stats()

    print(f"✓ Vector store initialized")
    print(f"  Current document count: {stats.get('count', 0)}")

except Exception as e:
    print(f"✗ Vector store test failed: {e}")
    sys.exit(1)

print()

# Test 5: Test LLM (if API key available)
print("Test 5: Testing LLM connection...")
if settings.anthropic_api_key or settings.openai_api_key:
    try:
        from backend.core.rag_graph import get_llm

        llm = get_llm()
        response = llm.invoke("Say 'test successful' and nothing else.")

        print(f"✓ LLM connection working")
        print(f"  Response: {response.content[:50]}...")

    except Exception as e:
        print(f"✗ LLM test failed: {e}")
        print("  Check your API key in .env file")
else:
    print("⊘ Skipped (no API key configured)")

print()
print("="*60)
print("System Test Complete!")
print("="*60)
print()

if stats.get('count', 0) == 0:
    print("📝 Next steps:")
    print("1. Run: python app.py")
    print("2. Open: http://localhost:7860")
    print("3. Upload some PDF papers")
    print("4. Start asking questions!")
else:
    print(f"✓ You have {stats.get('count')} documents ready to query!")
    print()
    print("Run: python app.py")
    print("Open: http://localhost:7860")

print()

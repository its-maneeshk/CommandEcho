"""
Memory System for CommandEcho
Handles short-term and long-term memory with vector embeddings
"""

import logging
import sqlite3
import json
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

# Check for sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  sentence-transformers not installed. Install with: pip install sentence-transformers")

# Check for FAISS
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  faiss-cpu not installed. Install with: pip install faiss-cpu")

class MemorySystem:
    """Handles both short-term and long-term memory"""
    
    def __init__(self, memory_config):
        self.config = memory_config
        self.logger = logging.getLogger(__name__)
        
        # Create memory directories
        Path(self.config.memory_db_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.config.vector_db_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize databases
        self._init_sqlite_db()
        
        # Initialize embedding model
        self.embedding_model = None
        self.vector_index = None
        
        if EMBEDDINGS_AVAILABLE:
            self._init_embedding_model()
        
        # Short-term memory (conversation within session)
        self.short_term_memory: List[Dict[str, Any]] = []
        
        self.logger.info("Memory system initialized")
    
    def _init_sqlite_db(self):
        """Initialize SQLite database for structured memory"""
        self.conn = sqlite3.connect(self.config.memory_db_path, check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def _init_embedding_model(self):
        """Initialize sentence transformer model for embeddings"""
        try:
            self.logger.info("Loading embedding model...")
            self.embedding_model = SentenceTransformer(self.config.embedding_model)
            
            # Initialize or load FAISS index
            if FAISS_AVAILABLE:
                self._init_vector_index()
            
            self.logger.info("Embedding model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load embedding model: {e}")
            self.embedding_model = None
    
    def _init_vector_index(self):
        """Initialize FAISS vector index"""
        index_path = Path(self.config.vector_db_path) / "memory_index.faiss"
        metadata_path = Path(self.config.vector_db_path) / "memory_metadata.pkl"
        
        if index_path.exists() and metadata_path.exists():
            # Load existing index
            try:
                self.vector_index = faiss.read_index(str(index_path))
                with open(metadata_path, 'rb') as f:
                    self.vector_metadata = pickle.load(f)
                self.logger.info("Loaded existing vector index")
            except Exception as e:
                self.logger.error(f"Error loading vector index: {e}")
                self._create_new_vector_index()
        else:
            self._create_new_vector_index()
    
    def _create_new_vector_index(self):
        """Create new FAISS vector index"""
        # Get embedding dimension
        sample_embedding = self.embedding_model.encode(["test"])
        dimension = sample_embedding.shape[1]
        
        # Create FAISS index
        self.vector_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.vector_metadata = []
        
        self.logger.info(f"Created new vector index with dimension {dimension}")
    
    def add_to_conversation(self, role: str, content: str):
        """Add message to conversation history"""
        # Add to short-term memory
        self.short_term_memory.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })
        
        # Keep only recent messages in short-term memory
        if len(self.short_term_memory) > self.config.max_short_term_memory:
            self.short_term_memory.pop(0)
        
        # Store in database
        self.conn.execute(
            "INSERT INTO conversations (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()
    
    def get_recent_conversation(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        cursor = self.conn.execute(
            "SELECT role, content, timestamp FROM conversations ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'role': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        return list(reversed(conversations))  # Return in chronological order
    
    def store_memory(self, content: str, memory_type: str = 'general', metadata: Dict = None):
        """Store a memory with optional vector embedding"""
        # Store in SQLite
        metadata_json = json.dumps(metadata) if metadata else None
        cursor = self.conn.execute(
            "INSERT INTO memories (content, memory_type, metadata) VALUES (?, ?, ?)",
            (content, memory_type, metadata_json)
        )
        memory_id = cursor.lastrowid
        self.conn.commit()
        
        # Store vector embedding if available
        if self.embedding_model and self.vector_index is not None:
            try:
                embedding = self.embedding_model.encode([content])
                # Normalize for cosine similarity
                faiss.normalize_L2(embedding)
                
                self.vector_index.add(embedding)
                self.vector_metadata.append({
                    'id': memory_id,
                    'content': content,
                    'memory_type': memory_type,
                    'metadata': metadata
                })
                
                # Save updated index
                self._save_vector_index()
                
            except Exception as e:
                self.logger.error(f"Error storing vector embedding: {e}")
    
    def search_memories(self, query: str, limit: int = 5) -> List[str]:
        """Search memories using vector similarity"""
        if not self.embedding_model or self.vector_index is None:
            # Fallback to text search
            return self._text_search_memories(query, limit)
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search vector index
            scores, indices = self.vector_index.search(query_embedding, limit)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1 and scores[0][i] > 0.3:  # Similarity threshold
                    results.append(self.vector_metadata[idx]['content'])
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in vector search: {e}")
            return self._text_search_memories(query, limit)
    
    def _text_search_memories(self, query: str, limit: int) -> List[str]:
        """Fallback text-based memory search"""
        cursor = self.conn.execute(
            "SELECT content FROM memories WHERE content LIKE ? ORDER BY timestamp DESC LIMIT ?",
            (f"%{query}%", limit)
        )
        
        return [row[0] for row in cursor.fetchall()]
    
    def store_user_preference(self, key: str, value: str):
        """Store user preference"""
        self.conn.execute(
            "INSERT OR REPLACE INTO user_preferences (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()
        
        # Also store as memory for context
        self.store_memory(f"User preference: {key} = {value}", "user_preference")
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        cursor = self.conn.execute(
            "SELECT value FROM user_preferences WHERE key = ?",
            (key,)
        )
        
        result = cursor.fetchone()
        return result[0] if result else default
    
    def _save_vector_index(self):
        """Save FAISS vector index to disk"""
        if self.vector_index is None:
            return
        
        try:
            index_path = Path(self.config.vector_db_path) / "memory_index.faiss"
            metadata_path = Path(self.config.vector_db_path) / "memory_metadata.pkl"
            
            faiss.write_index(self.vector_index, str(index_path))
            
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.vector_metadata, f)
                
        except Exception as e:
            self.logger.error(f"Error saving vector index: {e}")
    
    def cleanup_old_conversations(self, days: int = 30):
        """Clean up old conversation history"""
        cutoff_date = datetime.now() - timedelta(days=days)
        self.conn.execute(
            "DELETE FROM conversations WHERE timestamp < ?",
            (cutoff_date,)
        )
        self.conn.commit()
        self.logger.info(f"Cleaned up conversations older than {days} days")
    
    def get_memory_stats(self) -> Dict[str, int]:
        """Get memory system statistics"""
        stats = {}
        
        # Count memories
        cursor = self.conn.execute("SELECT COUNT(*) FROM memories")
        stats['total_memories'] = cursor.fetchone()[0]
        
        # Count conversations
        cursor = self.conn.execute("SELECT COUNT(*) FROM conversations")
        stats['total_conversations'] = cursor.fetchone()[0]
        
        # Count user preferences
        cursor = self.conn.execute("SELECT COUNT(*) FROM user_preferences")
        stats['user_preferences'] = cursor.fetchone()[0]
        
        # Vector index size
        if self.vector_index:
            stats['vector_memories'] = self.vector_index.ntotal
        else:
            stats['vector_memories'] = 0
        
        return stats

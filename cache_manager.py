import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List


class CacheManager:
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.db_path = self.cache_dir / "papers.db"
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                arxiv_id TEXT PRIMARY KEY,
                title TEXT,
                authors TEXT,
                summary TEXT,
                published TEXT,
                updated TEXT,
                cached_at TEXT,
                source_path TEXT,
                main_tex_file TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_paper_metadata(self, arxiv_id: str, metadata: Dict, source_path: Path, main_tex_file: Optional[Path] = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO papers 
            (arxiv_id, title, authors, summary, published, updated, cached_at, source_path, main_tex_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            arxiv_id,
            metadata.get('title', ''),
            json.dumps(metadata.get('authors', [])),
            metadata.get('summary', ''),
            metadata.get('published', ''),
            metadata.get('updated', ''),
            datetime.now().isoformat(),
            str(source_path),
            str(main_tex_file) if main_tex_file else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_paper_metadata(self, arxiv_id: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM papers WHERE arxiv_id = ?', (arxiv_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'arxiv_id': row[0],
            'title': row[1],
            'authors': json.loads(row[2]) if row[2] else [],
            'summary': row[3],
            'published': row[4],
            'updated': row[5],
            'cached_at': row[6],
            'source_path': Path(row[7]),
            'main_tex_file': Path(row[8]) if row[8] else None
        }
    
    def is_paper_cached(self, arxiv_id: str) -> bool:
        cached_data = self.get_paper_metadata(arxiv_id)
        if not cached_data:
            return False
        
        source_path = cached_data['source_path']
        return source_path.exists()
    
    def list_cached_papers(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT arxiv_id, title, authors, cached_at FROM papers ORDER BY cached_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        papers = []
        for row in rows:
            papers.append({
                'arxiv_id': row[0],
                'title': row[1],
                'authors': json.loads(row[2]) if row[2] else [],
                'cached_at': row[3]
            })
        
        return papers
    
    def clear_cache(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM papers')
        conn.commit()
        conn.close()
        
        import shutil
        for item in self.cache_dir.iterdir():
            if item.is_dir() and item.name != 'papers.db':
                shutil.rmtree(item)
    
    def get_cache_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM papers')
        paper_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(LENGTH(summary) + LENGTH(title)) FROM papers')
        total_text_size = cursor.fetchone()[0] or 0
        
        conn.close()
        
        total_disk_size = sum(f.stat().st_size for f in self.cache_dir.rglob('*') if f.is_file())
        
        return {
            'cached_papers': paper_count,
            'total_text_size': total_text_size,
            'total_disk_size': total_disk_size,
            'cache_directory': str(self.cache_dir)
        }
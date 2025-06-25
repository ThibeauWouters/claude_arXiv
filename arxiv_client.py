import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import os
import tarfile
import zipfile
from pathlib import Path


class ArxivClient:
    BASE_URL = "http://export.arxiv.org/api/query"
    EXPORT_URL = "https://arxiv.org/e-print"
    
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_paper_metadata(self, arxiv_id: str) -> Dict:
        clean_id = self._clean_arxiv_id(arxiv_id)
        url = f"{self.BASE_URL}?id_list={clean_id}"
        
        try:
            with urllib.request.urlopen(url) as response:
                xml_data = response.read().decode('utf-8')
                return self._parse_metadata_xml(xml_data)
        except Exception as e:
            raise Exception(f"Failed to fetch metadata for {arxiv_id}: {str(e)}")
    
    def download_source(self, arxiv_id: str) -> Path:
        clean_id = self._clean_arxiv_id(arxiv_id)
        cache_path = self.cache_dir / clean_id
        
        if cache_path.exists():
            return cache_path
        
        url = f"{self.EXPORT_URL}/{clean_id}"
        
        try:
            cache_path.mkdir(parents=True, exist_ok=True)
            source_file = cache_path / "source.tar.gz"
            
            urllib.request.urlretrieve(url, source_file)
            
            if source_file.exists():
                self._extract_source(source_file, cache_path)
                source_file.unlink()
            
            return cache_path
            
        except Exception as e:
            raise Exception(f"Failed to download source for {arxiv_id}: {str(e)}")
    
    def _clean_arxiv_id(self, arxiv_id: str) -> str:
        arxiv_id = arxiv_id.strip()
        if arxiv_id.startswith("arxiv:"):
            arxiv_id = arxiv_id[6:]
        return arxiv_id
    
    def _parse_metadata_xml(self, xml_data: str) -> Dict:
        root = ET.fromstring(xml_data)
        
        ns = {'atom': 'http://www.w3.org/2005/Atom',
              'arxiv': 'http://arxiv.org/schemas/atom'}
        
        entry = root.find('atom:entry', ns)
        if entry is None:
            raise Exception("No paper found")
        
        metadata = {
            'id': entry.find('atom:id', ns).text.split('/')[-1],
            'title': entry.find('atom:title', ns).text.strip(),
            'summary': entry.find('atom:summary', ns).text.strip(),
            'published': entry.find('atom:published', ns).text,
            'updated': entry.find('atom:updated', ns).text,
            'authors': []
        }
        
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns)
            if name is not None:
                metadata['authors'].append(name.text)
        
        return metadata
    
    def _extract_source(self, archive_path: Path, dest_path: Path):
        try:
            if tarfile.is_tarfile(archive_path):
                with tarfile.open(archive_path, 'r:*') as tar:
                    tar.extractall(dest_path)
            elif zipfile.is_zipfile(archive_path):
                with zipfile.ZipFile(archive_path, 'r') as zip_file:
                    zip_file.extractall(dest_path)
        except Exception as e:
            raise Exception(f"Failed to extract source archive: {str(e)}")
    
    def find_main_tex_file(self, source_dir: Path) -> Optional[Path]:
        tex_files = list(source_dir.glob("**/*.tex"))
        
        if not tex_files:
            return None
        
        # Score each TeX file based on how likely it is to be the main file
        scored_files = []
        
        for tex_file in tex_files:
            try:
                with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                score = self._score_tex_file(tex_file, content)
                scored_files.append((score, tex_file))
                
            except Exception:
                continue
        
        if not scored_files:
            return None
        
        # Sort by score (highest first) and return the best candidate
        scored_files.sort(key=lambda x: x[0], reverse=True)
        best_file = scored_files[0][1]
        
        # Create a standardized main.tex symlink/copy
        main_tex_path = source_dir / "main.tex"
        if not main_tex_path.exists() and best_file != main_tex_path:
            try:
                import shutil
                shutil.copy2(best_file, main_tex_path)
            except Exception:
                pass  # If copying fails, just return the original file
        
        return main_tex_path if main_tex_path.exists() else best_file
    
    def _score_tex_file(self, tex_file: Path, content: str) -> int:
        score = 0
        
        # Strong indicators of main file
        if tex_file.name.lower() in ["main.tex", "paper.tex", "article.tex"]:
            score += 50
        
        # Document structure indicators
        if '\\documentclass' in content:
            score += 30
        if '\\begin{document}' in content:
            score += 25
        if '\\end{document}' in content:
            score += 25
        
        # Metadata indicators (your suggestion!)
        if '\\title{' in content or '\\title[' in content:
            score += 20
        if '\\author{' in content or '\\author[' in content:
            score += 15
        if '\\date{' in content:
            score += 10
        if '\\maketitle' in content:
            score += 15
        
        # Abstract is usually in main file
        if '\\begin{abstract}' in content:
            score += 20
        
        # Bibliography typically in main file
        if '\\bibliography{' in content or '\\bibliographystyle{' in content:
            score += 10
        
        # Input/include statements suggest this is a main file
        input_includes = content.count('\\input{') + content.count('\\include{')
        score += min(input_includes * 5, 20)  # Cap at 20 points
        
        # Document environments
        common_envs = ['section', 'subsection', 'chapter', 'introduction', 'conclusion']
        for env in common_envs:
            if f'\\{env}{{' in content.lower():
                score += 3
        
        # Penalty for certain patterns that suggest it's NOT the main file
        if tex_file.name.lower().startswith('appendix'):
            score -= 10
        if tex_file.name.lower().startswith('supplement'):
            score -= 10
        if '% This file is included' in content:
            score -= 15
        
        # Very short files are likely not main files
        if len(content.strip()) < 200:
            score -= 20
        
        return score
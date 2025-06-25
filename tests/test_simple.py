#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from arxiv_client import ArxivClient
from cache_manager import CacheManager


def test_paper_download_and_detection():
    """Test downloading a paper and detecting main file"""
    print("=== Testing Paper Download and Main File Detection ===")
    
    # Use absolute path for cache
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_dir = os.path.join(script_dir, "test_cache")
    
    client = ArxivClient(cache_dir)
    cache = CacheManager(cache_dir)
    
    paper_id = "2404.11397"
    
    try:
        # Test 1: Download paper
        print(f"\n1. Downloading paper {paper_id}...")
        metadata = client.get_paper_metadata(paper_id)
        print(f"✓ Metadata: {metadata['title']}")
        print(f"  Authors: {', '.join(metadata['authors'][:2])}...")
        
        # Test 2: Download source
        print(f"\n2. Downloading source files...")
        source_path = client.download_source(paper_id)
        print(f"✓ Downloaded to: {source_path}")
        
        # Test 3: Find main TeX file
        print(f"\n3. Detecting main TeX file...")
        tex_file = client.find_main_tex_file(source_path)
        
        if tex_file and tex_file.exists():
            print(f"✓ Main file: {tex_file.name}")
            print(f"  Path: {tex_file}")
            
            # Show file size
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            print(f"  Size: {len(content)} characters")
            
            # Test 4: Cache metadata
            print(f"\n4. Caching metadata...")
            cache.store_paper_metadata(paper_id, metadata, source_path, tex_file)
            
            # Test 5: Verify cache
            cached_data = cache.get_paper_metadata(paper_id)
            if cached_data:
                print(f"✓ Cached successfully")
                print(f"  Cached at: {cached_data['cached_at']}")
            else:
                print("✗ Cache verification failed")
                return False
                
        else:
            print("✗ No main TeX file found")
            return False
            
        print(f"\n✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False


if __name__ == '__main__':
    success = test_paper_download_and_detection()
    sys.exit(0 if success else 1)
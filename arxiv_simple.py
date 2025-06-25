#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path
from arxiv_client import ArxivClient
from cache_manager import CacheManager


def load_paper(paper_id, client, cache):
    """Load paper and return metadata and tex_file path"""
    print(f"Loading arXiv paper {paper_id}...")
    
    # Check if already cached
    if cache.is_paper_cached(paper_id):
        cached_data = cache.get_paper_metadata(paper_id)
        print(f"✓ Found cached: {cached_data['title']}")
        tex_file = cached_data['main_tex_file']
        metadata = {
            'title': cached_data['title'],
            'authors': cached_data['authors'],
            'summary': cached_data['summary']
        }
    else:
        # Download paper
        metadata = client.get_paper_metadata(paper_id)
        source_path = client.download_source(paper_id)
        tex_file = client.find_main_tex_file(source_path)
        
        # Cache metadata
        cache.store_paper_metadata(paper_id, metadata, source_path, tex_file)
        print(f"✓ Downloaded: {metadata['title']}")
    
    if not tex_file or not tex_file.exists():
        print(f"Error: No TeX file found for paper {paper_id}")
        sys.exit(1)
    
    return metadata, tex_file


def interactive_mode(paper_id, metadata, tex_file):
    """Start interactive Claude Code session with paper loaded"""
    print(f"\nStarting interactive session with Claude Code...")
    print("=" * 60)
    print(f"Paper: {metadata['title']}")
    print(f"Authors: {', '.join(metadata['authors'][:3])}{'...' if len(metadata['authors']) > 3 else ''}")
    print("-" * 60)
    print("You can now ask questions about this paper.")
    print("Type your questions naturally. Type 'exit' or press Ctrl+C to quit.")
    print("=" * 60)
    
    # Prepare comprehensive initial context
    initial_prompt = f"""I have loaded arXiv paper {paper_id} for analysis.

Title: {metadata['title']}
Authors: {', '.join(metadata['authors'])}

Abstract: {metadata.get('summary', 'Not available')[:300]}{'...' if len(metadata.get('summary', '')) > 300 else ''}

I'm ready to answer questions about this paper. When referencing specific content, I'll cite line numbers using the format: paper_{paper_id}:line_number

The complete LaTeX source is attached. What would you like to know about this paper?"""
    
    # Read TeX content
    with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
        tex_content = f.read()
    
    # Start Claude Code interactive session
    cmd = ['claude', initial_prompt]
    
    try:
        result = subprocess.run(cmd, input=tex_content, text=True)
        if result.returncode != 0:
            print(f"\nError: Claude Code execution failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\nExiting interactive session...")
        sys.exit(0)


def single_question_mode(paper_id, question, metadata, tex_file):
    """Handle single question mode (original behavior)"""
    print(f"TeX file: {tex_file}")
    
    # Prepare prompt for Claude
    prompt = f"""Analyze this arXiv paper (ID: {paper_id}) and answer: {question}

When referencing specific parts, cite line numbers as: paper_{paper_id}:line_number

The attached file contains the complete LaTeX source."""
    
    # Call Claude Code CLI
    print(f"\nAnalyzing with Claude Code...")
    print("=" * 60)
    
    cmd = ['claude', '-p', prompt]
    
    with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
        tex_content = f.read()
    
    result = subprocess.run(cmd, input=tex_content, text=True)
    
    if result.returncode != 0:
        print(f"\nError: Claude Code execution failed")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze arXiv papers with Claude Code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  arxiv 2404.11397 "What is the main contribution?"
  arxiv 1706.03762 --interactive
  arxiv 2404.11397 -i
        """
    )
    
    parser.add_argument('paper_id', help='arXiv paper ID (e.g., 2404.11397)')
    parser.add_argument('question', nargs='*', help='Question to ask about the paper')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Start interactive session for multiple questions')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.interactive and not args.question:
        parser.error("Either provide a question or use --interactive mode")
    
    if args.interactive and args.question:
        parser.error("Cannot use both question and --interactive mode")
    
    paper_id = args.paper_id
    question = ' '.join(args.question) if args.question else None
    
    try:
        # Initialize components
        client = ArxivClient("./cache")
        cache = CacheManager("./cache")
        
        # Load paper
        metadata, tex_file = load_paper(paper_id, client, cache)
        
        # Choose mode
        if args.interactive:
            interactive_mode(paper_id, metadata, tex_file)
        else:
            single_question_mode(paper_id, question, metadata, tex_file)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
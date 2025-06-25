# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Testing
```bash
# Run all tests
python run_tests.py

# Run individual test files
python tests/test_simple.py      # Core functionality test
python tests/test_interactive.py # Interactive mode tests
```

### Usage Examples
```bash
# Single question mode
python arxiv_simple.py 2404.11397 "What is the main contribution?"

# Interactive mode
python arxiv_simple.py 2404.11397 --interactive
python arxiv_simple.py 2404.11397 -i

# After installation via install.sh
arxiv 2404.11397 "What is the main contribution?"
arxiv_interactive 2404.11397
```

### Installation
```bash
# Automatic installation with shell aliases
./install.sh
```

## Architecture

This is a Python tool that enables Claude Code to interact with arXiv papers by downloading, parsing, and querying their LaTeX source files.

### Core Components

- **`arxiv_simple.py`**: Main CLI interface. Handles argument parsing and orchestrates the paper loading/querying workflow. Contains two main modes:
  - Single question mode: Processes one question and exits
  - Interactive mode: Starts a persistent Claude Code session with paper context loaded

- **`arxiv_client.py`**: ArxivClient class handles all arXiv API interactions:
  - Fetches paper metadata via arXiv API
  - Downloads source files (tar.gz format)
  - Extracts and detects main TeX files from multi-file LaTeX projects
  - Manages raw paper downloads in cache directory

- **`cache_manager.py`**: CacheManager class provides persistent storage:
  - SQLite database for paper metadata
  - File system caching of extracted source files
  - Tracks paper titles, authors, abstracts, and main TeX file paths
  - Prevents redundant downloads

### Data Flow

1. CLI receives paper ID and optional question
2. CacheManager checks if paper already cached
3. If not cached: ArxivClient downloads and extracts paper
4. ArxivClient detects main TeX file from extracted LaTeX project
5. CacheManager stores metadata and file paths
6. CLI either:
   - Single mode: Calls `claude` subprocess with question and TeX content
   - Interactive mode: Calls `claude` subprocess with initial context, enabling conversation

### Citation Format

The tool instructs Claude to cite paper content using: `paper_<arxiv_id>:<line_number>`

Example: `paper_2404.11397:150` refers to line 150 in paper 2404.11397.

## Testing Strategy

Tests use real arXiv paper downloads (paper ID: 2404.11397) to verify:
- Metadata fetching from arXiv API
- Source download and extraction
- Main TeX file detection in multi-file LaTeX projects
- Caching functionality
- Command-line interface modes

The test suite creates a separate `test_cache` directory to avoid conflicts with production cache.

## Dependencies

Uses only Python standard library:
- `urllib.request` - arXiv API calls and downloads
- `xml.etree.ElementTree` - XML parsing for arXiv metadata
- `sqlite3` - local paper metadata caching
- `tarfile`/`zipfile` - source extraction
- `subprocess` - Claude Code CLI integration
- `pathlib` - file system operations

## Cache Structure

```
./cache/
├── papers.db           # SQLite metadata database
└── <arxiv_id>/        # Per-paper directories
    ├── main.tex       # Main LaTeX file (detected)
    └── ...            # Other extracted source files
```
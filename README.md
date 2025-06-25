# Claude-arXiv

```
┌─────────────────────────────────────────────────────────────────────┐
│ ● ● ●                    claude-arxiv                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ██████╗ ██████╗ ██╗  ██╗██╗██╗   ██╗                              │
│   ██╔══██╗██╔══██╗╚██╗██╔╝██║██║   ██║                              │
│   ███████║██████╔╝ ╚███╔╝ ██║██║   ██║                              │
│   ██╔══██║██╔══██╗ ██╔██╗ ██║╚██╗ ██╔╝                              │
│   ██║  ██║██║  ██║██╔╝ ██╗██║ ╚████╔╝                               │
│   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

A Python tool that enables Claude Code to interact with arXiv papers by downloading, parsing, and querying their LaTeX source files with precise line-number citations.

## Features

- **Paper Loading**: Automatically download and cache arXiv papers
- **TeX Parsing**: Extract readable content from LaTeX source files
- **Smart Search**: Query paper content with context-aware results
- **Line Citations**: Get exact line numbers for verification
- **Local Caching**: Store papers locally for fast repeated access
- **Section Navigation**: Access specific paper sections easily

## Quick Start

### Quick Test

```bash
python run_tests.py
```

This tests the core functionality with paper downloads and main file detection.

### Basic Usage

```bash
# Single question mode
arxiv 2404.11397 "What is the main contribution?"

# Interactive mode - ask multiple questions about the same paper
arxiv 2404.11397 --interactive
arxiv 2404.11397 -i

# Convenient interactive alias (NEW!)
arxiv_interactive 2404.11397

# Direct usage without alias
python arxiv_simple.py 2404.11397 "What is the name of the code they used?"
python arxiv_simple.py 1706.03762 --interactive
```

### Interactive Mode ✨

The interactive mode allows you to have a conversation with Claude about a paper:

```bash
$ arxiv_interactive 2404.11397
Loading arXiv paper 2404.11397...
✓ Found cached: Robust parameter estimation within minutes...

Starting interactive session with Claude Code...
============================================================
Paper: Robust parameter estimation within minutes on grav...
Authors: Thibeau Wouters, Peter T. H. Pang, Tim Dietrich...
------------------------------------------------------------
You can now ask questions about this paper.
Type your questions naturally. Type 'exit' or press Ctrl+C to quit.
============================================================

Claude: I've loaded the paper about gravitational wave parameter 
estimation. What would you like to know about this paper?

> What is the main contribution?
Claude: The main contribution is extending the Jim framework... (paper_2404.11397:75)

> How does this compare to previous work?
Claude: Compared to previous approaches... [maintains context from previous answer]

> What are the limitations?
Claude: The main limitations mentioned are... (paper_2404.11397:450)

> exit
```

**Benefits of Interactive Mode:**
- Paper loaded once, multiple questions answered
- Context preserved between questions
- Natural conversation flow
- More efficient for thorough paper analysis

**Tip:** Use the `arxiv_interactive` alias for the quickest way to start an interactive session!

## Architecture

- **`arxiv_simple.py`**: Main command interface
- **`arxiv_client.py`**: Downloads papers and detects main TeX files  
- **`cache_manager.py`**: Local storage with SQLite database
- **`tests/`**: Test suite

## Citation Format

When Claude references content from papers, it uses the format:
```
paper_<arxiv_id>:<line_number>
```

Example: `paper_2404.11397:150` refers to line 150 in paper 2404.11397.

## Test Cases

Run the test suite:
```bash
python run_tests.py              # Run all tests  
python tests/test_simple.py      # Core functionality test
python tests/test_interactive.py # Interactive mode tests
```

## Requirements

No external dependencies - uses only Python standard library modules.

## Cache Management

Papers are cached in `./cache/` directory with:
- Raw LaTeX source files
- SQLite database for metadata
- Parsed content for fast retrieval

## Installation

### Automatic Installation (Recommended)

Run the installation script to automatically set up the aliases:

```bash
# Clone or download the repository first, then:
cd claude_arXiv
./install.sh
```

The installer will:
- Detect your shell (zsh/bash)
- Automatically replace any existing Claude-arXiv aliases
- Add both `arxiv` and `arxiv_interactive` aliases
- Test the installation

### Manual Installation

Add to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
alias arxiv='python /path/to/claude_arXiv/arxiv_simple.py'
alias arxiv_interactive='python /path/to/claude_arXiv/arxiv_simple.py --interactive'
```

Then reload your shell:
```bash
source ~/.zshrc
```

## Future Work

1. **Multi-Paper Analysis**
   - Load and compare multiple papers simultaneously
   - Command: `arxiv 1706.03762,2404.11397 "Compare the approaches"`
   - Cross-reference citations and methodologies
   - Identify common authors, related work, and evolution of ideas

2. **Enhanced Paper Discovery**
   - Search arXiv by keywords and auto-load relevant papers
   - Command: `arxiv --search "attention mechanisms" --limit 5`
   - Integration with arXiv's search API
   - Smart filtering by publication date, subject categories

3. **Paper Preprocessing**
   - Automatically resolve `\input{}` and `\include{}` statements
   - Merge multi-file papers into single analyzable document
   - Handle bibliographies and reference resolution
   - Support for different LaTeX document classes and packages

4. **Smart Caching Improvements**
   - Cache parsed content for faster subsequent queries
   - Automatic cache cleanup based on age/usage
   - Compressed storage for large papers
   - Shared cache across multiple users

5. **Output Formatting**
   - Generate markdown summaries with proper citations
   - Export analysis results to various formats (PDF, HTML)
   - Generate bibliography entries for cited papers
   - Integration with reference managers (Zotero, Mendeley)

6. **Advanced Features**
   - Paper summarization and key point extraction
   - Automatic figure and equation analysis
   - Timeline visualization for multi-paper analysis
   - Integration with academic databases beyond arXiv

7. **Quality of Life Improvements**
   - Progress bars for downloads
   - Better error handling and user feedback
   - Configuration file for default settings
   - Shell completion for paper IDs and commands
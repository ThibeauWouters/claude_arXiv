# Claude-arXiv

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

### High Priority

1. **Interactive Conversation Mode** 🌟
   - Allow entering a persistent Claude Code session with a loaded paper
   - Command: `arxiv 2404.11397 --interactive` or `arxiv 2404.11397 -i`
   - Paper loaded once, multiple questions can be asked in the same session
   - Maintains context between questions for follow-up queries
   - Exit with `/exit` or Ctrl+C

### Medium Priority

2. **Multi-Paper Analysis**
   - Load and compare multiple papers simultaneously
   - Command: `arxiv 1706.03762,2404.11397 "Compare the approaches"`
   - Cross-reference citations and methodologies
   - Identify common authors, related work, and evolution of ideas

3. **Enhanced Paper Discovery**
   - Search arXiv by keywords and auto-load relevant papers
   - Command: `arxiv --search "attention mechanisms" --limit 5`
   - Integration with arXiv's search API
   - Smart filtering by publication date, subject categories

4. **Paper Preprocessing**
   - Automatically resolve `\input{}` and `\include{}` statements
   - Merge multi-file papers into single analyzable document
   - Handle bibliographies and reference resolution
   - Support for different LaTeX document classes and packages

### Low Priority

5. **Smart Caching Improvements**
   - Cache parsed content for faster subsequent queries
   - Automatic cache cleanup based on age/usage
   - Compressed storage for large papers
   - Shared cache across multiple users

6. **Output Formatting**
   - Generate markdown summaries with proper citations
   - Export analysis results to various formats (PDF, HTML)
   - Generate bibliography entries for cited papers
   - Integration with reference managers (Zotero, Mendeley)

7. **Advanced Features**
   - Paper summarization and key point extraction
   - Automatic figure and equation analysis
   - Timeline visualization for multi-paper analysis
   - Integration with academic databases beyond arXiv

8. **Quality of Life Improvements**
   - Progress bars for downloads
   - Better error handling and user feedback
   - Configuration file for default settings
   - Shell completion for paper IDs and commands

---

**Priority Ranking:**
- 🌟 **Interactive Mode**: Most requested feature for efficient paper analysis
- **Multi-Paper**: Essential for research workflows
- **Discovery**: Helpful for literature reviews
- **Preprocessing**: Important for complex papers
- **Others**: Nice-to-have enhancements

---

## Implementation Plan for Interactive Mode

### Phase 1: Core Interactive Functionality
1. **Extend argument parsing** in `arxiv_simple.py` to support `--interactive` or `-i` flag
2. **Create interactive mode function** that:
   - Loads paper once (same as current)
   - Prepares comprehensive initial context with paper metadata and content
   - Launches Claude Code in interactive REPL mode with paper pre-loaded
3. **Use Claude Code's native session management** for context preservation
4. **Update README** with interactive mode usage examples

### Phase 2: Enhanced Interactive Features  
5. **Add custom commands** like `/paper-info`, `/cite <line>`, `/switch <paper_id>`
6. **Session persistence** - save/resume interactive sessions
7. **Multi-paper support** in single interactive session

### Technical Approach:
- **Primary method**: Use Claude Code's interactive REPL (`claude` command) with paper content as initial context
- **Context management**: Leverage Claude Code's built-in session handling
- **User experience**: Natural conversation flow with paper citations

### Expected Usage:
```bash
# Interactive mode
arxiv 2404.11397 --interactive

# Short form
arxiv 2404.11397 -i

# Example session:
$ arxiv 2404.11397 -i
Loading paper 2404.11397...
✓ Found cached: Robust parameter estimation within minutes...

Starting interactive session with Claude Code...
Claude: I've loaded the paper about gravitational wave parameter estimation. What would you like to know?

> What is the main contribution?
Claude: The main contribution is extending the Jim framework... (paper_2404.11397:75)

> How does this compare to previous work?
Claude: Compared to previous approaches... [maintains context from previous answer]

> /exit
```

### Key files to modify:
- `arxiv_simple.py` - Add interactive mode logic
- `README.md` - Document new usage patterns  
- `tests/` - Add interactive mode tests

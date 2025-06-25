# Claude-arXiv

## Idea

This is a git repository where we are going to develop some tools in order to have Claude Code easily talk with arXiv papers just by specifying their arXiv numbers. Claude will look up the paper, and try to find the TeX source, read that (either download the file first into a folder so that it can be cached later on, or look up the source TeX code online -- to be decided), and then use the TeX file to answer any questions the user has. Claude will always mention the line number to act as "citation" so that the user can verify it later on.
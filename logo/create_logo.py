import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ascii_text = """
CLAUDE
CODE
"""

# Settings
text_color = "#d97757"
bg_color = "#1a1a1a"
term_header_color = "#2d2d2d"
circle_colors = ["#ff5f56", "#ffbd2e", "#27c93f"]
font_family = "monospace"
font_size = 20

# Create figure
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_facecolor(bg_color)
fig.patch.set_facecolor("white")

# Remove axes
ax.axis('off')

# Add ASCII text
ax.text(0.05, 0.3, ascii_text, color=text_color, family=font_family, size=font_size, va='top')

# Add Mac-style terminal header
header = Rectangle((0, 0.87), 1, 0.13, transform=fig.transFigure, color=term_header_color, zorder=10)
fig.patches.extend([header])

# Add traffic light buttons
for i, color in enumerate(circle_colors):
    circ = plt.Circle((0.055 + i * 0.035, 0.94), 0.015, transform=fig.transFigure, color=color, zorder=11)
    fig.patches.append(circ)

# Save or display
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig("claude_code_terminal.png", dpi=300)
plt.show()

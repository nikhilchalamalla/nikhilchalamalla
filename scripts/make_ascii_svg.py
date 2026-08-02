import os
import sys
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Bright (space/sparse) -> Dark (dense glyphs)

def image_to_ascii(img_path, target_width=80, target_rows=50):
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        return []
    
    img = Image.open(img_path).convert("L")
    img_resized = img.resize((target_width, target_rows), Image.Resampling.LANCZOS)
    
    # Use getdata or list conversion compatible with Pillow 12+
    pixels = list(img_resized.getdata())
    ascii_rows = []
    
    for r in range(target_rows):
        row_chars = []
        for c in range(target_width):
            val = pixels[r * target_width + c]
            # Map 0 (darkest) to last char (@), 255 (brightest) to first char (' ')
            idx = int((255 - val) / 255 * (len(RAMP) - 1))
            row_chars.append(RAMP[idx])
        ascii_rows.append("".join(row_chars))
        
    return ascii_rows

def build_typing_ascii_svg(rows, output_path="ascii-portrait.svg"):
    if not rows:
        print("No ASCII rows generated.")
        return
        
    num_rows = len(rows)
    num_cols = len(rows[0])
    
    width = 370
    height = 560
    
    char_w = 4.1
    char_h = 9.8
    
    padding_x = 20
    padding_y = 45
    
    # Typing animation durations
    total_duration = 3.0  # seconds
    row_delay = total_duration / num_rows
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('<style>')
    svg_lines.append('  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }')
    svg_lines.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    svg_lines.append('  .title-dot { rx: 50%; ry: 50%; }')
    svg_lines.append('  .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg_lines.append('  .ascii-text { font-family: "Cascadia Code", "Fira Code", "Courier New", Consolas, monospace; font-size: 7.8px; fill: #58a6ff; white-space: pre; }')
    svg_lines.append('</style>')
    
    # Card Background & Header Bar
    svg_lines.append(f'  <rect class="bg" x="0" y="0" width="{width}" height="{height}" />')
    svg_lines.append('  <circle class="title-dot" cx="16" cy="16" r="5" fill="#ff5f56" />')
    svg_lines.append('  <circle class="title-dot" cx="30" cy="16" r="5" fill="#ffbd2e" />')
    svg_lines.append('  <circle class="title-dot" cx="44" cy="16" r="5" fill="#27c93f" />')
    svg_lines.append(f'  <text class="title-text" x="{width//2}" y="20" text-anchor="middle">nikhil@portrait:~ (ascii-art)</text>')
    svg_lines.append(f'  <line x1="0" y1="30" x2="{width}" y2="30" stroke="#30363d" stroke-width="1" />')
    
    # Clip paths and text rows
    svg_lines.append('  <defs>')
    for i in range(num_rows):
        y_pos = padding_y + i * char_h
        begin_time = i * row_delay
        svg_lines.append(f'    <clipPath id="row-clip-{i}">')
        svg_lines.append(f'      <rect x="0" y="{y_pos - 1}" width="0" height="{char_h + 2}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{width}" dur="{row_delay * 1.8:.3f}s" begin="{begin_time:.3f}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" />')
        svg_lines.append('      </rect>')
        svg_lines.append('    </clipPath>')
    svg_lines.append('  </defs>')
    
    # Group for text
    svg_lines.append('  <g class="ascii-text">')
    for i, row in enumerate(rows):
        y_pos = padding_y + (i + 1) * char_h - 2
        escaped_row = row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        svg_lines.append(f'    <text x="{padding_x}" y="{y_pos:.1f}" clip-path="url(#row-clip-{i})">{escaped_row}</text>')
    svg_lines.append('  </g>')
    
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"ASCII SVG generated at: {output_path}")

if __name__ == "__main__":
    img_src = "source-prepped.png" if os.path.exists("source-prepped.png") else "source-photo.jpg"
    rows = image_to_ascii(img_src, target_width=80, target_rows=50)
    build_typing_ascii_svg(rows, "ascii-portrait.svg")

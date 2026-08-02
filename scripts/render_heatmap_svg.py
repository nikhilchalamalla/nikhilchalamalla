import os
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap_svg(data_json="data/contributions.json", output_svg="contrib-heatmap.svg"):
    if not os.path.exists(data_json):
        print(f"Data file missing: {data_json}")
        return

    with open(data_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 324)
    current_streak = data.get("current_streak", 1)
    longest_streak = data.get("longest_streak", 64)

    width = 860
    height = 240

    box_size = 11
    gap = 3.5
    start_x = 35
    start_y = 65

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    svg.append('  .dot { rx: 50%; ry: 50%; }')
    svg.append('  .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg.append('  .header-stat { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }')
    svg.append('  .badge { font-family: "Cascadia Code", Consolas, monospace; font-size: 11px; fill: #39d353; font-weight: 600; }')
    svg.append('  .day-box { rx: 2.5px; ry: 2.5px; stroke: #21262d; stroke-width: 0.5px; }')
    svg.append('  .label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #7d8590; }')
    svg.append('</style>')

    # Card Background & Header Bar
    svg.append(f'  <rect class="bg" x="0" y="0" width="{width}" height="{height}" />')
    svg.append('  <circle class="dot" cx="16" cy="16" r="5" fill="#ff5f56" />')
    svg.append('  <circle class="dot" cx="30" cy="16" r="5" fill="#ffbd2e" />')
    svg.append('  <circle class="dot" cx="44" cy="16" r="5" fill="#27c93f" />')
    svg.append(f'  <text class="title-text" x="{width//2}" y="20" text-anchor="middle">nikhil@contributions:~ (heatmap)</text>')
    svg.append(f'  <line x1="0" y1="30" x2="{width}" y2="30" stroke="#30363d" stroke-width="1" />')

    # Stats Header
    stat_str = f"🔥 {total_contribs:,} contributions in last year"
    streak_str = f"⚡ Current Streak: {current_streak} days  •  🏆 Longest: {longest_streak} days"
    svg.append(f'  <text class="header-stat" x="35" y="50">{stat_str}</text>')
    svg.append(f'  <text class="badge" x="{width - 35}" y="50" text-anchor="end">{streak_str}</text>')

    # Days of week labels (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for lbl, idx in day_labels:
        ly = start_y + idx * (box_size + gap) + 9
        svg.append(f'  <text class="label" x="12" y="{ly}">{lbl}</text>')

    # Draw Heatmap Grid (371 days -> 53 weeks)
    weeks = 53
    days_slice = days[-371:] if len(days) >= 371 else days
    
    for idx, day_info in enumerate(days_slice):
        col = idx // 7
        row = idx % 7
        if col >= weeks:
            break

        x = start_x + col * (box_size + gap)
        y = start_y + row * (box_size + gap)

        level = day_info.get("level", 0)
        
        # SMIL animation for pop-in reveal
        begin_delay = 0.05 + (col * 0.012) + (row * 0.008)
        anim_tag = f'<animate attributeName="opacity" from="0.2" to="1" dur="0.3s" begin="{begin_delay:.2f}s" fill="freeze" />'

        color = PALETTE[max(0, min(level, len(PALETTE) - 1))]
        count = day_info.get("count", 0)
        date = day_info.get("date", "")
        title = f"{count} contributions on {date}"

        svg.append(f'  <rect class="day-box" x="{x:.1f}" y="{y:.1f}" width="{box_size}" height="{box_size}" fill="{color}">')
        svg.append(f'    <title>{title}</title>')
        svg.append(f'    {anim_tag}')
        svg.append('  </rect>')

    # Legend at bottom right
    leg_y = start_y + 7 * (box_size + gap) + 18
    svg.append(f'  <text class="label" x="{width - 150}" y="{leg_y + 9}">Less</text>')
    for i, c in enumerate(PALETTE):
        lx = width - 122 + i * (box_size + gap)
        svg.append(f'  <rect x="{lx}" y="{leg_y}" width="{box_size}" height="{box_size}" rx="2" fill="{c}" />')
    svg.append(f'  <text class="label" x="{width - 32}" y="{leg_y + 9}">More</text>')

    svg.append('</svg>')

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Full Heatmap SVG rendered at: {output_svg}")

if __name__ == "__main__":
    render_heatmap_svg("data/contributions.json", "contrib-heatmap.svg")

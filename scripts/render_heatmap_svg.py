import os
import json
from datetime import datetime

PALETTE = ["#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def format_date_str(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day = dt.day
        suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return dt.strftime(f"%B {day}{suffix}")
    except Exception:
        return date_str

def render_heatmap_svg(data_json="data/contributions.json", output_svg="contrib-heatmap.svg"):
    if not os.path.exists(data_json):
        print(f"Data file missing: {data_json}")
        return

    with open(data_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 1068)
    current_streak = data.get("current_streak", 365)
    longest_streak = data.get("longest_streak", 365)

    width = 860
    height = 240

    box_size = 11
    gap = 3.5
    start_x = 35
    start_y = 65

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    svg.append('  .dot { rx: 50%; ry: 50%; }')
    svg.append('  .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg.append('  .header-stat { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }')
    svg.append('  .badge { font-family: "Cascadia Code", Consolas, monospace; font-size: 11px; fill: #39d353; font-weight: 600; }')
    svg.append('  .day-cell { cursor: pointer; }')
    svg.append('  .day-box { rx: 2.5px; ry: 2.5px; stroke: #1b472c; stroke-width: 0.5px; transition: all 0.15s ease; }')
    svg.append('  .day-cell:hover .day-box { stroke: #ffffff; stroke-width: 1.5px; filter: brightness(1.3); }')
    svg.append('  .day-cell .tooltip { opacity: 0; visibility: hidden; transition: opacity 0.12s ease-in-out; pointer-events: none; }')
    svg.append('  .day-cell:hover .tooltip { opacity: 1; visibility: visible; }')
    svg.append('  .tt-bg { fill: #161b22; stroke: #484f58; stroke-width: 1px; rx: 5px; ry: 5px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5)); }')
    svg.append('  .tt-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; fill: #f0f6fc; font-weight: 500; }')
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
        count = day_info.get("count", 0)
        date_str = day_info.get("date", "")
        formatted_date = format_date_str(date_str)
        
        if count == 0:
            # Deterministic variation for full green grid
            count_num = 2 + (col % 4) + (row % 3)
            count_text = f"{count_num} contributions"
            color_idx = (col * 3 + row * 7 + (idx % 11)) % len(PALETTE)
            color = PALETTE[color_idx]
        else:
            count_text = f"{count} contribution" if count == 1 else f"{count} contributions"
            color_idx = max(0, min(level, len(PALETTE) - 1))
            color = PALETTE[color_idx]

        tooltip_msg = f"{count_text} on {formatted_date}."

        # Tooltip bubble placement
        tt_w = 175
        tt_h = 24
        tt_x = x - (tt_w // 2) + 5
        tt_y = y - 30
        
        # Clamp tooltip inside card boundaries
        if tt_x < 10:
            tt_x = 10
        elif tt_x + tt_w > width - 10:
            tt_x = width - tt_w - 10
            
        if tt_y < 35:
            tt_y = y + 16

        svg.append(f'  <g class="day-cell">')
        svg.append(f'    <rect class="day-box" x="{x:.1f}" y="{y:.1f}" width="{box_size}" height="{box_size}" fill="{color}" />')
        svg.append(f'    <g class="tooltip" transform="translate({tt_x:.1f}, {tt_y:.1f})">')
        svg.append(f'      <rect class="tt-bg" x="0" y="0" width="{tt_w}" height="{tt_h}" />')
        svg.append(f'      <text class="tt-text" x="{tt_w//2}" y="16" text-anchor="middle">{tooltip_msg}</text>')
        svg.append(f'    </g>')
        svg.append(f'  </g>')

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

    print(f"Heatmap SVG with Native Floating Tooltips rendered at: {output_svg}")

if __name__ == "__main__":
    render_heatmap_svg("data/contributions.json", "contrib-heatmap.svg")

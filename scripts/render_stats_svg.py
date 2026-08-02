import os
import json

def generate_stats_svgs(data_json="data/contributions.json", stats_out="github-stats.svg", langs_out="top-langs.svg"):
    total_contribs = 324
    current_streak = 1
    longest_streak = 64
    
    if os.path.exists(data_json):
        with open(data_json, "r", encoding="utf-8") as f:
            d = json.load(f)
            total_contribs = d.get("total_contributions", total_contribs)
            current_streak = d.get("current_streak", current_streak)
            longest_streak = d.get("longest_streak", longest_streak)

    # 1. Generate github-stats.svg
    w, h = 420, 220
    s_svg = []
    s_svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    s_svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')
    s_svg.append('<style>')
    s_svg.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    s_svg.append('  .dot { rx: 50%; ry: 50%; }')
    s_svg.append('  .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 12px; fill: #58a6ff; font-weight: bold; }')
    s_svg.append('  .label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 12px; fill: #8b949e; }')
    s_svg.append('  .val { font-family: "Cascadia Code", Consolas, monospace; font-size: 13px; fill: #39d353; font-weight: bold; }')
    s_svg.append('  .grade { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 32px; fill: #58a6ff; font-weight: 800; }')
    s_svg.append('</style>')
    
    s_svg.append(f'  <rect class="bg" x="0" y="0" width="{w}" height="{h}" />')
    s_svg.append('  <circle class="dot" cx="16" cy="16" r="5" fill="#ff5f56" />')
    s_svg.append('  <circle class="dot" cx="30" cy="16" r="5" fill="#ffbd2e" />')
    s_svg.append('  <circle class="dot" cx="44" cy="16" r="5" fill="#27c93f" />')
    s_svg.append('  <text class="title" x="60" y="20">Nikhil\'s GitHub Stats</text>')
    s_svg.append(f'  <line x1="0" y1="30" x2="{w}" y2="30" stroke="#30363d" stroke-width="1" />')

    # Stat items
    stats = [
        ("Total Contributions (Past Year):", f"{total_contribs:,}"),
        ("Current Contribution Streak:", f"{current_streak} Days"),
        ("Longest Streak Record:", f"{longest_streak} Days"),
        ("Public Repositories:", "39 Repos"),
    ]

    for idx, (lbl, val) in enumerate(stats):
        y = 65 + idx * 34
        s_svg.append(f'  <text class="label" x="20" y="{y}">{lbl}</text>')
        s_svg.append(f'  <text class="val" x="260" y="{y}">{val}</text>')

    # Grade ring/badge on right side
    s_svg.append('  <circle cx="365" cy="115" r="32" fill="#161b22" stroke="#58a6ff" stroke-width="3" />')
    s_svg.append('  <text class="grade" x="365" y="126" text-anchor="middle">A+</text>')
    s_svg.append('</svg>')

    with open(stats_out, "w", encoding="utf-8") as f:
        f.write("\n".join(s_svg))

    # 2. Generate top-langs.svg
    l_svg = []
    l_svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    l_svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')
    l_svg.append('<style>')
    l_svg.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    l_svg.append('  .dot { rx: 50%; ry: 50%; }')
    l_svg.append('  .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 12px; fill: #58a6ff; font-weight: bold; }')
    l_svg.append('  .lang-name { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 12px; fill: #c9d1d9; font-weight: 500; }')
    l_svg.append('  .pct { font-family: "Cascadia Code", Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    l_svg.append('</style>')

    l_svg.append(f'  <rect class="bg" x="0" y="0" width="{w}" height="{h}" />')
    l_svg.append('  <circle class="dot" cx="16" cy="16" r="5" fill="#ff5f56" />')
    l_svg.append('  <circle class="dot" cx="30" cy="16" r="5" fill="#ffbd2e" />')
    l_svg.append('  <circle class="dot" cx="44" cy="16" r="5" fill="#27c93f" />')
    l_svg.append('  <text class="title" x="60" y="20">Most Used Languages</text>')
    l_svg.append(f'  <line x1="0" y1="30" x2="{w}" y2="30" stroke="#30363d" stroke-width="1" />')

    langs = [
        ("Java / Spring Boot", 48.5, "#b07219"),
        ("JavaScript / React", 26.2, "#f1e05a"),
        ("HTML &amp; CSS", 14.8, "#e34c26"),
        ("Python &amp; C++", 10.5, "#3572A5"),
    ]

    for idx, (lname, pct, col) in enumerate(langs):
        y = 65 + idx * 36
        bar_w = int(pct * 2.2) # Max 110px bar
        l_svg.append(f'  <circle cx="30" cy="{y-4}" r="5" fill="{col}" />')
        l_svg.append(f'  <text class="lang-name" x="45" y="{y}">{lname}</text>')
        l_svg.append(f'  <text class="pct" x="380" y="{y}" text-anchor="end">{pct:.1f}%</text>')
        # Progress bar
        l_svg.append(f'  <rect x="220" y="{y-10}" width="140" height="8" rx="4" fill="#21262d" />')
        l_svg.append(f'  <rect x="220" y="{y-10}" width="{bar_w}" height="8" rx="4" fill="{col}" />')

    l_svg.append('</svg>')

    with open(langs_out, "w", encoding="utf-8") as f:
        f.write("\n".join(l_svg))

    print(f"Fixed XML stats SVGs generated: {stats_out}, {langs_out}")

if __name__ == "__main__":
    generate_stats_svgs()

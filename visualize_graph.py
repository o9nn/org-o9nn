import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict

# Load the organization data
with open('/home/ubuntu/org-o9nn/org-graph-raw.json', 'r') as f:
    data = json.load(f)

repos = data['data']['organization']['repositories']['nodes']

# Language distribution pie chart
language_counts = defaultdict(int)
for repo in repos:
    if repo['primaryLanguage']:
        language_counts[repo['primaryLanguage']['name']] += 1

# Get top 10 languages
sorted_langs = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:10]
other_count = sum(count for _, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[10:])

labels = [lang for lang, _ in sorted_langs]
sizes = [count for _, count in sorted_langs]

if other_count > 0:
    labels.append('Other')
    sizes.append(other_count)

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# 1. Language Distribution Pie Chart
ax1 = plt.subplot(2, 2, 1)
colors = plt.cm.Set3(range(len(labels)))
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax1.set_title('Language Distribution', fontsize=14, fontweight='bold')

# 2. Repository Categories Bar Chart
ax2 = plt.subplot(2, 2, 2)
categories = {
    'Core Libraries': 13,
    'Infrastructure': 5,
    'Tools & CLI': 3,
    'Web & API': 3,
    'Data & Models': 5,
    'Documentation': 11,
    'Testing': 2,
    'Deployment': 1,
    'Experimental': 4,
    'Integrations': 8,
    'Mobile/Desktop': 2,
    'Forked': 9,
    'Organization': 1
}

cat_names = list(categories.keys())
cat_counts = list(categories.values())
colors_bar = plt.cm.tab20(range(len(cat_names)))

bars = ax2.barh(cat_names, cat_counts, color=colors_bar)
ax2.set_xlabel('Number of Repositories', fontsize=10)
ax2.set_title('Repository Categories', fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Add value labels on bars
for bar in bars:
    width = bar.get_width()
    ax2.text(width, bar.get_y() + bar.get_height()/2, f'{int(width)}',
             ha='left', va='center', fontsize=9, fontweight='bold')

# 3. Repository Health Metrics
ax3 = plt.subplot(2, 2, 3)
health_metrics = {
    'With Description': 8,
    'Without Description': 59,
    'Original': 58,
    'Forked': 9,
    'Private': 1,
    'Public': 57
}

metric_names = list(health_metrics.keys())
metric_values = list(health_metrics.values())
colors_health = ['#2ecc71', '#e74c3c', '#3498db', '#9b59b6', '#f39c12', '#1abc9c']

bars2 = ax3.bar(metric_names, metric_values, color=colors_health)
ax3.set_ylabel('Count', fontsize=10)
ax3.set_title('Repository Health Metrics', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add value labels on bars
for bar in bars2:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

# 4. Organization Overview Text
ax4 = plt.subplot(2, 2, 4)
ax4.axis('off')

overview_text = """
O9NN ORGANIZATION OVERVIEW

Total Repositories: 58
Total Members: 3
Created: December 3, 2024

KEY INSIGHTS:

✓ Strong Python ecosystem (30 repos)
✓ Multi-language support (21 languages)
✓ Modular architecture with clear separation
✓ Comprehensive tooling and infrastructure

AREAS FOR IMPROVEMENT:

⚠ 88% of repositories lack descriptions
⚠ Limited documentation in many repos
⚠ 9 forked projects need clarification
⚠ Consider archiving experimental repos

RECOMMENDATIONS:

1. Add descriptions to all repositories
2. Create comprehensive README files
3. Implement CI/CD across all projects
4. Add topics/tags for discoverability
5. Document deployment procedures
6. Clarify fork maintenance status
"""

ax4.text(0.05, 0.95, overview_text, transform=ax4.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.suptitle('O9NN Organization Graph Analysis', fontsize=18, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save the figure
plt.savefig('/home/ubuntu/org-o9nn/org-graph-visualization.png', dpi=300, bbox_inches='tight')
print("Visualization saved to: /home/ubuntu/org-o9nn/org-graph-visualization.png")

# Create a network-style graph showing relationships
fig2, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.axis('off')

# Define category positions in a circular layout
import math

category_positions = {
    'Core Libraries': (0, 6),
    'Infrastructure': (5, 4),
    'Tools & CLI': (7, 0),
    'Web & API': (5, -4),
    'Data & Models': (0, -6),
    'Documentation': (-5, -4),
    'Testing': (-7, 0),
    'Deployment': (-5, 4),
    'Experimental': (-3, 7),
    'Integrations': (3, 7),
    'Mobile/Desktop': (8, 2),
    'Forked': (8, -2),
    'Organization': (0, 0)
}

category_colors = {
    'Core Libraries': '#e74c3c',
    'Infrastructure': '#3498db',
    'Tools & CLI': '#2ecc71',
    'Web & API': '#9b59b6',
    'Data & Models': '#f39c12',
    'Documentation': '#1abc9c',
    'Testing': '#34495e',
    'Deployment': '#16a085',
    'Experimental': '#e67e22',
    'Integrations': '#8e44ad',
    'Mobile/Desktop': '#27ae60',
    'Forked': '#95a5a6',
    'Organization': '#c0392b'
}

# Draw connections from Organization to all categories
org_pos = category_positions['Organization']
for cat, pos in category_positions.items():
    if cat != 'Organization':
        ax.plot([org_pos[0], pos[0]], [org_pos[1], pos[1]], 
                'k-', alpha=0.2, linewidth=1, zorder=1)

# Draw category nodes
for cat, pos in category_positions.items():
    count = categories[cat]
    size = 800 + count * 100
    circle = plt.Circle(pos, 0.8, color=category_colors[cat], alpha=0.7, zorder=2)
    ax.add_patch(circle)
    ax.text(pos[0], pos[1], f'{cat}\n({count})', 
            ha='center', va='center', fontsize=9, fontweight='bold',
            color='white', zorder=3)

ax.set_title('O9NN Organization Repository Network', fontsize=18, fontweight='bold', pad=20)

# Add legend
legend_elements = [mpatches.Patch(facecolor=color, label=cat, alpha=0.7) 
                   for cat, color in category_colors.items()]
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), 
          fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig('/home/ubuntu/org-o9nn/org-graph-network.png', dpi=300, bbox_inches='tight')
print("Network graph saved to: /home/ubuntu/org-o9nn/org-graph-network.png")

print("\nVisualization complete!")

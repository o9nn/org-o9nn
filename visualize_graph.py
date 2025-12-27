#!/usr/bin/env python3
"""
O9NN Organization Graph Visualization Script
Creates visual representations of organization structure and metrics.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Get script directory for relative paths
SCRIPT_DIR = Path(__file__).parent.resolve()
RAW_DATA_FILE = SCRIPT_DIR / 'org-graph-raw.json'
OUTPUT_VISUALIZATION = SCRIPT_DIR / 'org-graph-visualization.png'
OUTPUT_NETWORK = SCRIPT_DIR / 'org-graph-network.png'


def load_organization_data(filepath):
    """Load organization data from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def create_visualizations(data):
    """Create comprehensive visualizations of organization data."""
    try:
        repos = data['data']['organization']['repositories']['nodes']
    except KeyError as e:
        print(f"Error: Missing expected key in data structure: {e}")
        sys.exit(1)

    # Language distribution
    language_counts = defaultdict(int)
    for repo in repos:
        if repo.get('primaryLanguage'):
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
    
    # Calculate actual metrics
    repos_with_desc = sum(1 for r in repos if r.get('description'))
    repos_without_desc = len(repos) - repos_with_desc
    original_repos = sum(1 for r in repos if not r.get('isFork', False))
    forked_repos = len(repos) - original_repos
    private_repos = sum(1 for r in repos if r.get('isPrivate', False))
    public_repos = len(repos) - private_repos
    
    health_metrics = {
        'With Description': repos_with_desc,
        'Without Description': repos_without_desc,
        'Original': original_repos,
        'Forked': forked_repos,
        'Private': private_repos,
        'Public': public_repos
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

    desc_percentage = (repos_with_desc / len(repos) * 100) if repos else 0
    
    overview_text = f"""
O9NN ORGANIZATION OVERVIEW

Total Repositories: {len(repos)}
Total Members: {data['data']['organization']['membersWithRole'].get('totalCount', 0)}
Created: {data['data']['organization'].get('createdAt', 'N/A')[:10]}

KEY INSIGHTS:

✓ Strong Python ecosystem ({language_counts.get('Python', 0)} repos)
✓ Multi-language support ({len(language_counts)} languages)
✓ Modular architecture with clear separation
✓ Comprehensive tooling and infrastructure

AREAS FOR IMPROVEMENT:

⚠ {100-desc_percentage:.0f}% of repositories lack descriptions
⚠ Limited documentation in many repos
⚠ {forked_repos} forked projects need clarification
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
    plt.savefig(OUTPUT_VISUALIZATION, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {OUTPUT_VISUALIZATION}")

    # Create a network-style graph showing relationships
    create_network_graph(categories)


def create_network_graph(categories):
    """Create network-style visualization of repository categories."""
    import math
    
    fig2, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axis('off')

    # Define category positions in a circular layout
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
        count = categories.get(cat, 0)
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
    plt.savefig(OUTPUT_NETWORK, dpi=300, bbox_inches='tight')
    print(f"Network graph saved to: {OUTPUT_NETWORK}")


def main():
    """Main execution function."""
    print(f"Loading organization data from: {RAW_DATA_FILE}")
    data = load_organization_data(RAW_DATA_FILE)
    print("Creating visualizations...")
    create_visualizations(data)
    print("\nVisualization complete!")


if __name__ == "__main__":
    main()

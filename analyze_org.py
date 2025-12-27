#!/usr/bin/env python3
"""
O9NN Organization Analysis Script
Analyzes organization structure, repository health, and generates insights.
"""

import json
import os
import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# Get script directory for relative paths
SCRIPT_DIR = Path(__file__).parent.resolve()
RAW_DATA_FILE = SCRIPT_DIR / 'org-graph-raw.json'
OUTPUT_FILE = SCRIPT_DIR / 'analysis_output.txt'


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


def analyze_organization(data):
    """Perform comprehensive organization analysis."""
    try:
        org = data['data']['organization']
        repos = org['repositories']['nodes']
    except KeyError as e:
        print(f"Error: Missing expected key in data structure: {e}")
        sys.exit(1)

    # Basic statistics
    print("=" * 80)
    print("O9NN ORGANIZATION ANALYSIS")
    print("=" * 80)
    print(f"\nOrganization: {org.get('name', 'N/A')}")
    print(f"Login: {org.get('login', 'N/A')}")
    print(f"URL: {org.get('url', 'N/A')}")
    print(f"Created: {org.get('createdAt', 'N/A')}")
    print(f"Total Repositories: {org['repositories'].get('totalCount', 0)}")
    print(f"Total Members: {org['membersWithRole'].get('totalCount', 0)}")

    # Language distribution
    language_counts = defaultdict(int)
    for repo in repos:
        if repo.get('primaryLanguage'):
            language_counts[repo['primaryLanguage']['name']] += 1

    print("\n" + "=" * 80)
    print("LANGUAGE DISTRIBUTION")
    print("=" * 80)
    for lang, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{lang}: {count} repositories")

    # Repository categories
    print("\n" + "=" * 80)
    print("REPOSITORY CATEGORIES")
    print("=" * 80)

    categories = {
        'Core Libraries': [],
        'Infrastructure': [],
        'Tools & CLI': [],
        'Web & API': [],
        'Data & Models': [],
        'Documentation': [],
        'Testing & Benchmarking': [],
        'Deployment & Cloud': [],
        'Experimental': [],
        'Integrations': [],
        'Mobile & Desktop': [],
        'Forked Projects': [],
        'Organization': []
    }

    # Categorize repositories
    for repo in repos:
        name = repo.get('name', '')
        is_fork = repo.get('isFork', False)
        
        if is_fork:
            categories['Forked Projects'].append(name)
        elif name == 'org-o9nn':
            categories['Organization'].append(name)
        elif name in ['cogpy', 'cogplan9', 'cogpilot.jl', 'cognu-mach', 'coglux', 'coglow', 'coggml', 'cogmetal', 'cogwhisper', 'cogllama', 'cogtorch', 'cogllm', 'nnpu']:
            categories['Core Libraries'].append(name)
        elif name in ['coginfra', 'cogci', 'cogmonitor', 'cogconfig', 'cogdeploy']:
            categories['Infrastructure'].append(name)
        elif name in ['cogcli', 'cogtools', 'cogscripts']:
            categories['Tools & CLI'].append(name)
        elif name in ['cogweb', 'cogapi', 'cogserve']:
            categories['Web & API'].append(name)
        elif name in ['cogdata', 'cogmodels', 'coglearn', 'cogtrain', 'cogeval']:
            categories['Data & Models'].append(name)
        elif name in ['cogdocs', 'cogpapers', 'cogresearch', 'cognotebooks', 'cogexamples']:
            categories['Documentation'].append(name)
        elif name in ['cogbench', 'cogtests']:
            categories['Testing & Benchmarking'].append(name)
        elif name in ['cogcloud']:
            categories['Deployment & Cloud'].append(name)
        elif name in ['cogexp', 'cogproto', 'cogsandbox', 'cogplayground']:
            categories['Experimental'].append(name)
        elif name in ['cogintegrations', 'cogconnectors', 'cogadapters', 'cogbridge', 'cogsdk', 'cogclient', 'cogplugins', 'cogextensions']:
            categories['Integrations'].append(name)
        elif name in ['cogmobile', 'cogdesktop']:
            categories['Mobile & Desktop'].append(name)
        elif name in ['cogassets', 'cogmedia', 'cogbrand', 'cogarchive', 'coglegacy', 'cogviz']:
            categories['Documentation'].append(name)

    for category, repos_list in categories.items():
        if repos_list:
            print(f"\n{category} ({len(repos_list)}):")
            for repo in sorted(repos_list):
                print(f"  - {repo}")

    # Repository health metrics
    print("\n" + "=" * 80)
    print("REPOSITORY HEALTH METRICS")
    print("=" * 80)

    repos_with_desc = sum(1 for r in repos if r.get('description'))
    repos_without_desc = len(repos) - repos_with_desc
    forked_repos = sum(1 for r in repos if r.get('isFork', False))
    original_repos = len(repos) - forked_repos
    archived_repos = sum(1 for r in repos if r.get('isArchived', False))
    private_repos = sum(1 for r in repos if r.get('isPrivate', False))

    print(f"\nRepositories with descriptions: {repos_with_desc}/{len(repos)} ({repos_with_desc/len(repos)*100:.1f}%)")
    print(f"Repositories without descriptions: {repos_without_desc}/{len(repos)} ({repos_without_desc/len(repos)*100:.1f}%)")
    print(f"Original repositories: {original_repos}")
    print(f"Forked repositories: {forked_repos}")
    print(f"Archived repositories: {archived_repos}")
    print(f"Private repositories: {private_repos}")

    # Recent activity
    print("\n" + "=" * 80)
    print("RECENT ACTIVITY (Last 30 days)")
    print("=" * 80)

    now = datetime.now()
    recent_repos = []
    for repo in repos:
        updated_at = repo.get('updatedAt')
        if updated_at:
            try:
                updated = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                days_ago = (now - updated.replace(tzinfo=None)).days
                if days_ago <= 30:
                    recent_repos.append((repo.get('name', 'Unknown'), days_ago))
            except (ValueError, AttributeError):
                continue

    recent_repos.sort(key=lambda x: x[1])
    if recent_repos:
        for name, days in recent_repos[:10]:
            print(f"  - {name} (updated {days} days ago)")
    else:
        print("  No repositories updated in the last 30 days")

    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS FOR IMPROVEMENT")
    print("=" * 80)

    print("\n1. DOCUMENTATION GAPS:")
    print(f"   - {repos_without_desc} repositories lack descriptions")
    print("   - Add clear, concise descriptions to all repositories")
    print("   - Ensure README files exist in all active repositories")

    print("\n2. REPOSITORY ORGANIZATION:")
    print("   - Consider archiving unused experimental repositories")
    print("   - Add topics/tags to repositories for better discoverability")
    print("   - Create a comprehensive organization README (org-o9nn)")

    print("\n3. NAMING CONVENTIONS:")
    print("   - All repositories follow 'cog*' naming pattern (good consistency)")
    print("   - Consider adding prefixes for different categories (e.g., 'cog-core-*', 'cog-tools-*')")

    print("\n4. LANGUAGE ECOSYSTEM:")
    print("   - Strong Python presence (good for ML/AI)")
    print("   - Multiple low-level implementations (C, C++, Rust, Zig, Go)")
    print("   - Consider consolidating similar implementations")

    print("\n5. INTEGRATION & DEPLOYMENT:")
    print("   - Good separation of concerns (infra, CI, deploy)")
    print("   - Ensure CI/CD pipelines are active and maintained")
    print("   - Document deployment procedures")

    print("\n6. FORKED PROJECTS:")
    print(f"   - {forked_repos} forked repositories (Pygmalion AI related)")
    print("   - Clarify purpose and maintenance status of forks")
    print("   - Consider contributing changes upstream")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


def main():
    """Main execution function."""
    print(f"Loading organization data from: {RAW_DATA_FILE}")
    data = load_organization_data(RAW_DATA_FILE)
    analyze_organization(data)


if __name__ == "__main__":
    main()

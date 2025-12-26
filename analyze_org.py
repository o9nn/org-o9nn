import json
import pandas as pd
from datetime import datetime
from collections import defaultdict

# Load the organization data
with open('/home/ubuntu/org-o9nn/org-graph-raw.json', 'r') as f:
    data = json.load(f)

org = data['data']['organization']
repos = org['repositories']['nodes']

# Basic statistics
print("=" * 80)
print("O9NN ORGANIZATION ANALYSIS")
print("=" * 80)
print(f"\nOrganization: {org['name']}")
print(f"Login: {org['login']}")
print(f"URL: {org['url']}")
print(f"Created: {org['createdAt']}")
print(f"Total Repositories: {org['repositories']['totalCount']}")
print(f"Total Members: {org['membersWithRole']['totalCount']}")

# Language distribution
language_counts = defaultdict(int)
for repo in repos:
    if repo['primaryLanguage']:
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

for repo in repos:
    name = repo['name']
    is_fork = repo['isFork']
    
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

repos_with_desc = sum(1 for r in repos if r['description'])
repos_without_desc = len(repos) - repos_with_desc
forked_repos = sum(1 for r in repos if r['isFork'])
original_repos = len(repos) - forked_repos
archived_repos = sum(1 for r in repos if r['isArchived'])
private_repos = sum(1 for r in repos if r['isPrivate'])

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
    updated = datetime.fromisoformat(repo['updatedAt'].replace('Z', '+00:00'))
    days_ago = (now - updated.replace(tzinfo=None)).days
    if days_ago <= 30:
        recent_repos.append((repo['name'], days_ago))

recent_repos.sort(key=lambda x: x[1])
for name, days in recent_repos[:10]:
    print(f"  - {name} (updated {days} days ago)")

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

#!/usr/bin/env python3
"""
O9NN Organization Graph Fetcher
Fetches organization data from GitHub GraphQL API and saves to JSON files.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

# Get script directory for relative paths
SCRIPT_DIR = Path(__file__).parent.resolve()
RAW_OUTPUT_FILE = SCRIPT_DIR / 'org-graph-raw.json'
PROCESSED_OUTPUT_FILE = SCRIPT_DIR / 'org-graph.json'

# GitHub GraphQL API endpoint
GITHUB_API_URL = "https://api.github.com/graphql"

# GraphQL query to fetch organization data
GRAPHQL_QUERY = """
query($orgLogin: String!, $cursor: String) {
  organization(login: $orgLogin) {
    name
    login
    url
    description
    email
    websiteUrl
    createdAt
    updatedAt
    membersWithRole {
      totalCount
    }
    repositories(first: 100, after: $cursor) {
      totalCount
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        description
        url
        createdAt
        updatedAt
        pushedAt
        isPrivate
        isFork
        isArchived
        isTemplate
        primaryLanguage {
          name
          color
        }
        languages(first: 10) {
          nodes {
            name
          }
        }
        stargazerCount
        forkCount
        watchers {
          totalCount
        }
        issues {
          totalCount
        }
        pullRequests {
          totalCount
        }
        defaultBranchRef {
          name
        }
        licenseInfo {
          name
          spdxId
        }
        repositoryTopics(first: 10) {
          nodes {
            topic {
              name
            }
          }
        }
      }
    }
  }
}
"""


def fetch_organization_data(org_login, github_token):
    """
    Fetch organization data from GitHub GraphQL API.
    
    Args:
        org_login: GitHub organization login name
        github_token: GitHub personal access token
        
    Returns:
        Complete organization data dictionary
    """
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }
    
    all_repos = []
    cursor = None
    has_next_page = True
    
    print(f"Fetching organization data for: {org_login}")
    
    while has_next_page:
        variables = {
            "orgLogin": org_login,
            "cursor": cursor
        }
        
        try:
            response = requests.post(
                GITHUB_API_URL,
                headers=headers,
                json={"query": GRAPHQL_QUERY, "variables": variables},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data:
                print(f"GraphQL errors: {data['errors']}")
                sys.exit(1)
            
            org_data = data['data']['organization']
            repos = org_data['repositories']
            
            all_repos.extend(repos['nodes'])
            
            page_info = repos['pageInfo']
            has_next_page = page_info['hasNextPage']
            cursor = page_info['endCursor']
            
            print(f"  Fetched {len(all_repos)} repositories so far...")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from GitHub API: {e}")
            sys.exit(1)
        except KeyError as e:
            print(f"Error parsing response data: {e}")
            sys.exit(1)
    
    # Combine all repositories into final structure
    org_data['repositories']['nodes'] = all_repos
    
    return {"data": {"organization": org_data}}


def process_organization_data(raw_data):
    """
    Process raw organization data into structured format.
    
    Args:
        raw_data: Raw data from GitHub API
        
    Returns:
        Processed organization data dictionary
    """
    org = raw_data['data']['organization']
    repos = org['repositories']['nodes']
    
    # Categorize repositories
    categories = {
        'core_libraries': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'critical',
            'description': 'High-performance implementations of neural network primitives and cognitive computing foundations'
        },
        'infrastructure': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'critical',
            'description': 'DevOps, monitoring, and configuration management'
        },
        'tools_cli': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'medium',
            'description': 'Command-line interfaces and developer tools'
        },
        'web_api': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'high',
            'description': 'Web interfaces and API services'
        },
        'data_models': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'high',
            'description': 'Data processing, model training, and evaluation'
        },
        'documentation': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'high',
            'description': 'Documentation, research papers, and assets'
        },
        'testing_benchmarking': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'critical',
            'description': 'Quality assurance and performance testing'
        },
        'deployment_cloud': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'high',
            'description': 'Cloud deployment and orchestration'
        },
        'experimental': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'low',
            'description': 'Prototypes and experimental features'
        },
        'integrations': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'high',
            'description': 'Third-party integrations and connectors'
        },
        'mobile_desktop': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'medium',
            'description': 'Native applications'
        },
        'forked_projects': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'medium',
            'description': 'PygmalionAI ecosystem integrations'
        },
        'organization': {
            'count': 0,
            'repositories': [],
            'strategic_importance': 'medium',
            'description': 'Organization meta-repository'
        }
    }
    
    # Category mapping
    category_map = {
        'core_libraries': ['cogpy', 'cogplan9', 'cogpilot.jl', 'cognu-mach', 'coglux', 'coglow', 'coggml', 'cogmetal', 'cogwhisper', 'cogllama', 'cogtorch', 'cogllm', 'nnpu'],
        'infrastructure': ['coginfra', 'cogci', 'cogmonitor', 'cogconfig', 'cogdeploy'],
        'tools_cli': ['cogcli', 'cogtools', 'cogscripts'],
        'web_api': ['cogweb', 'cogapi', 'cogserve'],
        'data_models': ['cogdata', 'cogmodels', 'coglearn', 'cogtrain', 'cogeval'],
        'documentation': ['cogdocs', 'cogpapers', 'cogresearch', 'cognotebooks', 'cogexamples', 'cogassets', 'cogmedia', 'cogbrand', 'cogarchive', 'coglegacy', 'cogviz'],
        'testing_benchmarking': ['cogbench', 'cogtests'],
        'deployment_cloud': ['cogcloud'],
        'experimental': ['cogexp', 'cogproto', 'cogsandbox', 'cogplayground'],
        'integrations': ['cogintegrations', 'cogconnectors', 'cogadapters', 'cogbridge', 'cogsdk', 'cogclient', 'cogplugins', 'cogextensions'],
        'mobile_desktop': ['cogmobile', 'cogdesktop'],
        'organization': ['org-o9nn']
    }
    
    # Language distribution
    language_counts = {}
    
    # Categorize and count
    for repo in repos:
        name = repo.get('name', '')
        is_fork = repo.get('isFork', False)
        
        # Count languages
        if repo.get('primaryLanguage'):
            lang = repo['primaryLanguage']['name']
            language_counts[lang] = language_counts.get(lang, 0) + 1
        
        # Categorize
        if is_fork:
            categories['forked_projects']['repositories'].append(name)
            categories['forked_projects']['count'] += 1
        else:
            categorized = False
            for cat_key, repo_list in category_map.items():
                if name in repo_list:
                    categories[cat_key]['repositories'].append(name)
                    categories[cat_key]['count'] += 1
                    categorized = True
                    break
    
    # Calculate health metrics
    repos_with_desc = sum(1 for r in repos if r.get('description'))
    repos_without_desc = len(repos) - repos_with_desc
    original_repos = sum(1 for r in repos if not r.get('isFork', False))
    forked_repos = len(repos) - original_repos
    private_repos = sum(1 for r in repos if r.get('isPrivate', False))
    public_repos = len(repos) - private_repos
    archived_repos = sum(1 for r in repos if r.get('isArchived', False))
    
    # Build processed data structure
    processed_data = {
        'metadata': {
            'organization': org.get('login', ''),
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'total_repositories': len(repos),
            'total_members': org['membersWithRole'].get('totalCount', 0),
            'created_at': org.get('createdAt', '')
        },
        'categories': categories,
        'languages': language_counts,
        'health_metrics': {
            'repositories_with_description': repos_with_desc,
            'repositories_without_description': repos_without_desc,
            'description_coverage_percentage': round(repos_with_desc / len(repos) * 100, 1) if repos else 0,
            'original_repositories': original_repos,
            'forked_repositories': forked_repos,
            'private_repositories': private_repos,
            'public_repositories': public_repos,
            'archived_repositories': archived_repos
        },
        'recommendations': {
            'immediate': [
                f"Add descriptions to all {repos_without_desc} repositories without descriptions",
                "Create README.md files for all repositories",
                "Add GitHub topics to all repositories for discoverability",
                "Establish repository status labels (Active/Maintenance/Experimental/Archived)"
            ],
            'short_term': [
                "Implement CI/CD pipelines across all active repositories",
                "Create centralized documentation website",
                "Establish contribution guidelines and issue templates",
                "Define versioning strategy and release cadence"
            ],
            'medium_term': [
                "Evaluate overlap between cogpy, coggml, cogtorch, cogllm",
                "Conduct comprehensive benchmarking",
                "Build community engagement programs",
                "Develop plugin marketplace"
            ],
            'long_term': [
                "Achieve 1.0 stable releases for core libraries",
                "Establish production-ready deployment tools",
                "Publish academic research papers",
                "Develop enterprise features and commercial support"
            ]
        }
    }
    
    return processed_data


def main():
    """Main execution function."""
    # Get GitHub token from environment
    github_token = os.environ.get('GITHUB_TOKEN') or os.environ.get('magoo')
    
    if not github_token:
        print("Error: GitHub token not found in environment variables")
        print("Please set GITHUB_TOKEN or magoo environment variable")
        sys.exit(1)
    
    org_login = os.environ.get('ORG_LOGIN', 'o9nn')
    
    # Fetch organization data
    raw_data = fetch_organization_data(org_login, github_token)
    
    # Save raw data
    print(f"\nSaving raw data to: {RAW_OUTPUT_FILE}")
    with open(RAW_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, indent=2)
    
    # Process data
    print("Processing organization data...")
    processed_data = process_organization_data(raw_data)
    
    # Save processed data
    print(f"Saving processed data to: {PROCESSED_OUTPUT_FILE}")
    with open(PROCESSED_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2)
    
    print("\n✅ Organization graph updated successfully!")
    print(f"   Total repositories: {processed_data['metadata']['total_repositories']}")
    print(f"   Total members: {processed_data['metadata']['total_members']}")
    print(f"   Description coverage: {processed_data['health_metrics']['description_coverage_percentage']}%")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test cache lookup precision with tag-based matching.

This script simulates cache lookups by:
1. Extracting keywords from test queries
2. Matching against cache entry tags
3. Calculating precision, recall, and F1 metrics
"""

import re
import sys

# Cache entries with their tags
CACHE_ENTRIES = {
    "Entry 1": {
        "name": "proxmox-cloud-init.md",
        "tags": {"proxmox", "cloud-init", "vm-templates", "infrastructure"},
    },
    "Entry 2": {
        "name": "ansible-proxmox-automation.md",
        "tags": {"ansible", "proxmox", "automation", "infrastructure", "iac"},
    },
    "Entry 3": {
        "name": "kubernetes-ceph-storage.md",
        "tags": {"kubernetes", "ceph", "storage", "k8s", "persistent-volumes"},
    },
    "Entry 4": {
        "name": "netbox-dns-integration.md",
        "tags": {"netbox", "powerdns", "dns", "ipam", "automation"},
    },
    "Entry 5": {
        "name": "terraform-proxmox-provider.md",
        "tags": {"terraform", "proxmox", "iac", "vm-provisioning", "infrastructure"},
    },
}

# Test queries with expected matches
TEST_QUERIES = [
    {
        "query": "cloud-init for Proxmox VMs",
        "expected": {"Entry 1"},
        "type": "Direct",
    },
    {
        "query": "Proxmox automation with Ansible",
        "expected": {"Entry 2"},
        "type": "Direct",
    },
    {
        "query": "Ceph storage for K8s",
        "expected": {"Entry 3"},
        "type": "Direct",
    },
    {
        "query": "DNS automation with NetBox",
        "expected": {"Entry 4"},
        "type": "Direct",
    },
    {
        "query": "Terraform infrastructure on Proxmox",
        "expected": {"Entry 5"},
        "type": "Direct",
    },
    {
        "query": "VM templates in Proxmox",
        "expected": {"Entry 1"},
        "type": "Semantic",
    },
    {
        "query": "Infrastructure as Code for virtualization",
        "expected": {"Entry 2", "Entry 5"},  # Both Ansible and Terraform are IaC
        "type": "Semantic",
    },
    {
        "query": "Container storage solutions",
        "expected": {"Entry 3"},
        "type": "Semantic",
    },
    {
        "query": "IPAM and DNS management",
        "expected": {"Entry 4"},
        "type": "Semantic",
    },
    {
        "query": "Homelab automation",
        "expected": {"Entry 2", "Entry 4"},  # Multiple valid matches
        "type": "Broad",
    },
]


def extract_keywords(query: str) -> set[str]:
    """
    Extract keywords from query by:
    1. Converting to lowercase
    2. Splitting on whitespace and hyphens
    3. Removing common stop words
    4. Normalizing synonyms
    """
    # Stop words to ignore
    stop_words = {"for", "with", "in", "on", "and", "the", "a", "an", "to", "of"}

    # Synonym mapping to normalize terms
    synonyms = {
        "vms": "vm",
        "k8s": "kubernetes",
        "infra": "infrastructure",
        "virtualization": "vm",
        "container": "kubernetes",
        "containers": "kubernetes",
    }

    # Extract words
    words = re.findall(r"[a-z0-9]+", query.lower())

    # Filter and normalize
    keywords = set()
    for word in words:
        if word not in stop_words:
            # Apply synonym mapping
            normalized = synonyms.get(word, word)
            keywords.add(normalized)

    return keywords


def cache_lookup(query: str, threshold: float = 0.3) -> set[str]:
    """
    Perform cache lookup using tag-based matching with scoring.

    Returns entries ranked by match quality.
    threshold: minimum ratio of matching tags (overlap / total_tags)
    """
    keywords = extract_keywords(query)
    scores = []

    for entry_id, entry_data in CACHE_ENTRIES.items():
        tags = entry_data["tags"]

        # Calculate overlap
        overlap = keywords & tags

        if overlap:
            # Calculate match score based on:
            # 1. Number of matching tags
            # 2. Ratio of matched tags to total tags
            # 3. Ratio of matched keywords to total keywords
            tag_ratio = len(overlap) / len(tags) if tags else 0
            keyword_ratio = len(overlap) / len(keywords) if keywords else 0

            # Combined score favors entries with more specific matches
            score = (tag_ratio * 0.6) + (keyword_ratio * 0.4)

            scores.append((entry_id, score, len(overlap)))

    # Sort by score (highest first), then by overlap count
    scores.sort(key=lambda x: (x[1], x[2]), reverse=True)

    # Return entries above threshold
    matches = set()
    for entry_id, score, overlap_count in scores:
        if score >= threshold or overlap_count >= 2:
            matches.add(entry_id)

    return matches


def evaluate_results() -> dict:
    """Run all test queries and calculate metrics."""
    results = []
    total_tp = 0
    total_fp = 0
    total_fn = 0

    print("=" * 80)
    print("CACHE LOOKUP PRECISION TEST")
    print("=" * 80)
    print()

    for i, test in enumerate(TEST_QUERIES, 1):
        query = test["query"]
        expected = test["expected"]
        query_type = test["type"]

        # Perform lookup
        found = cache_lookup(query)

        # Calculate TP, FP, FN for this query
        tp = len(found & expected)  # True positives
        fp = len(found - expected)  # False positives
        fn = len(expected - found)  # False negatives

        total_tp += tp
        total_fp += fp
        total_fn += fn

        # Determine result status
        if found == expected:
            status = "PERFECT"
        elif found & expected:  # Some overlap
            status = "PARTIAL"
        else:
            status = "MISS"

        # Store result
        result = {
            "query": query,
            "expected": expected,
            "found": found,
            "type": query_type,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "status": status,
        }
        results.append(result)

        # Print result
        print(f"Q{i}: {query}")
        print(f"    Type: {query_type}")
        print(f"    Expected: {sorted(expected)}")
        print(f"    Found:    {sorted(found)}")
        print(f"    Status:   {status} (TP={tp}, FP={fp}, FN={fn})")
        print()

    # Calculate overall metrics
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Summary
    print("=" * 80)
    print("METRICS SUMMARY")
    print("=" * 80)
    print(f"True Positives:  {total_tp}")
    print(f"False Positives: {total_fp}")
    print(f"False Negatives: {total_fn}")
    print()
    print(f"Precision: {precision:.1%} (TP / (TP + FP))")
    print(f"Recall:    {recall:.1%} (TP / (TP + FN))")
    print(f"F1 Score:  {f1:.1%}")
    print()

    # Go/No-Go decision
    threshold = 0.70
    decision = "PASS" if precision >= threshold else "FAIL"
    print(f"Go/No-Go Decision: {decision} (threshold: {threshold:.0%})")
    print("=" * 80)

    return {
        "results": results,
        "metrics": {
            "tp": total_tp,
            "fp": total_fp,
            "fn": total_fn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        },
        "decision": decision,
    }


if __name__ == "__main__":
    evaluation = evaluate_results()
    sys.exit(0 if evaluation["decision"] == "PASS" else 1)

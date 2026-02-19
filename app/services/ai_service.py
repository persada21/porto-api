"""
AI Service for GitHub Profile Analysis
"""
import random
import re
from collections import defaultdict
from typing import List, Dict, Optional

class AIService:
    """Service for AI-powered analysis and generation"""

    def analyze_persona(self, events: List[Dict]) -> Dict:
        """
        Analyze commit messages to determine developer persona
        """
        commits = self._extract_commits(events)

        if not commits:
            return {
                "persona": "The Ghost",
                "vibe": "Mysterious and silent. No recent activity detected.",
                "traits": ["Invisible", "Quiet"],
                "commit_distribution": {}
            }

        # Categorize commits
        categories = defaultdict(int)

        patterns = {
            "feat": r"^(feat|add|new|implement|create)",
            "fix": r"^(fix|bug|resolve|patch|hotfix)",
            "docs": r"^(docs|doc|readme|comment)",
            "refactor": r"^(refactor|clean|improve|optimize|structure)",
            "test": r"^(test|spec|coverage)",
            "chore": r"^(chore|ci|build|config|update|upgrade)"
        }

        for commit in commits:
            msg = commit.lower()
            categorized = False
            for cat, pattern in patterns.items():
                if re.search(pattern, msg):
                    categories[cat] += 1
                    categorized = True
                    break
            if not categorized:
                categories["other"] += 1

        # Determine persona
        total_commits = len(commits)
        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        top_cat = sorted_cats[0][0] if sorted_cats else "other"

        persona_map = {
            "feat": ("The Creator", "Always building something new. A true innovator."),
            "fix": ("The Maintainer", "Keeping the digital world bug-free. The hero we need."),
            "docs": ("The Scribe", "Believes that code without documentation is just noise."),
            "refactor": ("The Architect", "Pursuing the perfect code structure. Elegant and efficient."),
            "test": ("The Guardian", "Safety first. Nothing breaks on your watch."),
            "chore": ("The Automator", "Configuration master. Keeping the pipelines green."),
            "other": ("The Wildcard", "Unpredictable and versatile. You code by your own rules.")
        }

        persona, vibe = persona_map.get(top_cat, persona_map["other"])

        # Calculate traits
        traits = []
        if total_commits > 20:
            traits.append("Prolific")
        if categories.get("fix", 0) > categories.get("feat", 0):
            traits.append("Detail-oriented")
        if categories.get("test", 0) > 0:
            traits.append("Cautious")
        if categories.get("refactor", 0) > 0:
            traits.append("Perfectionist")
        if not traits:
            traits.append("Balanced")

        return {
            "persona": persona,
            "vibe": vibe,
            "traits": traits,
            "commit_distribution": dict(categories)
        }

    def generate_commit_message(self, events: List[Dict]) -> str:
        """
        Generate a commit message using Markov Chain based on recent commits
        """
        commits = self._extract_commits(events)

        if len(commits) < 5:
            return "feat: building something awesome (not enough data to mock you)"

        # simple bigram model
        words = []
        for commit in commits:
            # simple tokenization
            tokens = re.findall(r"[\w']+|[.,!?;]", commit.lower())
            words.extend(tokens)

        if not words:
            return "feat: initial commit"

        chain = defaultdict(list)
        for i in range(len(words) - 1):
            chain[words[i]].append(words[i+1])

        # Generate
        # Start with a word that appeared at start of a commit if possible?
        # Simpler: just pick random from keys
        if not chain:
             return "feat: magic happens here"

        start_word = random.choice(list(chain.keys()))
        current_word = start_word
        message = [current_word]

        # Generate up to 10 words or until dead end
        for _ in range(10):
            next_words = chain.get(current_word)
            if not next_words:
                break
            next_word = random.choice(next_words)
            message.append(next_word)
            current_word = next_word

        return " ".join(message)

    def _extract_commits(self, events: List[Dict]) -> List[str]:
        """Helper to extract commit messages from PushEvents"""
        commits = []
        for event in events:
            if event.get("type") == "PushEvent":
                payload = event.get("payload", {})
                event_commits = payload.get("commits", [])
                for commit in event_commits:
                    commits.append(commit.get("message", ""))
        return commits

ai_service = AIService()

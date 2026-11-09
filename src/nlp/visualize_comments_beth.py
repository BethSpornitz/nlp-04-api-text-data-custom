"""visualize_comments_beth.py.

Author: Beth Spornitz
Date: 2026-11

Purpose:
    Visualize the distribution of word counts in
    the processed JSONPlaceholder comments dataset.
"""

from collections import Counter
from pathlib import Path
import re

import matplotlib.pyplot as plt
import polars as pl


def main() -> None:
    """Create and save a comment word-count distribution chart."""
    input_path = Path("data/processed/beth_comments_processed.csv")
    output_path = Path("docs/images/comment_word_counts.png")

    # Read the processed comments produced by the EVTL pipeline.
    df = pl.read_csv(input_path)

    # Count how many comments have each word count.
    distribution = df.group_by("body_word_count").len().sort("body_word_count")

    # Create a bar chart using actual calculated frequencies.
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        distribution["body_word_count"].to_list(),
        distribution["len"].to_list(),
    )

    ax.set_title("Distribution of Comment Word Counts")
    ax.set_xlabel("Words per Comment")
    ax.set_ylabel("Number of Comments")
    ax.set_xticks(distribution["body_word_count"].to_list())

    fig.tight_layout()

    # Save the image for the documentation website.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    # ============================================================
    # ADDITIONAL NLP ANALYSIS: MOST FREQUENT WORDS
    # ============================================================

    # Small stopword list to remove common function words.
    stopwords = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "but",
        "by",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "their",
        "this",
        "to",
        "was",
        "were",
        "with",
        "you",
        "your",
        "i",
        "me",
        "my",
        "we",
        "our",
        "they",
        "them",
        "he",
        "she",
        "his",
        "her",
        "not",
    }

    # Lowercase and tokenize the comment bodies.
    all_words = []

    for body in df["body"].to_list():
        words = re.findall(r"[a-z]+", body.lower())
        all_words.extend(
            word for word in words if word not in stopwords and len(word) > 2
        )

    # Count the 15 most frequent remaining words.
    word_counts = Counter(all_words)
    top_words = word_counts.most_common(15)

    # Display the actual results in the terminal.
    print("\nTop 15 words after preprocessing:")
    for word, count in top_words:
        print(f"{word}: {count}")

    # Create a second visualization.
    words = [word for word, count in top_words]
    counts = [count for word, count in top_words]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(words[::-1], counts[::-1])

    ax.set_title("Top 15 Tokens in Synthetic Comments")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Word")

    fig.tight_layout()

    word_chart_path = Path("docs/images/comment_top_words.png")
    fig.savefig(word_chart_path, dpi=150)
    plt.close(fig)

    print(f"Word frequency chart saved to: {word_chart_path}")

    print(f"Comments analyzed: {df.height}")
    print(f"Chart saved to: {output_path}")


if __name__ == "__main__":
    main()

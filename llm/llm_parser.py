"""
LLM output parser

Extracts sentiment score from model output.
"""

import re


def parse_sentiment_score(text):

    match = re.search(

        r"-?\d+\.?\d*",

        text

    )

    if match:

        value = float(

            match.group()

        )

        return max(

            min(value, 1),

            -1

        )

    return 0
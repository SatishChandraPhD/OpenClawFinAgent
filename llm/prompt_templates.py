"""
LLM Prompt Templates

Defines structured prompts for financial sentiment reasoning.

Compatible with FREF-style evaluation:
robust reasoning rather than keyword sentiment.
"""


def build_sentiment_prompt(symbol, headlines):

    headlines_text = "\n".join(

        [f"- {h}" for h in headlines]

    )


    prompt = f"""
You are a financial analyst.

Analyze the sentiment of the following news headlines for stock {symbol}.

Focus on:

earnings outlook
growth prospects
risk exposure
macroeconomic impact
management quality
competitive position

Headlines:

{headlines_text}


Return ONLY a number between -1 and 1:

1 = very positive
0 = neutral
-1 = very negative


Example outputs:

0.7
-0.4
0.0


Sentiment score:
"""


    return prompt
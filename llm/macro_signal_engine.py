"""
Macro LLM Signal Engine

Generates macroeconomic sentiment signal
from global financial news.
"""

import datetime as dt
import urllib.parse
import feedparser

from llm.prompt_templates import build_sentiment_prompt
from llm.llm_parser import parse_sentiment_score

from transformers import AutoTokenizer, AutoModelForCausalLM

import torch


class MacroSignalEngine:

    def __init__(self, config):

        self.config = config
        self.model = None
        self.tokenizer = None


    # =========================
    # FETCH MACRO NEWS
    # =========================

    def fetch_macro_news(self):

        queries = [

            "stock market outlook",

            "interest rates Federal Reserve",

            "inflation outlook",

            "oil price forecast",

            "global recession risk",

            "geopolitical risk markets"

        ]

        headlines = []

        for q in queries:

            encoded_query = urllib.parse.quote(q)

            url = (

                "https://news.google.com/rss/search?q="
                f"{encoded_query}&hl=en-US&gl=US&ceid=US:en"

            )

            feed = feedparser.parse(url)

            for entry in feed.entries[:2]:

                headlines.append(entry.title)

        return headlines[: self.config["MAX_NEWS_ITEMS"]]


    # =========================
    # LOAD MODEL
    # =========================

    def load_model(self):

        if self.model is not None:

            return


        print("Loading macro reasoning model...")


        model_name = "Qwen/Qwen2.5-0.5B-Instruct"


        self.tokenizer = AutoTokenizer.from_pretrained(

            model_name

        )


        self.model = AutoModelForCausalLM.from_pretrained(

            model_name,

            torch_dtype=torch.float32

        )


        print("Macro LLM ready")


    # =========================
    # GENERATE SIGNAL
    # =========================

    def generate_signal(self):

        if not self.config["ENABLE_LLM"]:

            return {

                "macro_score": 0,

                "confidence": 0,

                "headline_count": 0,

                "timestamp": dt.datetime.utcnow().isoformat(),

                "headlines": []

            }


        headlines = self.fetch_macro_news()


        if len(headlines) == 0:

            return {

                "macro_score": 0,

                "confidence": 0,

                "headline_count": 0,

                "timestamp": dt.datetime.utcnow().isoformat(),

                "headlines": []

            }


        self.load_model()


        prompt = build_sentiment_prompt(

            "GLOBAL_MARKETS",

            headlines

        )


        inputs = self.tokenizer(

            prompt,

            return_tensors="pt",

            truncation=True,

            max_length=512

        )


        with torch.no_grad():

            output = self.model.generate(

                **inputs,

                max_new_tokens=20

            )


        text = self.tokenizer.decode(

            output[0],

            skip_special_tokens=True

        )


        value = parse_sentiment_score(text)


        confidence = min(

            abs(value),

            0.8

        )


        return {

            "macro_score": float(value),

            "confidence": float(confidence),

            "headline_count": len(headlines),

            "timestamp": dt.datetime.utcnow().isoformat(),

            "headlines": headlines

        }
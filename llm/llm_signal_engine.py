"""
LLM Signal Engine

Fetches financial news and generates sentiment score
using Qwen reasoning model.
"""

import datetime as dt

import feedparser

import torch

from transformers import AutoTokenizer, AutoModelForCausalLM

from llm.prompt_templates import build_sentiment_prompt

from llm.llm_parser import parse_sentiment_score


class LLMSignalEngine:

    def __init__(self, config):

        self.config = config

        self.model = None

        self.tokenizer = None


    # =============================
    # NEWS FETCHER
    # =============================

    def fetch_news(self, symbol):

        url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(url)

        headlines = []

        for entry in feed.entries[: self.config["MAX_NEWS_ITEMS"]]:

            headlines.append(entry.title)

        return headlines


    # =============================
    # LOAD MODEL
    # =============================

    def load_model(self):

        if self.model is not None:

            return


        print("Loading Qwen reasoning model...")


        model_name = "Qwen/Qwen2.5-0.5B-Instruct"


        self.tokenizer = AutoTokenizer.from_pretrained(

            model_name

        )


        self.model = AutoModelForCausalLM.from_pretrained(

            model_name,

            torch_dtype=torch.float32

        )


        print("LLM ready")


    # =============================
    # GENERATE SENTIMENT
    # =============================

    def generate_signal(self, symbol):

        if not self.config["ENABLE_LLM"]:

            return {

                "symbol": symbol,

                "sentiment_score": 0,

                "confidence": 0,

                "headline_count": 0,

                "timestamp": dt.datetime.utcnow().isoformat(),

                "headlines": []

            }


        headlines = self.fetch_news(symbol)


        if len(headlines) == 0:

            return {

                "symbol": symbol,

                "sentiment_score": 0,

                "confidence": 0,

                "headline_count": 0,

                "timestamp": dt.datetime.utcnow().isoformat(),

                "headlines": []

            }


        self.load_model()


        prompt = build_sentiment_prompt(

            symbol,

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

            "symbol": symbol,

            "sentiment_score": float(value),

            "confidence": float(confidence),

            "headline_count": len(headlines),

            "timestamp": dt.datetime.utcnow().isoformat(),

            "headlines": headlines

        }
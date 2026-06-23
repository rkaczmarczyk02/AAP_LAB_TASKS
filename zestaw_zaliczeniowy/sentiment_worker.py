
import re
import multiprocessing as mp

POS_WORDS = {
    "good", "great", "excellent", "wonderful", "love",
    "best", "amazing", "brilliant", "perfect"
}

NEG_WORDS = {
    "bad", "worst", "awful", "terrible", "hate",
    "boring", "waste", "poor", "horrible"
}

def sentiment_score(text: str) -> int:
    words = re.findall(r"\b\w+\b", text.lower())
    positive = sum(word in POS_WORDS for word in words)
    negative = sum(word in NEG_WORDS for word in words)
    return positive - negative

def multiprocessing_scores(texts, workers: int, chunksize: int = 100):
    context = mp.get_context("spawn")
    with context.Pool(processes=workers) as pool:
        return pool.map(sentiment_score, texts, chunksize=chunksize)

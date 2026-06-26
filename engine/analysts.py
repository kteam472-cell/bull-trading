import json

PROMPT = ("You are a technical analyst. Given these computed indicators, return "
          'STRICT JSON {{"stance": "bullish|bearish|neutral", "note": "<=20 words"}}. '
          "Reason only from the numbers. Indicators: {card}")

def annotate(card, llm):
    try:
        raw = llm(PROMPT.format(card=json.dumps({k: card[k] for k in card})))
        advice = json.loads(raw)
        advice = {"stance": str(advice.get("stance", "neutral")),
                  "note": str(advice.get("note", ""))[:200]}
    except Exception:
        advice = {"stance": "neutral", "note": "llm unavailable"}
    card["advice"] = advice
    return card

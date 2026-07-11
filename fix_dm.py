import os
DM = {
    "Artificial Intelligence (AI)": {"Machine Learning": "machine learning", "LLMs": "LLM OR GPT", "Robotics": "robotics"},
    "Technology": {"Software": "software OR apps", "Internet": "internet trends"},
    "Sports": {"Cricket": "cricket OR IPL", "Football": "football OR soccer", "NBA": "basketball OR NBA"},
    "Business": {"Startups": "startups OR founders", "Venture Capital": "venture capital"},
    "Finance": {"Stocks": "stock market", "Banking": "banking"},
    "Health": {"Medical": "medical research", "Fitness": "fitness"},
    "Science": {"Space": "NASA OR SpaceX", "Physics": "physics"},
    "Cybersecurity": {"Breaches": "data breach", "Malware": "malware"},
    "Gaming": {"PC/Console": "xbox OR playstation", "Mobile": "mobile games"},
    "Crypto": {"Bitcoin": "bitcoin OR ethereum", "Web3": "web3 OR NFTs"},
    "Entertainment": {"Movies": "movies OR netflix", "Music": "music"},
    "World News": {"Elections": "elections", "Geopolitics": "geopolitics"},
    "Education": {"Universities": "universities OR college", "EdTech": "online courses OR edtech"},
    "Travel": {"Destinations": "travel destinations", "Airlines": "airlines"},
    "Food": {"Recipes": "recipes OR cooking", "Trends": "food trends"},
    "Automobiles": {"EVs": "tesla OR electric vehicles", "Launches": "new cars"},
    "War & Conflicts": {"Conflicts": "war OR military", "Defense": "defense technology"},
    "Environment": {"Warming": "global warming", "Energy": "solar OR wind energy"},
    "Social Media": {"TikTok/IG": "tiktok OR instagram", "X/Twitter": "X platform OR twitter"}
}
parts = []
for d, subs in DM.items():
    sub_strs = []
    for s, q in subs.items():
        sub_strs.append(chr(34) + s + chr(34) + ":" + chr(34) + q + chr(34)
    parts.append(chr(34) + d + chr(34) + ":{" + ",".join(sub_strs) + "}")
dm_js = "var DM={" + ",".join(parts) + ";"
with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()
bad = "var DM=.*?;"
import re
match = re.search(bad, content, re.DOTALL)
if match:
    content = content[:match.start()] + dm_js + content[match.end():]
else:
    print("ERROR")
    exit()
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED")

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
q = chr(39)
dm_parts = []
for d, subs in DM.items():
    sub_parts = []
    for s, query in subs.items():
        sub_parts.append(q + s + q + ":" + q + query + q)
    dm_parts.append(q + d + q + ":{" + ",".join(sub_parts) + "}")
dm_js = "var DM={" + ",".join(dm_parts) + ";"
h = open("templates/index.html", "r", encoding="utf-8").read()
h = h.replace("var DM=.*?;", dm_js)
open("templates/index.html", "w", encoding="utf-8").write(h)
print("FIXED - sidebar will show domains now")

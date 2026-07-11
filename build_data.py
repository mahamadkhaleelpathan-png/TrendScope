import json
DM = {
    "Artificial Intelligence (AI)": {"Machine Learning": "machine learning", "LLMs & GPT": "LLM OR GPT", "Robotics": "robotics", "Computer Vision": "computer vision", "Generative AI": "generative AI", "AI Ethics": "AI ethics OR bias"},
    "Technology": {"Software & Apps": "software OR apps", "Internet Trends": "internet trends", "Cloud Computing": "cloud computing OR AWS OR Azure", "Semiconductors": "chips OR semiconductors", "5G & 6G": "5G OR 6G technology"},
    "Sports": {"Cricket": "cricket OR IPL", "Football/Soccer": "football OR soccer", "NBA & Basketball": "basketball OR NBA", "Tennis": "tennis", "Formula 1": "formula 1 OR F1", "Esports": "esports"},
    "Business": {"Startups": "startups OR founders", "Venture Capital": "venture capital", "Layoffs & Jobs": "layoffs OR hiring", "Mergers & Acquisitions": "mergers OR acquisitions", "Remote Work": "remote work"},
    "Finance": {"Stock Market": "stock market", "Banking": "banking", "FinTech": "fintech", "Interest Rates": "interest rates OR RBI", "Real Estate": "real estate"},
    "Health": {"Medical Research": "medical research", "Fitness": "fitness", "Mental Health": "mental health", "Pharma & Drugs": "pharmaceuticals OR new drugs", "Healthcare Tech": "healthcare technology"},
    "Science": {"Space (NASA/SpaceX)": "NASA OR SpaceX", "Physics": "physics", "Biology": "biology OR genetics", "Climate Science": "climate science", "Archaeology": "archaeology"},
    "Cybersecurity": {"Data Breaches": "data breach", "Malware & Ransomware": "malware OR ransomware", "AI in Security": "AI cybersecurity", "Privacy Laws": "privacy laws OR GDPR"},
    "Gaming": {"PC & Console": "xbox OR playstation OR PC gaming", "Mobile Games": "mobile games", "Game Dev": "game development OR Unreal Engine", "VR/AR Gaming": "virtual reality gaming"},
    "Crypto": {"Bitcoin & Ethereum": "bitcoin OR ethereum", "Web3 & NFTs": "web3 OR NFTs", "DeFi": "decentralized finance", "Crypto Regulations": "crypto regulations OR SEC crypto"},
    "Entertainment": {"Movies & Netflix": "movies OR netflix", "Music": "music industry", "Streaming Wars": "streaming wars OR Disney+", "Celebrities": "celebrities OR pop culture", "Anime & K-Pop": "anime OR K-pop"},
    "World News": {"Elections": "elections", "Geopolitics": "geopolitics", "UN & Summits": "United Nations OR global summit", "Protests": "protests OR strikes"},
    "Education": {"Universities": "universities OR college", "EdTech": "online courses OR edtech", "AI in Education": "AI in education", "Exams & Results": "exams OR competitive tests"},
    "Travel": {"Destinations": "travel destinations", "Airlines": "airlines", "Budget Travel": "budget travel", "Luxury Travel": "luxury travel"},
    "Food": {"Recipes & Cooking": "recipes OR cooking", "Food Trends": "food trends", "Restaurants": "restaurants OR fine dining", "Sustainability": "sustainable food"},
    "Automobiles": {"EVs & Tesla": "tesla OR electric vehicles", "New Car Launches": "new car launches", "Self-Driving": "autonomous OR self-driving cars", "Auto Market": "automobile market"},
    "War & Conflicts": {"Global Conflicts": "war OR military conflict", "Defense Tech": "defense technology", "NATO & Alliances": "NATO OR military alliances"},
    "Environment": {"Global Warming": "global warming", "Green Energy": "solar OR wind energy", "Conservation": "wildlife conservation", "Extreme Weather": "extreme weather OR climate disaster"},
    "Social Media": {"TikTok & Instagram": "tiktok OR instagram", "X (Twitter)": "X platform OR twitter", "YouTube": "YouTube trends", "Influencers": "influencers OR creators"}
}
DI = {
    "Artificial Intelligence (AI)": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop",
    "Technology": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=400&fit=crop",
    "Sports": "https://images.unsplash.com/photo-1461896836934-bd45ea8ba7e2?w=800&h=400&fit=crop",
    "Business": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop",
    "Finance": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop",
    "Health": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&h=400&fit=crop",
    "Science": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800&h=400&fit=crop",
    "Cybersecurity": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&h=400&fit=crop",
    "Gaming": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&h=400&fit=crop",
    "Crypto": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=800&h=400&fit=crop",
    "Entertainment": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&h=400&fit=crop",
    "World News": "https://images.unsplash.com/photo-1504711434969-e33886168d6c?w=800&h=400&fit=crop",
    "Education": "https://images.unsplash.com/photo-1523050854058-8df90110c476?w=800&h=400&fit=crop",
    "Travel": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&h=400&fit=crop",
    "Food": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&h=400&fit=crop",
    "Automobiles": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&h=400&fit=crop",
    "War & Conflicts": "https://images.unsplash.com/photo-1543342574-701859b23c8c?w=800&h=400&fit=crop",
    "Environment": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=400&fit=crop",
    "Social Media": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&h=400&fit=crop"
}
open("_data.json", "w", encoding="utf-8").write(json.dumps({"dm": DM, "di": DI}))
print("Data file written: " + str(len(DM)) + " domains")

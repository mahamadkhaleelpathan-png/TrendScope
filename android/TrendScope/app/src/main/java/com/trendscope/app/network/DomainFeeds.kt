package com.trendscope.app.network

object DomainFeeds {
    val FEEDS: Map<String, List<String>> = linkedMapOf(
        "Top News" to listOf(
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "https://feeds.npr.org/1001/rss.xml",
        ),
        "AI" to listOf(
            "https://blog.google/technology/ai/rss/",
            "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        ),
        "Technology" to listOf(
            "https://feeds.arstechnica.com/arstechnica/index",
            "https://www.theverge.com/rss/index.xml",
            "https://www.zdnet.com/news/rss.xml",
            "https://www.wired.com/feed/rss",
        ),
        "Business" to listOf(
            "https://feeds.bbci.co.uk/news/business/rss.xml",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://feeds.marketwatch.com/marketwatch/topstories",
        ),
        "World News" to listOf(
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "https://www.aljazeera.com/xml/rss/all.xml",
        ),
        "Politics" to listOf(
            "https://feeds.bbci.co.uk/news/politics/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        ),
        "Health" to listOf(
            "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
            "https://khn.org/feed/",
            "https://www.who.int/feeds/entity/emergencies/news/en/rss.xml",
        ),
        "Science" to listOf(
            "https://www.sciencedaily.com/rss/all.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
            "https://www.nature.com/nature.rss",
        ),
        "Sports" to listOf(
            "https://www.espn.com/espn/rss/news",
            "https://feeds.bbci.co.uk/sport/rss.xml",
        ),
        "Entertainment" to listOf(
            "https://variety.com/feed/",
            "https://www.hollywoodreporter.com/feed/",
        ),
        "Finance" to listOf(
            "https://feeds.content.dowjones.io/public/rss/mw_topstories",
            "https://finance.yahoo.com/news/rssindex",
        ),
        "Education" to listOf(
            "https://rss.nytimes.com/services/xml/rss/nyt/Education.xml",
            "https://www.edsurge.com/feed.rss",
        ),
        "Cybersecurity" to listOf(
            "https://feeds.feedburner.com/TheHackersNews",
            "https://krebsonsecurity.com/feed/",
        ),
        "Gaming" to listOf(
            "https://www.polygon.com/rss/index.xml",
            "https://www.pcgamer.com/rss/",
        ),
        "Mobile & Gadgets" to listOf(
            "https://www.techradar.com/rss",
            "https://www.gsmarena.com/rss-news-reviews.php3",
        ),
        "Crypto" to listOf(
            "https://cointelegraph.com/rss",
            "https://coinrivet.com/feed/",
        ),
        "Environment" to listOf(
            "https://feeds.npr.org/1025/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml",
        ),
        "Travel" to listOf(
            "https://www.rss-bridge.org/bridge01/?action=display&bridge=Nytimes&feed=travel",
            "https://www.thetravel.com/feed/",
        ),
        "Food" to listOf(
            "https://www.seriouseats.com/rss/all",
            "https://www.bonappetit.com/feed/rss",
        ),
        "Automobiles" to listOf(
            "https://www.autoblog.com/rss.xml",
            "https://www.caranddriver.com/rss/all.xml",
        ),
        "Defense" to listOf(
            "https://www.defenseone.com/rss/",
            "https://www.twz.com/rss",
        ),
        "Social Media" to listOf(
            "https://socialmediaexplorer.com/feed/",
            "https://www.socialmediatoday.com/rss/trending",
        ),
        "Real Estate" to listOf(
            "https://www.inman.com/feed/",
            "https://www.housingwire.com/feed/",
        ),
        "Music" to listOf(
            "https://www.rollingstone.com/music/feed/",
            "https://pitchfork.com/feed/feed-news/rss",
        ),
        "Art & Design" to listOf(
            "https://www.artnews.com/feed/",
            "https://www.dezeen.com/feed/",
        ),
        "India" to listOf(
            "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
            "https://www.thehindu.com/news/national/feeder/default.rss",
        ),
        "Movies" to listOf(
            "https://variety.com/feed/",
            "https://deadline.com/feed/",
        ),
        "Startups" to listOf(
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/startups/index.xml",
        ),
        "Space" to listOf(
            "https://www.space.com/feeds/all.xml",
            "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        ),
    )

    val CATEGORY_EMOJI: Map<String, String> = mapOf(
        "Top News" to "\uD83D\uDD25",
        "AI" to "\uD83E\uDD16",
        "Technology" to "\uD83D\uDCBB",
        "Business" to "\uD83D\uDCBC",
        "Finance" to "\uD83D\uDCCA",
        "Health" to "\uD83C\uDFE5",
        "Education" to "\uD83D\uDCDA",
        "Entertainment" to "\uD83C\uDFAC",
        "Sports" to "\u26BD",
        "World News" to "\uD83C\uDF0D",
        "Science" to "\uD83D\uDD2C",
        "Cybersecurity" to "\uD83D\uDD12",
        "Gaming" to "\uD83C\uDFAE",
        "Mobile & Gadgets" to "\uD83D\uDCF1",
        "Crypto" to "\u20BF",
        "Environment" to "\uD83C\uDF3F",
        "Travel" to "\u2708\uFE0F",
        "Food" to "\uD83C\uDF7D\uFE0F",
        "Automobiles" to "\uD83D\uDE97",
        "Defense" to "\uD83D\uDEE1\uFE0F",
        "Social Media" to "\uD83D\uDCAC",
        "Politics" to "\uD83C\uDFDB\uFE0F",
        "Real Estate" to "\uD83C\uDFE0",
        "Music" to "\uD83C\uDFB5",
        "Art & Design" to "\uD83C\uDFA8",
        "India" to "\uD83C\uDDEE\uD83C\uDDF3",
        "Movies" to "\uD83C\uDFAC",
        "Startups" to "\uD83D\uDE80",
        "Space" to "\uD83D\uDE80",
    )

    fun getCategoryEmoji(category: String): String = CATEGORY_EMOJI[category] ?: ""

    fun getFaviconUrl(domain: String): String = "https://www.google.com/s2/favicons?domain=$domain&sz=64"

    fun getAllCategories(): List<String> = FEEDS.keys.toList()

    fun getFeedsForCategory(category: String): List<String> = FEEDS[category] ?: emptyList()
}

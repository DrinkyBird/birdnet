<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
    <channel>
        <title>Community Goals</title>
        <link>https://elite.drinkybird.net/goals</link>
        <description>Your galaxy in focus</description>
        <language>{$language|get_rss_language}</language>
        {foreach $active as $row}
            <item>
                <title>{$row->title|htmlspecialchars:ENT_XML1}</title>
                <link>https://elite.drinkybird.net/goals/{$row->id}</link>
                <guid isPermaLink="false">{$row->id}</guid>
                <pubDate>{$row->first_seen|date_format:"D, d M Y H:i:s O"}</pubDate>
                <description><![CDATA[{$row->bulletin|generate_extract}]]></description>
                <content:encoded><![CDATA[{$row->bulletin|format_text}]]></content:encoded>
            </item>
        {/foreach}
    </channel>
</rss>

<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
    <channel>
        <title>GalNet News</title>
        <link>https://elite.drinkybird.net</link>
        <description>Your galaxy in focus</description>
        <language>{$language|get_rss_language}</language>
        {foreach $rows as $row}
            <item>
                <title>{$row->title|htmlspecialchars:ENT_XML1}</title>
                <link>https://elite.drinkybird.net/?guid={$row->guid}</link>
                <guid isPermaLink="false">{$row->guid}</guid>
                <pubDate>{$row->date|date_format:"D, d M Y H:i:s O"}</pubDate>
                <description><![CDATA[{$row->text|generate_extract}]]></description>
                <content:encoded><![CDATA[{$row->text|format_text}]]></content:encoded>
                <image>
                    <url>https://hosting.zaonce.net/elite-dangerous/galnet/{$row|get_image}.png</url>
                    <link>https://elite.drinkybird.net/?guid={$row->guid}</link>
                    <title>{$row->title|htmlspecialchars:ENT_XML1}</title>
                </image>
            </item>
        {/foreach}
    </channel>
</rss>

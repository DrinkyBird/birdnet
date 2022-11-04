<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
    <channel>
        <title>Store</title>
        <link>https://elite.drinkybird.net/store</link>
        <description>Elite Dangerous Arx store items</description>
        <language>en-GB</language>
        {foreach $rows as $row}
            <item>
                <title>{$row->title|htmlspecialchars:ENT_XML1}</title>
                <link>https://elite.drinkybird.net/store/{$row->sku}</link>
                <guid isPermaLink="false">{$row->sku}</guid>
                <pubDate>{$row->first_seen|date_format:"D, d M Y H:i:s O"}</pubDate>
                <description><![CDATA[{$row->short_description|generate_extract}]]></description>
                <content:encoded><![CDATA[{$row->short_description}]]></content:encoded>
                <image>
                    <url>https://dlc.elitedangerous.com/images/med/{$row->image|escape}</url>
                    <link>https://elite.drinkybird.net/store/{$row->sku}</link>
                    <title>{$row->title|htmlspecialchars:ENT_XML1}</title>
                </image>
            </item>
        {/foreach}
    </channel>
</rss>

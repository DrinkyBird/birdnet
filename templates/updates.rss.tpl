<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
    <channel>
        <title>Elite Dangerous Updates</title>
        <link>https://elite.drinkybird.net/updates</link>
        <language>en-GB</language>
        {foreach $rows as $row}
            <item>
                <title>{$row->title|htmlspecialchars:ENT_XML1}</title>
                <link>https://elite.drinkybird.net/updates?version={$row->version}</link>
                <guid isPermaLink="false">{$row->version}</guid>
                <pubDate>{$row->date|date_format:"D, d M Y H:i:s O"}</pubDate>
                <description><![CDATA[{$row->text}]]></description>
                <content:encoded><![CDATA[{$row->notes}]]></content:encoded>
            </item>
        {/foreach}
    </channel>
</rss>

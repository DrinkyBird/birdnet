{extends file="main.tpl"}
{assign var="title" value="{$pageTitle}Updates"}
{if $is_single_article}
	{assign var="title" value="{$rows[0]->title|escape}"}
	{assign var="description" value="{$rows[0]->text|strip_tags|escape}"}
{/if}
{block name=content}
	<a href="/updates/rss"><img src="/assets/rss.png" title="RSS" alt="RSS" style="width: 32px; height: 32px; float: right;" /></a>
    <h1 class="title is-1">Updates</h1>
    <div class="columns">
        <div class="column">
            {if count($rows) > 0}
				{foreach $rows as $row}
					<section class="section news-content">
						{if $row->image != null}
						<div class='news-background' style='background-image: url("https://hosting.zaonce.net/elite-dangerous/galnet/{get_image($row)}.png");'>
							<div class='news-background-title'><a href="?version={$row->version}" class="link"><h2 class='title is-2'>{$row->title|escape}</h2></a></div>
						</div>
						{else}
						<a href="?version={$row->version}" class="link"><h2 class='title is-2'>{$row->title|escape}</h2></a>
						{/if}
						<p class='article-date' title='{$row->date|date_format:"%F %T %z"}'>{$row->date|date_format:"%d %b %Y"}</p>
						<div class='content'>{$row->text}{$row->notes|highlight_search:$filter_notes}</div>
						{if $is_single_article}
							<hr>
							<p>View on:
								<ul>
									<li><a href="https://www.elitedangerous.com/update-notes/{$row->version|replace:'.':'-'}">elitedangerous.com</a></li>
									{if $row->forum_post !== null}<li><a href="https://forums.frontier.co.uk/threads/{$row->forum_post}">Frontier Forums</a></li>{/if}
								</ul>
							</p>
						{/if}
					</section>
				{/foreach}
				
				{if !$is_single_article}
					<div class='columns' style='text-align: center'>
						{if $page > 1}
							<div class='column'><a href="?page=1{$filter_url}">&lt;&lt; First</a></div>
							<div class='column'><a href="?page={$page-1}{$filter_url}">&lt; Previous</a></div>
						{else}
							<div class='column'>&lt;&lt; First</div>
							<div class='column'>&lt; Previous</div>
						{/if}
						<div class='column'>Page {$page} / {$pages}</div>
						{if $page < $pages}
							<div class='column'><a href="?page={$page+1}{$filter_url}">Next &gt;</a></div>
							<div class='column'><a href="?page={$pages}{$filter_url}">Last &gt;&gt;</a></div>
						{else}
							<div class='column'>Next &gt;</div>
							<div class='column'>Last &gt;&gt;</div>
						{/if}
					</div>
				{/if}
            {else}
                <p>Your query returned no results.</p>
            {/if}
        </div>
        <div class="column is-one-quarter">
            <h2 class="subtitle">Search</h2>
            <form action="" method="GET">
                <div class="field">
                    <label class="label">Notes contain</label>
                    <div class="control">
                        <input class="input" type="text" name="notes" value="{$filter_text}" />
                    </div>
                </div>
                <div class="field">
                    <div class="control">
                        <input class="button is-link" type="submit" value="Search" />
                    </div>
                </div>
            </form>
            
            <h2 class="subtitle">Archives</h2>
            <ul>
            {foreach $archives as $key => $value}
                <li><a href="?version={$key}">{$key} ({$value|date_format:"%d %b %Y"})</a></li>
            {/foreach}
            </ul>
        </div>
    </div>
{/block}

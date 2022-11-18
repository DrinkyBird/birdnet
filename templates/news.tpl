{extends file="main.tpl"}
{assign var="title" value="{$pageTitle}Galnet News"}
{if $is_single_article}
	{assign var="title" value="{$rows[0]->title|escape} &mdash; Galnet News"}
	{assign var="description" value="{$rows[0]->text|escape}"}
	{assign var="image" value="https://hosting.zaonce.net/elite-dangerous/galnet/{get_image($rows[0])|escape}.png"}
{/if}
{block name=content}
	<a href="/rss?lang={$language}"><img src="/assets/rss.png" title="RSS" alt="RSS" style="width: 32px; height: 32px; float: right;" /></a>
    <h1 class="title is-1">Galnet News</h1>
    <div class="columns">
        <div class="column">
            {if count($rows) > 0}
				{foreach $rows as $row}
					<section class="section news-content">
						{if $row->image != null}
						<div class='news-background' style='background-image: url("https://hosting.zaonce.net/elite-dangerous/galnet/{get_image($row)}.png");'>
							<div class='news-background-title'><a href="?guid={$row->guid}" class="link"><h2 class='title is-2'>{$row->title|escape|highlight_search:$filter_title}</h2></a></div>
						</div>
						{else}
						<a href="?guid={$row->guid}" class="link"><h2 class='title is-2'>{$row->title|escape|highlight_search:$filter_title}</h2></a>
						{/if}
						<p class='article-date' title='{$row->date|date_format:"%F %T %z"}'>{format_timestamp($row->date)}</p>
						<div class='content'>
							{if $extracts_only}
								<p>{$row->text|generate_extract|highlight_search:$filter_text}</p>
								<p><a href="?guid={$row->guid}">Read more...</a></p>
							{else}
								{$row->text|format_text|highlight_search:$filter_text}
							{/if}
						</div>
						{if $is_single_article}
							<hr>
							<p>View on:
								<ul>
									{if $row->slug !== null}<li><a href="https://www.elitedangerous.com/news/galnet/{$row->slug}">elitedangerous.com</a></li>{/if}
									<li><a href="https://community.elitedangerous.com/galnet/uid/{$row->guid}">community.elitedangerous.com</a></li>
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
            <p>All search fields are optional.</p>
            <form action="" method="GET">
                <div class="field">
                    <label class="label">Title contains</label>
                    <div class="control">
                        <input class="input" type="text" name="title" value="{$filter_title}" />
                    </div>
                </div>
                <div class="field">
                    <label class="label">Body contains</label>
                    <div class="control">
                        <input class="input" type="text" name="text" value="{$filter_text}" />
                    </div>
                </div>
                <div class="field">
                    <label class="label">Start date</label>
                    <div class="control">
                        <input class="input" type="date" name="from" value="{$filter_from}" />
                    </div>
                </div>
                <div class="field">
                    <label class="label">End date</label>
                    <div class="control">
                        <input class="input" type="date" name="to" value="{$filter_to}" />
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
                <li><a href="?from={$value[0]}&to={$value[1]}">{$key}</a></li>
            {/foreach}
            </ul>
        </div>
    </div>
{/block}

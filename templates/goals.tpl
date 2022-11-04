{extends file="main.tpl"}
{assign var="num_active" value=count($active)}
{block name=title}Community Goals{/block}
{block name=content}
	<a href="/goals/rss?lang={$language}"><img src="/assets/rss.png" title="RSS" alt="RSS" style="width: 2em; height: 2em; float: right;" /></a>
    <h1 class='title'>Community Goals</h1>
    <h2 class='subtitle'>Active</h2>
	<p>
		{if $num_active == 1}
			One CG is currently active.
		{else}
			{$num_active} CGs are currently active.
		{/if}
	</p>
    {foreach $active as $goal}
        {include file="goals_item.tpl"}
    {/foreach}
    <h2 class='subtitle'>Concluded</h2>
    {foreach $expired as $goal}
        {include file="goals_item.tpl"}
    {/foreach}
{/block}
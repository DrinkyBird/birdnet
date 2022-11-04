{extends file="main.tpl"}
{block name=title}Maps &amp; data{/block}
{block name=content}
	{function name=munin_graph}
		<h2 class="subtitle" id="{$path|escape}"><a href='#{$path|escape}'>#</a> {$title|escape}</h2>
		<div class="columns">
			<div class="column">
				<a href="https://munin.drinkybird.net/munin-cgi/munin-cgi-graph/drinkybird.net/haiti.drinkybird.net/{$path|escape}-day.png">
					<img src="https://munin.drinkybird.net/munin-cgi/munin-cgi-graph/drinkybird.net/haiti.drinkybird.net/{$path|escape}-day.png" alt="{$title|escape}" />
				</a>
			</div>
			<div class="column">
				<a href="https://munin.drinkybird.net/munin-cgi/munin-cgi-graph/drinkybird.net/haiti.drinkybird.net/{$path|escape}-week.png">
					<img src="https://munin.drinkybird.net/munin-cgi/munin-cgi-graph/drinkybird.net/haiti.drinkybird.net/{$path|escape}-week.png" alt="{$title|escape}" />
				</a>
			</div>
		</div>
	{/function}
	
	<h1 class='title'>Graphs</h1>
	{munin_graph title="EDDN messages by schema" path="elitedangerous_eddn_messages"}
	{munin_graph title="EDDN journal messages by event type" path="elitedangerous_eddn_journal"}
	{munin_graph title="EDDN messages by game type" path="elitedangerous_eddn_game_types"}
	{munin_graph title="EDDN messages by software" path="elitedangerous_eddn_software"}
	{munin_graph title="Number of stations known" path="elitedangerous_markets_total"}
	{munin_graph title="Number of systems known" path="elitedangerous_starsystems_total"}
{/block}

{extends file="main.tpl"}
{block name=title}Maps &amp; data{/block}
{block name=content}
	{function name=map}
		<h2 class="subtitle" id="{$path|escape}"><a href='#{$path|escape}'>#</a> {$title|escape}</h2>
		<p>Generation took {(get_timing($path) / 1000000000)|number_format:1} seconds.</p>
		<a href="/maps/{$path|escape}.png"><img src="/maps/{$path|escape}.png" alt="{$title|escape}" /></a>
	{/function}
	
    <h1 class='title'>Maps</h1>
	<p>For heatmaps, blue pixels show systems below y=0, yellow pixels above y=0, and green pixels at y=0.</p>
	
	{map title="All systems" path="systems_all"}
	{map title="Systems updated in past 48 hours" path="systems_recent"}
	{map title="Fleet Carriers" path="carriers"}
{/block}
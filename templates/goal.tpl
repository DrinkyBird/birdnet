{block name=title}{$goal->title} &mdash; Community Goals{/block}
{assign var=title value="{$goal->title}"}
{assign var=description value="{$goal->bulletin|nl2br}"}
{assign var=has_chart value={$sheetId !== null}}
{assign var=chart_has_data value={time() > $row->first_seen + (10 * 60)}}
{assign var=load_google_charts value=($has_chart && $chart_has_data)}
{extends file="main.tpl"}
{if $has_chart && $chart_has_data}
	{block name="head_additional"}
		<script type="text/javascript">
			{literal}const CG = {{/literal}
				"id": {$goal->id},
				"title": "{$goal->title}",
				"sheet": "{$sheetId}"
			{literal}};{/literal}
		</script>
	{/block}
{/if}
{block name=content}
    <a href="/goals">&laquo; Return to Community Goals listing</a>
    <div class='cg'>
        <h1 class='title'>{$goal->title}</h1>
        <p><b>Location:</b> {$goal->market_name}, {$goal->system_name}</p>
        <p><b>Ends:</b> {$goal->expiry|date_format:"%F %T %z"}</p>
        <p><b>Activity:</b> {$goal->activity|get_cg_activity_name}</p>
        <p><b>Objective:</b> {$goal->objective}</p>
        {if $goal->quantity != 0}
            <p>
                <b>Progress:</b>
                {$goal->progress|number_format:0} / {$goal->quantity|number_format:0} ({math equation="x / y * 100" x=$goal->progress y=$goal->quantity format="%.2f"}%)
                {if $has_chart}
                    (<a href="https://docs.google.com/spreadsheets/d/{$sheetId}/edit">Sheet</a>)
                {/if}
            </p>
        {/if}
        <progress class="progress{if $goal->progress >= $goal->quantity} is-success{/if}" value="{$goal->progress}" max="{$goal->quantity}"></progress>
        {if $has_chart}<p><b>Progress Graph</b> {if $chart_has_data}(<a href="/goals/{$goal->id}/graph">full screen</a>){/if}</p>
		<div id="progressChart" style="width: 100%; height: 250px;">
			{if $chart_has_data}
			Loading chart... (make sure you have JavaScript enabled)
			{else}
			Not enough data for the graph just yet, check back in a few minutes.
			{/if}
		</div>{/if}
        <p><b>Last updated:</b> {$goal->last_updated|date_format:"%F %T %z"}</p>
        {if $goal->first_seen <= 1645102800}
        <p><b>First seen:</b> <span class="has-help-title" title="This CG was started before their first seen dates were tracked; the date shown is an estimation that may be inaccurate.">{$goal->first_seen|date_format:"%F %T %z"}</span></p>
        {else}
        <p><b>First seen:</b> {$goal->first_seen|date_format:"%F %T %z"}</p>
        {/if}
        <h3 class="title is-5">Bulletin</h3>
        <blockquote>{$goal->bulletin|format_text}</blockquote>
    </div>
    
	{if $has_chart && $chart_has_data}
    <script type="text/javascript" src="/assets/cggraph.min.js"></script>
	{/if}
{/block}
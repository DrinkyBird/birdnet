{extends file="main.tpl"}
{block name=title}Maps &amp; data{/block}
{block name=content}
	<h2 class='title'>Most popular stations</h2>
	<p>Most visited stations in the past 24 hours. This is based on EDDN data and may not be representative.</p>
	<p>A visit is counted as any <tt>Docked</tt> or <tt>Location</tt> journal event at a station.</p>
	<table class='table is-fullwidth is-narrow is-striped'>
		<thead>
			<tr>
				<th>System</th>
				<th>Station</th>
				<th>Type</th>
				<th>Visits</th>
			</tr>
		</thead>
		<tbody>
			{foreach $markets as $market}
				{if $market->count > 1}
					<tr>
						<td><a href='https://eddb.io/system/ed-address/{$market->system_id}'>{$market->system_name|escape}</a></td>
						<td><a href='https://eddb.io/station/market-id/{$market->market_id}'>
							{if $market->market_type == "FleetCarrier"}
							{$market->market_name|get_carrier_name|escape}
							{else}
							{$market->market_name|escape}
							{/if}
						</a></td>
						<td>{$market->market_type|escape}</td>
						<td>{$market->count}</td>
					</tr>
				{/if}
			{/foreach}
		</tbody>
	</table>
{/block}
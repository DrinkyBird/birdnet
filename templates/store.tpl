{extends file="main.tpl"}
{block name=title}Store Items{/block}
{block name=content}
	<a href="/store/rss"><img src="/assets/rss.png" title="RSS" alt="RSS" style="width: 2em; height: 2em; float: right;" /></a>
    <h1 class='title'>Store Items</h1>
	<p>Note that greyed out rows indicate that item is currently not available for purchase from the game store.</p>
	<div>
		<b>Filter:</b> <a href="store/filter?{$smarty.server.QUERY_STRING}">Edit</a>
		{if $filter_name !== null}
			<span class="tag is-medium">Name contains: "{$filter_name}"</span>
		{/if}
		{if $filter_available !== null}
			<span class="tag is-medium">Available: {($filter_available) ? "Yes" : "No"}</span>
		{/if}
		{if $filter_discounted !== null}
			<span class="tag is-medium">Discounted: {($filter_discounted) ? "Yes" : "No"}</span>
		{/if}
		{foreach $filter_attributes as $attr}
			<span class="tag is-medium">Has attribute: {$attr|get_store_attribute_name}</span>
		{/foreach}
	</div>

	{assign var="totalCost" value=0}
	<table class="table is-fullwidth is-narrow is-striped">
		<thead>
			<tr>
				<th colspan="2">SKU</th>
				<th>Name</th>
				<th>Price</th>
				<th>First Seen</th>
			</tr>
		</thead>
		<tbody>
			{foreach $items as $item}
				{math equation="x + y" x=$totalCost y=$item->current_price assign="totalCost"}
				{if $item->available === 0}
					{assign var=class value="has-background-grey-lighter"}
				{elseif $item->discounted}
					{assign var=class value="has-background-primary-light"}
				{else}
					{assign var=class value=""}
				{/if}
				<tr class="{$class}">
					<td>
						{if $item->available === 1}
							<a href="https://dlc.elitedangerous.com/product/{$item->slug}">
								<img src="assets/arx.svg" alt="ARX Store" title="View on the Elite Dangerous DLC store" style="width: 1.5em; height: 1.5em;" />
							</a>
						{/if}
					</td>
					<td><code>{$item->sku}</code></td>
					<td><a href="/store/{$item->sku}">{$item->title}</a></td>
					<td>
						{if $item->current_price != $item->original_price and $item->available}
							<s>{$item->original_price}</s> {$item->current_price}
						{else}
							{$item->current_price}
						{/if}
					</td>
					<td>{$item->first_seen|date_format:"%F %T %z"}</td>
				</tr>
			{/foreach}
		</tbody>
	</table>

	<p>{$itemCount|number_format} items shown with a total cost of {$totalCost|number_format} Arx (at current prices).</p>
{/block}
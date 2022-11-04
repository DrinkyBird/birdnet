{extends file="main.tpl"}
{block name=title}Store Items{/block}
{block name=content}
	<a href="/store/rss"><img src="/assets/rss.png" title="RSS" alt="RSS" style="width: 2em; height: 2em; float: right;" /></a>
    <h1 class='title'>Store Items</h1>
	<p>{$itemCount|number_format} items</p>
	<p>Note that greyed out items are currently unavailable.</p>
	{if false}
	<form action="" method="GET">
        <div class="field">
            <div class="select">
                <select name="attribute">
					{foreach $attributes as $attribute}
						<option value="{$attribute}">
							{$attribute|get_store_attribute_name}
						</option>
					{/foreach}
                </select>
            </div>
		</div>
	</form>{/if}
	<table class="table is-fullwidth is-narrow is-striped">
		<thead>
			<tr>
				<th>SKU</th>
				<th>Name</th>
				<th>Price</th>
				<th>First Seen</th>
			</tr>
		</thead>
		<tbody>
			{foreach $items as $item}
				{if $item->available == 0}
					{assign var=class value="has-background-grey-lighter"}
				{elseif $item->discounted}
					{assign var=class value="has-background-primary-light"}
				{else}
					{assign var=class value=""}
				{/if}
				<tr class="{$class}">
					<td><code>{$item->sku}</code></td>
					<td><a href="/store/{$item->sku}">{$item->title}</a></td>
					<td>
						{if $item->current_price != $item->original_price}
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
{/block}
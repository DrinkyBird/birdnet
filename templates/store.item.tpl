{extends file="main.tpl"}
{assign var=title value="{$item->title}"}
{assign var=description value="{$description}"}
{if $item->colour}
{assign var=discord_colour value="#{$item->colour}"}
{/if}
{assign var=image value="https://dlc.elitedangerous.com/images/med/{$item->small_image|escape}"}
{block name=content}
    <a href="/store">&laquo; Return to store listing</a>
	{if $item === false}
		<p>No item with that SKU is known.</p>
	{else}
		<h1 class='title'>{$item->title}</h1>
		<p><a href="https://dlc.elitedangerous.com/product/{$item->slug}">View on the Elite Dangerous store</a></p>
		<p><b>SKU:</b> <code>{$item->sku}</code></p>
		<p><b>Current Price:</b> {$item->current_price|number_format}</p>
		<p><b>Original Price:</b> {$item->original_price|number_format}</p>
		<p><b>Type:</b> {$item->type}</p>
		<p><b>Subtype:</b> {$item->subtype}</p>
		<p><b>Available:</b> {($item->available == 1) ? "Yes" : "No"}</p>
		<p><b>Minimum Client Version:</b> {$item->minimum_client_version|get_store_client_version_name}</p>
		<p><b>Minimum Season:</b> {$item->minimum_season|get_store_season_name}</p>
		<p><b>Thumbnail:</b> <br /> <a href="https://dlc.elitedangerous.com/images/med/{$item->thumbnail|escape}"><img src="https://dlc.elitedangerous.com/images/med/{$item->thumbnail|escape}" /></a></p>
		<p><b>Image:</b> <br /> <a href="https://dlc.elitedangerous.com/images/med/{$item->image|escape}"><img src="https://dlc.elitedangerous.com/images/med/{$item->image|escape}" /></a></p>
		<p><b>Small Image:</b> <br /> <a href="https://dlc.elitedangerous.com/images/med/{$item->small_image|escape}"><img src="https://dlc.elitedangerous.com/images/med/{$item->small_image|escape}" /></a></p>
		<p>
			<b>Description:</b>
			<blockquote>{$item->short_description}</blockquote>
		</p>
		<p>
			<b>Attributes</b>
			<table class="table is-fullwidth is-narrow is-striped">
				<thead>
					<tr>
						<th>ID</th>
						<th>Description</th>
					</tr>
				</thead>
				<tbody>
					{foreach $attributes as $id}
						<tr>
							<td>{$id}</td>
							<td>{$id|get_store_attribute_name}</td>
						</tr>
					{/foreach}
				</tbody>
			</table>
		</p>
	{/if}
{/block}

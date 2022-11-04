{extends file="main.tpl"}
{block name=title}Server Status{/block}
{block name=content}
    <h1 class='title'>Server Status</h1>
	<table class="table is-fullwidth is-narrow is-striped">
		<thead>
			<tr>
				<th>Timestamp</th>
				<th>Code</th>
				<th>Text</th>
			</tr>
		</thead>
		<tbody>
			{foreach $statuses as $status}
				<tr>
					<td>{$status->timestamp|date_format:"%F %T %z"}</td>
					<td><code>{$status->status_code}</code></td>
					<td>{$status->status_text|escape}</td>
				</tr>
			{/foreach}
		</tbody>
	</table>
{/block}
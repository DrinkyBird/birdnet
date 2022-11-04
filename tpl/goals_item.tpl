<div class='cg'>
    <h2 class='subtitle'><a href='/goals/{$goal->id}'>{$goal->title}</a></h2>
    <p>
        <b>Location:</b>
        {$goal->market_name},
        {$goal->system_name}
    </p>
    <p><b>Ends:</b> {$goal->expiry|date_format:"%F %T %z"}</p>
    <p><b>Progress:</b> {$goal->progress|number_format:0} / {$goal->quantity|number_format:0} ({math equation="x / y * 100" x=$goal->progress y=$goal->quantity format="%.2f"}%)</p>
    <progress class="progress{if $goal->progress >= $goal->quantity} is-success{/if}" value="{$goal->progress}" max="{$goal->quantity}"></progress>
</div>
<hr/>
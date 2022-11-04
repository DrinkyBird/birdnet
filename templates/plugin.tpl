{extends file="main.tpl"}
{block name=title}EDMC Plugin{/block}
{block name=content}
    <h1 class='title'>BirdNet EDMC Plugin</h1>
	<h2 class='subtitle'>Collected Journal Events</h2>
	<ul>
		<li><b><code>CommunityGoal</code></b>: used for more immediate tracking of CG status, and hidden CGs</li>
		<li><b><code>CarrierJump</code></b>, <b><code>CarrierJumpRequest</code></b>, <b><code>CarrierJumpCancelled</code></b>: tracking of average galactic FC jump time</li>
	</ul>
	
	<h2 class='subtitle'>Installation</h2>
	<ol>
		<li>Launch EDMC</li>
		<li>Go to File &#x2192; Settings</li>
		<li>Go to the Plugins tab</li>
		<li>Click Open next to the plugins folder path</li>
		<li>Extract the downloaded zip file to the folder that opened</li>
		<li>Restart EDMC</li>
	</ol>
{/block}
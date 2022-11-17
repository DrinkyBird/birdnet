<!DOCTYPE html>
<html>
    <head>
        <meta charset='utf-8' />
        <title>{if isset($title)}{$title|escape}{else}{block name="title"}missing title block{/block}{/if} &mdash; BirdNet</title>

        <link rel='stylesheet' type='text/css' href='/assets/bulma.min.css?0' />
        <link rel='stylesheet' type='text/css' href='/assets/birdnet.css?7' />

        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
		
		<meta property="og:site_name" content="BirdNet" />
		{if isset($title)}<meta property="og:title" content="{$title|escape}" />{/if}
		{if isset($description)}<meta property="og:description" content="{$description|escape}" />{/if}
		{if isset($image)}<meta property="og:image" content="{$image|escape}" />{/if}
		{if isset($discord_colour) and is_discord()}<meta name="theme-color" content="{$discord_colour|escape}" />{/if}
        
        <script defer src="/assets/webjs.min.js"></script>
		{if isset($load_google_charts) && $load_google_charts}<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>{/if}
		{block name="head_additional"}{/block}
    </head>
    <body>
        <nav class="navbar" role="navigation" aria-label="main navigation">
            <div class="navbar-brand">
                <div class="navbar-item">
                    <strong>BirdNet</strong>
                </div>
                
                <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarMain" onclick="navbarClick()">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>
            <div id="navbarMain" class="navbar-menu">
				<div class="navbar-start">
					<a class="navbar-item" href='/'>News</a>
					<a class="navbar-item" href='/goals'>Community Goals</a>
					<a class="navbar-item" href='/store'>Store</a>
					<a class="navbar-item" href='/updates'>Updates</a>
				</div>
				<div class="navbar-end">
					<a class="navbar-item" href='/language'>Language</a>
					<div class="navbar-item" id='clock' style="font-family: Consolas, monospace;"></div>
				</div>
			</div>
        </nav>
        
        <section class="section">
            <div class="container is-max-desktop">
                <div class="content">
                    {block name="content"}{/block}
                </div>
            </div>
        </section>
        
        <footer class="footer">
            <div class="content has-text-centered">
				<p>
					BirdNet is owned and operated by <a href="https://drinkybird.net">DrinkyBird</a> (<a href="https://inara.cz/cmdr/110994/">CMDR csn</a>)
				</p>
                <p>
                    This website uses content from <a href="https://elitedangerous.com">Elite Dangerous</a> which is developed by <a href="https://frontier.co.uk">Frontier Developments</a>. <br />This website is not endorsed by nor reflects the views or opinions of Frontier Developments and no employee of Frontier Developments was involved in the making of it.
                </p>
            </div>
        </footer>
        
        <script src="/assets/spaceclock.min.js"></script>
    </body>
</html>

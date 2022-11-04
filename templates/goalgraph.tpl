<!DOCTYPE html>
<html>
    <head>
        <meta charset='utf-8' />
        <title>{$goal->id}</title>

        <link rel='stylesheet' type='text/css' href='/assets/bulma.min.css' />
		
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<script type="text/javascript">
			{literal}const CG = {{/literal}
				"id": {$goal->id},
				"title": "{$goal->title}",
				"sheet": "{$sheetId}"
			{literal}};{/literal}
		</script>
		
		<style type="text/css"> 
			html, body {
				margin: 0;
				height: 100%;
			}
			
			.return {
				position: fixed;
				top: 15px;
				left: 15px;
			}
		</style>
    </head>
    <body>
		<div id="progressChart" style="width: 100%; height: 100%;"></div>
		<a href="/goals/{$goal->id}" class="return">&laquo; Return to {$goal->title|escape}</a>
		<script type="text/javascript" src="/assets/cggraph.min.js"></script>
    </body>
</html>
{extends file="main.tpl"}
{block name=title}Language{/block}
{block name=content}
    <h1 class="title is-1">Change Language</h1>
    {if $changed}
    <div class="message is-success">
        <div class="message-body">
            Your content language was set successfully.
        </div>
    </div>
    {/if}

    <p>You can change your language for BirdNet here. This only affects the text for Galnet News and Community Goals.</p>
    <p>Note that community goal progress on non-English languages may lag behind a bit due to poor database design.</p>
    <form action="" method="POST">
        <div class="field">
            <label class="label">Language</label>
            <div class="select">
                <select name="lang">
					{for $i = 0 to count($languageIds)-1}
						<option value="{$languageIds[$i]}" {if $currentLanguage == $languageIds[$i]}selected{/if}>
							{$languageNames[$i]} {if $defaultLanguage == $languageIds[$i]}(system){/if}
						</option>
					{/for}
                </select>
            </div>
        </div>
        <div class="field">
            <div class="control">
                <input class="button is-link" type="submit" value="Save" />
            </div>
        </div>
    </form>
{/block}
{extends file="main.tpl"}
{block name=title}Home{/block}
{block name=content}
    <h1 class='title'>Welcome to BirdNet</h1>
    <div class="columns">
        <div class="column is-one-third">
            <a href="/news">
                <div class="card">
                    <div class="card-image">
                        <figure class="image is-2by1">
                            <img src="/assets/img_home_news.png" />
                        </figure>
                    </div>
                    
                    <div class="card-content">
                        <div class="content">
                            <h2 class="title is-4">Galnet News</h2>
                            <p><i>"Your galaxy in focus."</i></p>
                            <p>View the latest - and older - happenings in the galaxy with a slightly nicer interface.</p>
                        </div>
                    </div>
                </div>
            </a>
        </div>
        <div class="column is-one-third">
            <a href="/goals">
                <div class="card">
                    <div class="card-image">
                        <figure class="image is-2by1">
                            <img src="/assets/img_home_goals.png" />
                        </figure>
                    </div>
                    
                    <div class="card-content">
                        <div class="content">
                            <h2 class="title is-4">Community Goals</h2>
                            <p>View present and past Community Goals.</p>
                        </div>
                    </div>
                </div>
            </a>
        </div>
        <div class="column is-one-third">
            <a href="/eddn">
                <div class="card">
                    <div class="card-image">
                        <figure class="image is-2by1">
                            <img src="/assets/img_home_eddn.png" />
                        </figure>
                    </div>
                    
                    <div class="card-content">
                        <div class="content">
                            <h2 class="title is-4">EDDN</h2>
                            <p>View statistics about the Elite Dangerous Data Network.</p>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>
    <div class="columns">
        <div class="column is-one-third">
            <a href="/systems">
                <div class="card">
                    <div class="card-image">
                        <figure class="image is-2by1">
                            <img src="/assets/img_home_systems.png" />
                        </figure>
                    </div>
                    
                    <div class="card-content">
                        <div class="content">
                            <h2 class="title is-4">Systems</h2>
                            <p>View informations about star systems in Elite Dangerous.</p>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>
{/block}
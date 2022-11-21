{extends file="main.tpl"}
{assign var=title value="Build-a-Filter Workshop"}
{block name=content}
    <h1 class='title'>Build-a-Filter Workshop</h1>
    <p>All fields are optional.</p>
    <noscript>
        <article class="message is-warning">
            <div class="message-body">
                Attribute filtering is only available when JavaScript is enabled.
            </div>
        </article>
    </noscript>

    <form method="get" action="/store">
        <table class="table is-fullwidth">
            <tbody id="filtertable-body">
                <tr>
                    <th><label for="name">Name contains</label></th>
                    <td><input class="input" type="text" id="name" name="name" value="{(isset($smarty.get.name)) ? $smarty.get.name : ""}" /></td>
                    <td colspan="2"></td>
                </tr>
                <tr>
                    <th><label for="available">Availability</label></th>
                    <td>
                        <div class="select is-fullwidth">
                            <select id="available" name="available">
                                <option value="">Any</option>
                                <option value="true" {if $filter_available == "true"}selected{/if}>Available</option>
                                <option value="false" {if $filter_available == "false"}selected{/if}>Unavailable</option>
                            </select>
                        </div>
                    </td>
                    <td colspan="2"></td>
                </tr>
                <tr>
                    <th><label for="discounted">Discounted</label></th>
                    <td>
                        <div class="select is-fullwidth">
                            <select id="discounted" name="discounted">
                                <option value="">Any</option>
                                <option value="true" {if $filter_discounted == "true"}selected{/if}>Yes</option>
                                <option value="false" {if $filter_discounted == "false"}selected{/if}>No</option>
                            </select>
                        </div>
                    </td>
                    <td colspan="2"></td>
                </tr>
            </tbody>
        </table>

        <input class="button is-primary" type="submit" value="Apply" />
        <a class="button" href="/store/filter">Reset</a>
    </form>

    <script>
        const tbody = document.getElementById("filtertable-body");
        const filterAttributes = [ {implode(",", $filter_attributes)} ];
        const STORE_ATTRIBUTES_GROUPED = {
            {foreach STORE_ATTRIBUTES_GROUPED as $group => $values}
                {if is_array($values)}
                    "{$group}": {
                        {foreach $values as $id => $desc}
                            {$id}: "{$desc}",
                        {/foreach}
                    },
                {else}
                    {$group}: "{$values}",
                {/if}
            {/foreach}
        };

        for (let i = 0; i < filterAttributes.length; i++) {
            addRow(filterAttributes[i]);
        }

        if (filterAttributes.length < 1) {
            addRow();
        }

        function addRow(attribute) {
            const tr = document.createElement("tr");
            tr.dataset.isArxAttribute = "true";

            const fieldName = document.createElement("th");
            const label = document.createElement("label");
            fieldName.appendChild(label);
            tr.appendChild(fieldName);

            const value = document.createElement("td");
            const select = createSelect(attribute);
            value.appendChild(select);
            tr.appendChild(value);

            const addButtonField = document.createElement("td");
            const addButton = document.createElement("input");
            addButton.type = "button";
            addButton.className = "button is-success";
            addButton.value = "Add";
            addButton.onclick = ev => { addRow(); };
            addButtonField.appendChild(addButton);
            tr.appendChild(addButtonField);

            const delButtonField = document.createElement("td");
            const delButton = document.createElement("input");
            delButton.type = "button";
            delButton.className = "button is-danger";
            delButton.value = "Del";
            delButton.onclick = onRemoveButton;
            delButtonField.appendChild(delButton);
            tr.appendChild(delButtonField);

            tbody.appendChild(tr);

            updateRows();
        }

        function createSelect(attribute) {
            const div = document.createElement("div");
            div.className = "select is-fullwidth";

            const select = document.createElement("select");
            select.name = "attribute[]";

            const empty = document.createElement("option");
            empty.value = "";
            empty.innerText = "-";
            select.appendChild(empty);

            for (const group in STORE_ATTRIBUTES_GROUPED) {
                const values = STORE_ATTRIBUTES_GROUPED[group];

                if (typeof values === "object") {
                    const optgroup = document.createElement("optgroup");
                    optgroup.label = group;

                    for (const id in values) {
                        const desc = values[id];

                        const option = document.createElement("option");
                        option.value = id;
                        option.innerText = desc;

                        if (id == attribute) {
                            console.info("OK");
                            option.selected = true;
                        }

                        optgroup.appendChild(option);
                    }

                    select.appendChild(optgroup);
                } else {
                    const option = document.createElement("option");
                    option.value = group;
                    option.innerText = values;

                    if (group == attribute) {
                        console.info("OK");
                        option.selected = true;
                    }

                    select.appendChild(option);
                }
            }

            div.appendChild(select);
            return div;
        }

        function updateRows() {
            let row = 0;
            const rows = countRows();

            for (let i = 0; i < tbody.children.length; i++) {
                const child = tbody.children[i];

                if (!child.dataset.isArxAttribute) {
                    continue;
                }

                const selectId = "attr-select-" + row;

                child.children[0].children[0].innerText = (row === 0 ? "Has attribute" : "and");
                child.children[0].children[0].htmlFor = selectId;
                child.children[1].children[0].children[0].id = selectId;
                child.children[2].children[0].style.display = (row < rows - 1 ? "none" : "block");
                child.dataset.isFirst = (row === 0 ? "true" : "false");

                row++;
            }
        }

        function countRows() {
            let n = 0;

            for (let i = 0; i < tbody.children.length; i++) {
                if (tbody.children[i].dataset.isArxAttribute) {
                    n++;
                }
            }

            return n;
        }

        function onRemoveButton() {
            const row = this.parentElement.parentElement;
            const isFirst = row.dataset.isFirst === "true";
            row.remove();
            if (isFirst && countRows() === 0) {
                addRow();
            }
            updateRows();
        }
    </script>
{/block}

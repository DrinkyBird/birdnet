google.charts.load("current", { "packages": [ "corechart" ] });
google.charts.setOnLoadCallback(prepareChart);

function prepareChart() {
    let query = new google.visualization.Query("https://docs.google.com/spreadsheets/d/" + CG.sheet + "/gviz/tq?gid=0&headers=1", {});
    query.send(queryResponse);
}

/** @param {google.visualization.CallbackResponse} response */
function queryResponse(response) {
    let div = document.getElementById("progressChart");
    if (response.isError()) {
        console.error(response.getMessage() + ": " + response.getDetailedMessage());
        div.style.color = "#FF0000";
        div.innerText = "Failed to load data for graph.\n" + response.getMessage() + ': ' + response.getDetailedMessage();
    } else {
		/** @type {google.visualization.DataTable} */
        let data = response.getDataTable();
        data.setColumnLabel(0, "Time");
        data.setColumnLabel(1, "Total progress");
        data.setColumnLabel(2, "Change since last poll");
        
        let view = new google.visualization.DataView(data);
        view.setColumns([ 0, 2, 1 ]);
        
        const opts = {
            "title":                CG.title,
            "curveType":            "none",
            "focusTarget":          "category",
            "hAxis": {
                "title":            "Time"
            },
            "series": {
                0: { 
                    "targetAxisIndex":  1,
                    "color":            "#AAAAAA"
                },
                1: { 
                    "targetAxisIndex":  0,
                    "color":            "#3366CC"
                }
            },
            "vAxes": {
                0: { 
                    "title":            "Progress",
                    "format":           "decimal",
                    "minValue":         0,
                    "viewWindow": {
                        "min":          0
                    }
                },
                1: { 
                    "title":            "Change",
                    "format":           "decimal",
                    "minValue":         0,
                    "viewWindow": {
                        "min":          0
                    }
                }
            }
        };
        
        let chart = new google.visualization.LineChart(div);
        chart.draw(view, opts);
    }
}
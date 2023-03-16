var name;
var add_see_also_url;

// initialize global variables which are defined as template strings in parent html
function initializeAddSeeAlsoListener(name, add_see_also_url) {
    this.name = name
    this.add_see_also_url = add_see_also_url
}

// add listener to buttons in autocomplete table
document.getElementById("autocomplete_table").addEventListener("click", function(e) {
    if (e.target && e.target.type == "button") {
        let formData = new FormData()
        formData.append('subject', name)
        formData.append('obj', e.target.id)

        // request to flask endpoints to add new related resource to the graph
        fetch(add_see_also_url, {
            "method": "POST",
            "body": formData,
        }).then(
            () => {
                //remove row with suggestion
                document.getElementById(e.target.id).parentElement.parentElement.outerHTML = "";

                //add new row to "seeAlso" section
                var tableBody = document.getElementById("see_also_table").getElementsByTagName('tbody')[0];
                var newRow = tableBody.insertRow();
                var newCell = newRow.insertCell();
                var newText = document.createTextNode(e.target.id);
                var newA = document.createElement('a');
                newA.appendChild(newText);
                newA.title = e.target.id;
                newA.href = e.target.id;
                newCell.appendChild(newA);
                newCell = newRow.insertCell();
                var newButton = document.createElement('input');
                newButton.type = "button";
                newButton.id = e.target.id
                newButton.name = e.target.id
                newButton.value = "remove"
                newCell.appendChild(newButton);
            }
        );
    }
});
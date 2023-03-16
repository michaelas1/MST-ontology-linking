var name;
var remove_see_also_url;

// initialize global variables which are defined as template strings in parent html
function initializeRemoveSeeAlsoListener(name, remove_see_also_url) {
    this.name = name
    this.remove_see_also_url = remove_see_also_url
}

// add listener to buttons to remove related data
document.getElementById("see_also_table").addEventListener("click", function(e) {
    if (e.target && e.target.type == "button") {

        let formData = new FormData()
        formData.append('subject', name)
        formData.append('obj', e.target.name)

        // request to flask endpoints to remove related resource from the graph
        fetch(remove_see_also_url, {
            "method": "POST",
            "body": formData,
        }).then(
            () => {
                //remove row
                document.getElementById(e.target.id).parentElement.parentElement.outerHTML = "";
            }
        );
    }
});
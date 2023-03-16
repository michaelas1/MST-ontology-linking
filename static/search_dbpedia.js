function searchDBPedia() {
    // looks up keywords on DBPedia and gives autocomplete suggestions

    var searchbar_text = document.getElementById('searchbar')

    $("#searchbar").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "https://lookup.dbpedia.org/api/search?query=" + searchbar_text.value,
                dataType: "xml",
                success: function(xml) {

                    // store the results of the AJAX query in an array
                    var result_array = [];
                    $(xml).find('Result').each(function(i, first) {
                        result_array[i] = [];
                        $(first).find("> Label").each(function(j, second) {
                            result_array[i].push($(second).text());
                        });
                        $(first).find("> URI").each(function(j, second) {
                            result_array[i].push($(second).text());
                        });
                    });

                    // map result array to dict format expected by autocomplete
                    result_array = $.map(result_array, function(m) {
                        return {
                            label: m[0],
                            url: m[1]
                        };
                    });

                    // limit responses to first 10 entries
                    response(result_array.slice(0, 10));
                },
                error: function(xhr) {
                    // no specific error information for security reasons
                    console.log("An error has occured");
                }

            });
        },
        create: function() {
            // format response as a list instead of a drop-down menu
            $(this).data('ui-autocomplete')._renderMenu = function(ul, items) {

                //remove previous autocomplete table 
                $("#autocomplete_table tbody tr").remove();

                //create new table
                $.each(items, function(index, item) {
                    var table = $("#autocomplete_table");
                    var item_link = "<a href=" + item.url + ">" + item.url + "</a>"
                    table.append("<tr><td>" + item.value + "</td><td>" + item_link + "</td><td><input type='button' id='" + item.url + "' value='add'></td>");
                });
            };

        }
    });
}
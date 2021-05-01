
d3.select("#button").on("click", function() {
    var first_name = d3.select('#first_name').property('value');
    var last_name = d3.select('#last_name').property('value');
    var entry = {first_name: first_name,
                last_name: last_name
                };
        console.log(entry)
    var my_url = "http://127.0.0.1:5000/scrape"
    fetch(my_url, {method:'POST', body: JSON.stringify(entry), headers: new Headers({
        "content-type": "application/json"
      })})
        .then(response => response.json()).then((data)=> {
        console.log(data)
       
        var Year = data.demo[0]
        var First = data.demo[4]
        var Last = data.demo[5]
        var Country = data.demo[1]
        var State = data.demo[2]
        var City = data.demo[3]
        var Height = data.demo[7]
        var Weight = data.demo[6]
        var Bats = data.demo[8]
        var Throws = data.demo[9]

        var list = d3.select("ul");

        list.append("li").text(`First Name: ${First}`);
        list.append("li").text(`Last Name: ${Last}`);
        list.append("li").text(`Birth Year: ${Year}`);
        list.append("li").text(`Country: ${Country}`);
        list.append("li").text(`State: ${State}`);
        list.append("li").text(`City: ${City}`);
        list.append("li").text(`Height: ${Height}`);
        list.append("li").text(`Weight: ${Weight}`);
        list.append("li").text(`Bats: ${Bats}`);
        list.append("li").text(`Throws: ${Throws}`);

        var stats_temp = data.stats.replaceAll("\\\\", "")
        var statcast_temp = data.statcast.replaceAll("\\\\", "");

        var stats = JSON.parse(stats_temp)
        var statcast = JSON.parse(statcast_temp)

        console.log(stats)
        console.log(Object.keys(stats))

        var stat_head = d3.select("#stat_head");
        var stat_body = d3.select("#stat_body");
        var statcast_head = d3.select("#statcast_head");
        var statcast_body = d3.select("#statcast_body");

        
        Object.keys(stats).forEach((headers) => {
            var row = stat_head.append("tr");
            Object.entries(headers).forEach(([key, value]) => {
              var cell = row.append("th");
              cell.text(value);
            });
          });
        Object.values(stats).forEach((rows) => {
            var row = stat_body.append("tr");
            Object.entries(rows).forEach(([key, value]) => {
              var cell = row.append("td");
              cell.text(value);
            });
          });
 

          Object.keys(statcast).forEach((headers) => {
            var row = statcast_head.append("tr");
            Object.entries(headers).forEach(([key, value]) => {
              var cell = row.append("th");
              cell.text(value);
            });
          });
        
          Object.values(statcast).forEach((rows) => {
            var row = statcast_body.append("tr");
            Object.entries(rows).forEach(([key, value]) => {
              var cell = row.append("td");
              cell.text(value);
            });
          });
          

    });
});

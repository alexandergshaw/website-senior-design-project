function test() {
    var the_stats = {{ all_stats }};

    let filtered_stats = the_stats.filter(stat => stat.voltage >= 4);
    document.getElementById("stats_list").innerHTML(filtered_stats);
}

var the_stats = "{{ all_stats }}";

document.getElementById("stats_list").innerHTML = the_stats.filter(stats => "{{stats.voltage}}" >= 4.0);
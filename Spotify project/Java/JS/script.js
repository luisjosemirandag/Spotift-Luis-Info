/* Function to read the csv and paste it when we call it */
var artist_names = [];
var artist_pictures = [];
var artist_origin = [];

d3.csv("https://raw.githubusercontent.com/luisjosemirandag/spotify-luis-insights/master/Spotify%20project/Mejores%205%20artistas.csv").then(function(data){
  for (f = 0; f < 5 ; f ++){
    artist_names.push(data[f].Artist_Name)
    document.getElementById("artist_nm_"+f).innerHTML = artist_names[f];
    artist_pictures.push(data[f].Artist_Picture)
    document.getElementById("artist_px_"+f).innerHTML = "<img src="+artist_pictures[f]+" class='img-thumbnail' width='200' height='200'>";
    artist_origin.push(data[f].artist_country);
  };

artist_names = [artist_names[0], artist_names[1], artist_names[2], artist_names[3], artist_names[4]]
artist_pictures = [artist_pictures[0], artist_pictures[1], artist_pictures[2], artist_pictures[3], artist_pictures[4]]
artist_origin = [artist_origin[0], artist_origin[1], artist_origin[2], artist_origin[3], artist_origin[4]]

svg = d3.select('svg');
projection = d3.geoOrthographic();
pathGenerator = d3.geoPath().projection(projection);


d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(function(data){
  world = {type:"Sphere"};
  countries = topojson.feature(data,data.objects.countries)
  countries_wt   = [];
  for (var i = 0; i < 177 ; i++){
    countries_wt.push(topojson.feature(data,data.objects.countries.geometries[i]));
  }
  i = -1
  n = countries_wt.lenght
  countries_top = artist_origin;
  indexes = []
  for (g = 0; g < 5; g++){
    for (i = 0; i < 177; i++) {
        if (countries_top[g].includes(countries_wt[i].properties.name)){
            indexes.push(i)
        }
      }
  }
  svg.append("path")
    .datum(world)
    .attr("d", pathGenerator);

  country = svg.selectAll(null).data(countries.features).enter().append('path').attr('d', pathGenerator)
      .attr('class','countries')
    .attr('d',pathGenerator);

  var title = svg.append("text")
    .attr("x", 960 / 2)
    .attr("y", 500 / 2); 
  step();
  function step() {
    if (++i >= 5) i = 0
    title.text(artist_names[i]+" - "+countries_wt[indexes[i]].properties.name).style("fill","white")
    title.style("font-size",20)
    title.style("text-shadow","-1px 0 #000, 0 1px #000, 1px 0 #000, 0 -1px #000")
    country.transition().style("fill", function(d, j) { return j === indexes[i] ? "#033f03" : "#80cc86"; });
    d3.transition()
        .delay(250)
        .duration(1000)
        .tween("rotate", function() {
          point = d3.geoCentroid(countries_wt[indexes[i]]),
          rotate = d3.interpolate(projection.rotate(), [-point[0], -point[1]]);
          return function(t) {
            projection.rotate(rotate(t));
            country.attr("d", pathGenerator);
          };
        })
      .transition()
        .on("end", step);     
      }
  });
});


artist_sign = [{sign:"Aries",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Aries.svg/1081px-Aries.svg.png' class='img-thumbnail'>",plural:"aries"},
  {sign:"Taurus",url: "<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Taurus.svg/980px-Taurus.svg.png' class='img-thumbnail'>",plural:"tauruses"},
  {sign:"Gemini",url: "<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Gemini.svg/998px-Gemini.svg.png' class='img-thumbnail'>",plural:"geminis"},
  {sign:"Cancer",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Cancer.svg/1280px-Cancer.svg.png' class='img-thumbnail'>",plural:"cancers"},
  {sign:"Leo",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Leo.svg/802px-Leo.svg.png' class='img-thumbnail'>",plural:"leos"},
  {sign:"Virgo",url:"<img src='https://uploadartist_sing.wikimedia.org/wikipedia/commons/thumb/0/0c/Virgo.svg/845px-Virgo.svg.png' class='img-thumbnail'>",plural:"virgos"},
  {sign:"Libra",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Libra.svg/1225px-Libra.svg.png' class='img-thumbnail'>",plural:"libras"},
  {sign:"Scorpio",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Scorpio.svg/932px-Scorpio.svg.png' class='img-thumbnail'>",plural:"scorpios"},
  {sign:"Sagittarius",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Sagittarius.svg/1024px-Sagittarius.svg.png' class='img-thumbnail'>",plural:"sagittariuses"},
  {sign:"Capricorn",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Capricorn.svg/1072px-Capricorn.svg.png' class='img-thumbnail'>",plural:"capricorns"},
  {sign:"Aquarius",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Aquarius.svg/1280px-Aquarius.svg.png' class='img-thumbnail'>",plural:"aquariuses"},
  {sign:"Pisces",url:"<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Pisces.svg/823px-Pisces.svg.png' class='img-thumbnail'>",plural:"pisces"}]

d3.csv("https://raw.githubusercontent.com/luisjosemirandag/spotify-luis-insights/master/Spotify%20project/sign_age_top.csv").then(function(data){
  for (i=0;i<12;i++){
    if (data[0].artist_mode_zodiac == artist_sign[i].sign){
      document.getElementById("sign_zodiac").innerHTML = artist_sign[i].url;
      document.getElementById("sign-explanation").innerHTML = artist_sign[i].sign+" artists are the ones that I listen to the most. "+data[0].top_artist_sign+" is my most listened artist with this zodiac sign"
      document.getElementById("artist_sign_px").innerHTML = "<img src='"+data[0].top_artist_pic+"' class='img-thumbnail'>"
    }
  }
  var counter = 0
  elem = $('#age_numbers')
  function myAnimation(){
  counter++
  format_int = d3.format(".0f")
  artist_top_age = data[0].artist_top_age;
  age = d3.select("#age_numbers")
  age.datum(artist_top_age)
  .transition()
    .duration(1000)
    .textTween(function(d) {
        const i = d3.interpolate(0, d);
        return function(t) { return format_int(i(t)); };
      })
  .end();
  }

  $(window).scroll(function(){
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();
    if ((elemBottom <= docViewBottom) && (elemTop >= docViewTop) && counter < 1) {
        myAnimation();
    }
});
});



d3.csv("https://raw.githubusercontent.com/luisjosemirandag/spotify-luis-insights/master/Spotify%20project/top_hour_times.csv").then(function(data){
  data.forEach(function(d){
    d.count = +d.count
  });

  width = 900;
  height = 300;


  margin = ({top: 30, right: 5, bottom: 30, left: 5});
  color = "#80cc86";

  const svg_2 = d3.select('#hour_line_svg')
    .attr("viewBox", [0, 0, width, height]);
  
  x = d3.scaleBand()
    .domain(d3.range(data.length))
    .range([margin.left, width - margin.right])
    .padding(0.1);

  y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.count)]).nice()
    .range([height - margin.bottom, margin.top]);
  
  bars = svg_2.append("g")
        .attr("fill", color)
      .selectAll("rect")
      .data(data)
      .join("rect")
        .attr("x", (d, i) => x(i))
        .attr("y", d => y(d.count))
        .attr("height", d => y(0) - y(d.count))
        .attr("width", x.bandwidth());
  
  bars.append("title")
    .text(function(d) {
        return d.hours + "\n" + d.count + " songs";
    });

  xAxis = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickFormat(i => data[i].hours).tickSizeOuter(0))
    .attr('color','white')
  
  svg_2.append("g")
    .call(xAxis);

});

d3.csv("https://raw.githubusercontent.com/luisjosemirandag/spotify-luis-insights/master/Spotify%20project/song_info.csv").then(function(data){
  song_name = []
  artist_name_sg = []
  song_pic =[]
  for (f = 0; f < 5 ; f ++){
    song_pic.push(data[f].song_picture)
    document.getElementById("info_pic_song_"+f).innerHTML = "<img src="+song_pic[f]+" class='img-thumbnail' width='200' height='200'>";
    song_name.push(data[f].song_name)
    document.getElementById("info_song_"+f).innerHTML = song_name[f];
    artist_name_sg.push(data[f].artist_name)
    document.getElementById("info_art_song_"+f).innerHTML = artist_name_sg[f];
  };
});

d3.csv("https://raw.githubusercontent.com/luisjosemirandag/spotify-luis-insights/master/Spotify%20project/album_duration.csv").then(function(data){
  document.getElementById("album_px").innerHTML = "<img src="+data[0].album_picture+" class='img-thumbnail' width='200' height='200'>";
  document.getElementById("album_name").innerHTML = data[0].album_name;
  document.getElementById("alb_artist").innerHTML = data[0].artist_name;
  
  var counter = 0
  elem_2 = $('#dur_hours')
  function myAnimation_2(){
    counter++
    format_int = d3.format(".0f")
    hours = data[0].duration_hours;
    duration = d3.select("#dur_hours")
    duration.datum(hours)
    .transition()
      .duration(1000)
      .textTween(function(d) {
          const i = d3.interpolate(0, d);
          return function(t) { return format_int(i(t)); };
        })
    .end();
      }

  $(window).scroll(function(){
    var docViewTop_2 = $(window).scrollTop();
    var docViewBottom_2 = docViewTop_2 + $(window).height();

    var elemTop_2 = $(elem_2).offset().top;
    var elemBottom_2 = elemTop_2 + $(elem_2).height();
    if ((elemBottom_2 <= docViewBottom_2) && (elemTop_2 >= docViewTop_2) && counter < 1) {
        myAnimation_2();
    }
});
});


d3.csv("https://raw.githubusercontent.com/luisjosemirandag/spotify-luis-insights/master/Spotify%20project/genres_top.csv").then(function (data){
  i=-1;
  a=-1;
  step();
  function step() {
    const div = d3.select("#genres")
    if (++i >= 4) i = 0
      genre = data[i].genre_name;
      genre_1 = data[i+1].genre_name;
      n = genre.length;
        div.text(genre)
        div.transition()
        .delay(500)
        .duration(500)
        .text(genre_1)
        .on("end",step)
        }
});

d3.csv("https://raw.githubusercontent.com/luisjosemirandag/spotify-luis-insights/master/Spotify%20project/pop_grammy_dance.csv").then(function(data){
  artist_top_name = data[0].top_artist_name
  grammy_nominations = data[0].artist_top_nom
  grammy_wins = data[0].artist_top_wins
  if (grammy_nominations == 0){
    document.getElementById("grammy_text").innerHTML = artist_top_name+", who is my top artist, has never been nominaded to a Grammy Award."
  }
  else if(grammy_wins==0){
    document.getElementById("grammy_text").innerHTML = artist_top_name+", who is my top artist, has been nominated to "+grammy_nominations+" Grammy Awards and has never won any"
    }
  else {
    document.getElementById("grammy_text").innerHTML = artist_top_name+", who is my top artist, has been nominated to "+grammy_nominations+" Grammy Awards and has won "+grammy_wins+" of them"
  }
  var counter = 0
  elem_3 = $('#popularity')
  function myAnimation_3(){
    counter++
  format = d3.format(".0%")
  popularity_artist = data[0].perc_pop_artist/100
  popularity = d3.select("#popularity")
  popularity.datum(popularity_artist)
  .transition()
    .duration(1000)
    .textTween(function(d) {
        const i = d3.interpolate(0, d);
        return function(t) { return format(i(t)); };
      })
  .end();
    };

  $(window).scroll(function(){
    var docViewTop_3 = $(window).scrollTop();
    var docViewBottom_3 = docViewTop_3 + $(window).height();

    var elemTop_3 = $(elem_3).offset().top;
    var elemBottom_3 = elemTop_3 + $(elem_3).height();
    if ((elemBottom_3 <= docViewBottom_3) && (elemTop_3 >= docViewTop_3) && counter < 1) {
        myAnimation_3();
    }
  });
  
  var counter_1 = 0
  elem_4 = $('#dance_perc')
  function myAnimation_4(){
    counter_1++
    dance_percentage = data[0].perc_song_dance/100
    danceability = d3.select("#dance_perc")
    danceability.datum(dance_percentage)
    .transition()
      .duration(1000)
      .textTween(function(d) {
          const i = d3.interpolate(0, d);
          return function(t) { return format(i(t)); };
        })
    .end();
      };
  $(window).scroll(function(){
    var docViewTop_4 = $(window).scrollTop();
    var docViewBottom_4 = docViewTop_4 + $(window).height();

    var elemTop_4 = $(elem_4).offset().top;
    var elemBottom_4 = elemTop_4 + $(elem_4).height();
    if ((elemBottom_4 <= docViewBottom_4) && (elemTop_4 >= docViewTop_4) && counter_1 < 1) {
        myAnimation_4();
    }
  });
});

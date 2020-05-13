/* Function to read the csv and paste it when we call it */
var artist_names = [];
var artist_pictures = [];
var artist_origin = [];
d3.csv("Spotify project/Mejores 5 artistas.csv").then(function(data){
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

d3.csv("Spotify project/sign_age_top.csv").then(function(data){
  for (i=0;i<12;i++){
    if (data[0].artist_mode_zodiac == artist_sign[i].sign){
      document.getElementById("sign_zodiac").innerHTML = artist_sign[i].url;
      document.getElementById("sign-explanation").innerHTML = artist_sign[i].sign+" artists are the ones that I listen to the most. "+data[0].top_artist_sign+" is my most listened artist with this zodiac sign"
      document.getElementById("artist_sign_px").innerHTML = "<img src='"+data[0].top_artist_pic+"' class='img-thumbnail'>"
    }
  artist_top_age = data[0].artist_top_age
  document.getElementById("age_numbers").innerHTML = artist_top_age;
  } 
});

d3.csv("Spotify project/top_hour_times.csv").then(function(data){
  data.forEach(function(d){
    d.count = +d.count
  });

});

var app = angular.module('MyApp',['ngMaterial', 'ngMessages', 'material.svgAssetsCache']);

app.config(['$mdThemingProvider', function($mdThemingProvider) {
  
    $mdThemingProvider.theme('input')
      .primaryPalette('blue')
      .accentPalette('pink')
      .dark();
  }
]);

app.controller('TitleController', function($scope) {
  $scope.title = 'Ask Sparkey !';
});

app.controller('AppCtrl', function($scope) {
  var imagePath = 'img/list/60.jpeg';
});

var spanWidth = jQuery('#search').width();
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
final_transcript = '';
recognition.onresult = function(event) {
    var interim_transcript = '';

    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = final_transcript;
    console.log(final_transcript);
    if(final_transcript.trim().startsWith("Sparky")) {
         value = final_transcript.replace("Sparky",'');
         jQuery("#search").val(value);
         analyse(value);
    }
    final_transcript = ''
}

function analyse(text_input) {
    $.ajax({
       method: "POST",
       url: "/ml/api/v1.0/understand",
       data: JSON.stringify({ text: text_input , query_type: "elastic"}),
       contentType: 'application/json',
       success: function(msg){
          console.log(msg);
          //jQuery('span#result').text(JSON.stringify(msg, null, '\t'));
          jQuery('textarea').text(JSON.stringify(msg, null, '\t'));
          query(msg);
       }
    })
}

function query(query_json) {
    $.ajax({
       method: "POST",
       url: "http://localhost:9200/db/_search?pretty=true",
       data: JSON.stringify(query_json),
       contentType: 'application/json',
       success: function(msg){
          console.log(msg);
          //jQuery('span#result').text(JSON.stringify(msg, null, '\t'));
          jQuery('textarea').text(JSON.stringify(msg["hits"], null, '\t'));
          loadui(msg["hits"])
       }
    })
}

function loadui(content) {
        console.log(content);
        $.get('events_table.html', function (template) {
             console.log(content)
             var str = JSON.stringify(content);
             str = str.replace(/_source/g, 'source');
             str = str.replace(/_source/g, 'source');

             object = JSON.parse(str);
             console.log('*******************')
             console.log(object)
             var html = Mustache.to_html(template, object);
             console.log(html);
             $('#searchresult').html(html);
             $('#myModal').modal('show');
             $('.modal .modal-body').css('overflow-y', 'auto');
             $('.modal .modal-body').css('max-height', $(window).height() * 0.7);
             //$('div#noncriticaltransaction').html(html);
        });

}

recognition.start();

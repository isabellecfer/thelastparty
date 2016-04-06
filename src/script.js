$(document).ready(function () {
    var usuarios = [];

    $('#adicionarDJ').click(function () {
        var toAdd = $('input[name=checkListItem]').val();
        $("#list").append('<div class="item">' + toAdd + '</div>');
        $("input[name=checkListItem], textarea").val("");
        usuarios.push('"' + toAdd + '"');


    });

    //$(document).on('click', '.item', function(){
    //    $(this).remove();
    //});

    $('#gerarLista').click(function () {
        //var musicas = ["spotify:track:0gzpfUezy3wdktjC2SD1FY","spotify:track:0oks4FnzhNp5QPTZtoet7c", "spotify:track:3q6TKWVArb6Hm8nVfsiNDu", "spotify:track:3BMNLPH50kY8HkDuwfa60s"];
        //setupPlayer(musicas);
        document.getElementById('txt').innerHTML = "Wait, this might take several minutes...";
        $.ajax({
            type: "GET",
            //url: "http://localhost:5002/[" + usuarios + "]"
            //url: "playlistmaker.py"

        }).done(function (o) {
            //alert("criando a lista perfeita"),
            //location.href="http://localhost:5002/["+usuarios +"]";
            //envia lista de usuarios lastfm
            //


            var musicas = readJSON("http://localhost:5002/[" + usuarios + "]");
            //inicia o player com a lista de musicas
            setupPlayer(musicas);

        }).fail(function () {
            document.getElementById('txt').innerHTML = "Uh-oh! Try generating the playlist in a few seconds.";
        });

        for (var i = 0; i < usuarios.length; i++) {
            console.log(usuarios[i]);
        }
    });

    function readJSON(url) {
        var dataframe;

        $.ajax({
            url: url,
            type: 'GET',
            async: false,
            dataType: 'json',
            success: function (data) {
                console.log("success ajax!");
                dataframe = data;
            },
            error: function (xhr, status, error) {
                var error = eval("(" + xhr.responseText + ")");
                console.log(error.Message);
            }
        });

        return dataframe;
    }

    function setupPlayer(musicas) {

        var ids = musicas.join("&");
        document.getElementById('txt').innerHTML = "";
        location.href = "player.html?videoIds=" + ids;

    };

});


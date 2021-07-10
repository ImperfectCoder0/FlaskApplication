setInterval((function(){
        var layout = 6;
        $.ajax({
            url: '/login',
            method: 'post',
            data: {layout2: layout},
        });

        if (document.getElementById("Username").value){

        }
    }), 1000);
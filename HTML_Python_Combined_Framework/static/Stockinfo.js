setInterval(function (){
        var Ticker2_ = document.getElementById("Ticker2");
        var Ticker3_ = document.getElementById("Ticker3");
        if (Ticker2_ != null){
            Ticker2_ = document.getElementById("Ticker2").value;
        } else {
            Ticker2_ = ''
        }

        if (Ticker3_ != null){
            Ticker3_ = document.getElementById("Ticker3").value;
        } else {
            Ticker3_ = '';
        }
        $.ajax({
            url: '/stocks/sender',
            method: 'post',
            dataType: 'json',
            data: {Ticker: document.getElementById("Ticker").value, Ticker2: Ticker2_, Ticker3: Ticker3_},
            success: function(data){
                console.log(data);
                document.getElementById("updateable").innerHTML = "Value of stock: " + data['A'];
                document.getElementById("updateable2").innerHTML = "Value of stock: " + data['B'];
                document.getElementById("updateable3").innerHTML = "Value of stock: " + data['C'];
            }
        });
        $.ajax({
            url: '/stocks/image/sender',
            method: 'post',
            dataType: 'json',
            data: {Ticker: document.getElementById("Ticker").value, Ticker2: Ticker2_, Ticker3: Ticker3_},
            success: function(data){
                console.log(data, "Image");
                document.getElementById("img_stock").src = "data:image/png;base64," + data;
            }
//            error: function(error_){
//                console.log(error_)
//
//            }
        })

        }, 10000)
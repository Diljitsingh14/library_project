 $(document).ready(function(){$('#message').css("display", "none")})
        function complete(x)
        {
            var status = document.getElementById('complete'+x).value;
            if(!$('#complete'+x).is(':checked'))
            status = "off"
            
            var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        
            jQuery.post
            (
                '/user/ToDo/update/',
                {'csrfmiddlewaretoken':token,'id':x,'status':status},
                function(data,status)
                {
                    // console.log(data+status)
                    document.getElementById('message').innerHTML = data;
                    $('#message').css('display','block');

                    
                }
            )
        }
        
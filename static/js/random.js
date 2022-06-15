function anim(x) {
    x.classList.toggle("change");
    $('.menu').toggleClass('vp')
    // $('body').css('filter','blur(3)')
}
function anim2(x) {
  x.classList.toggle("change");
  
  // $('body').css('filter','blur(3)')
}

document.addEventListener('DOMContentLoaded',(ev)=>{
    var form = document.getElementById('myform');
    var input = document.getElementById('myfile')
    input.addEventListener('change',(ev)=>{
      console.dir(input.files[0])
      if(input.files[0].type.indexOf('image/') > -1)
      {
        let img = document.getElementById('img')
        img.src = window.URL.createObjectURL(input.files[0])
        img.style.display = "block";
      }
      else  if(input.files[0].type.indexOf('video/') > -1)
      {
        let video = document.getElementById('video')
        video.src = window.URL.createObjectURL(input.files[0])
        img.style.display = "block";

      }
    })
 })
 var myelement = document.getElementById('add_btn')
 var mc = new Hammer(myelement);
  mc.on('panright swiperight tap',function(en)
  {
       $('#exampleModal').modal('show')
       $('#exampleModal').fadeIn(500);
    //    console.log('click')
    }
    )
    $('.card').each(function()
    {
        var mc2 = new Hammer(this) 
        mc2.on('swiperight swipeleft tap',function(en)
        {
            var id = en.target.id
            var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            // console.log(en.type+id)
            // $('body').css('opacity','.3')
            if(en.type == 'swipeleft' || en.type == 'tap')
            {
                // console.log('ready '+csrf_token)
                jQuery.post('/random/open_detail/',{'csrfmiddlewaretoken':csrf_token,'id':id,'type':'post'},function(data,status)
                {
                    // console.log(data+status)
                    var show_case = document.getElementsByClassName('open_detail')[0]
                    show_case.style.display= 'block'
                    show_case.innerHTML = data;
                    $('#get_post').modal('show')

                })
            }
            else if(en.type == 'swiperight')
            {
              jQuery.post('/random/open_detail/',{'csrfmiddlewaretoken':csrf_token,'id':id,'type':'user'},function(data,status)
                {
                  // console.log(data+status)

              var show_case = document.getElementsByClassName('open_detail')[0]
              show_case.style.display= 'block'
              show_case.innerHTML = data;
              $('#post_user_detail').modal('show') 
                
            })
            }

        });
    })
    function selectTag(x)
    {
      var tag = document.getElementById('tag')
      tag.value = x.innerHTML;
    }

    function post_like(x)
    {
      var id = x.id;
      var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
      jQuery.post('/random/post/like/',{'csrfmiddlewaretoken':csrf_token,'id':id},function(data,status)
      {
        console.log(data+status);
      })

    }
    function post_comment(x)
    {
      console.log(x)
    }
    function post_share(x)
    {
      console.log(x)
    }
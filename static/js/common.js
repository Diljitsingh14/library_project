var pdfv=undefined;
var link;
var max_page=1;
var current_page=1;
var bookname;
var bookid;
$('#add_shell').click(function(){$('#addshell').modal('show')})
$('.add_book').click(function()
{
    $('#addbookinfo').modal('show')
    var shellname = $(this).attr('name');
    document.getElementById('shellName').value = shellname;
   

    })
function gotopage()
{
    var getPageNo = document.getElementById('pagenoInp')
    current_page = parseInt(getPageNo.value);
    console.log(current_page)
    if(current_page < max_page)
        openPDF()
    else
        alert("invalid page no.")
    getPageNo.value = current_page;

}
function pageup()
{
    var getPageNo = document.getElementById('pagenoInp')
    current_page = getPageNo.value;
    console.log(current_page)
    current_page++;
    openPDF()
    getPageNo.value = current_page;

}
function pagedown()
{
    var getPageNo = document.getElementById('pagenoInp')
    current_page = getPageNo.value;
    console.log(current_page)
    current_page--;
    openPDF();
    getPageNo.value = current_page;

}
$(".viewpdf").click(function(){
    current_page = parseInt($(this).attr('last-page'))

    link = $(this).attr("href");
    bookname = $(this).attr("target");
    bookid=parseInt($(this).attr("bookid"))
    pdfv = pdfjsLib.getDocument(link)
    openPDF();
    document.getElementById('pagenoInp').value = current_page;
    $("#bookview").modal("show");
    $('#bookname').html(bookname);

})
$(".nailview").each(function()
{
    id = this.id ;
    var data = $(this).attr("data-content");
    frontPageViewer(id,data,1);
     })

function openPDF()
{
    var canvas = document.getElementById("pdfview")
    var context = canvas.getContext("2d",{alpha:false})

    pdfv.promise.then(function(pdf_data)
    {
        max_page = pdf_data._pdfInfo.numPages
        document.getElementById('endpage').innerHTML = max_page;
        
        pdf_data.getPage(current_page).then(function(fetchPage)
        {
            
            let viewport = fetchPage.getViewport({scale:3})
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            let renderContext = {
                canvasContext :context,
                viewport:viewport
            }
            fetchPage.render(renderContext);
        })
    })
}
function frontPageViewer(id,path,i)
{
    i = parseInt(i)
    var pdf = pdfjsLib.getDocument(path);
    var canvas = document.getElementById(id)
    var context = canvas.getContext("2d",{alpha:false})
    pdf.promise.then(function(pdf_data)
    {

        pdf_data.getPage(i).then(function(f_page)
        {
            var viewport = f_page.getViewport({scale:1});
            canvas.height = viewport.height;
            
            canvas.width = viewport.width;
            var renderContext = {
                canvasContext :context,
                viewport:viewport
            }
            f_page.render(renderContext);
        })
    })
    

}
function remember_page()
{
    data = {bookid:bookid,last_page:current_page,total_pages:max_page}
    j_data = JSON.stringify(data)
    $.ajax({url:"/book/remember/",data:{"data":j_data},method:"GET"}).done(function(data)
    {
        if(data == "save")
        {
            notification("your page saved and remember your learning . <br> A knowledge worth is Sharing so keep sharing...","Save successfully")

        }

        else
        {
            notification("Sorry we are unable to remember your reading please <a href='/reader/login/'>login </a> and Retry..","Fail to Save")
        }
        
        })

}
$(document).ready(function()
{
    $('[data-toggle="tooltip"]').tooltip();   
    });

function notification(message,title)
{
    let time = new Date();
    time = time.toLocaleTimeString()
    let header = `
      <i class="fa fa-bell"></i>  <strong class="ml-4 mr-2">${title}</strong>  <i>${time}</i>
    `
    $("#header").html(header)
    $("#message").html(message);
    $("#notification").css("display","block");
}
function shell_settings(x)
{
    var sid = $(x).attr('data-resp')
    // var shell;
    $.getJSON("/library/get_shell_detail/",{id:sid},function(data,status)
    {
        console.log(data.id+status)
        if(status == "success")
        {
            $('#shell_title').html(data.name)
            document.getElementById('sid').value = data.id;
            document.getElementById('shell_name').value = data.name;
            document.getElementById('shell_contrib').checked = data.contrib;
            document.getElementById('shell_privacy').checked = data.privacy;

            
            $('#shell_settings').modal('show')
        }
        })
}
function shell_info(x)
{
    var sid = $(x).attr('data-resp')

    $.getJSON("/library/get_shell_detail/",{id:sid},function(data,status)
    {
        // console.log(data.no_of_books+status)
        if(status == "success")
        {
            $('.t_shell_name').html(data.name)
            $('.t_shell_owner').html(data.create_by)
            $('#t_shell_privacy').html(`${data.privacy}`)
            $('#t_shell_contrib').html(data.contrib)
            $('#t_shell_date').html(data.create_on)
            $('#t_books_inside').html(parseInt(data.no_of_books))
            $('#shell_info').modal('show')
        }
        })
}

function book_like(x)
{
    var bid = $(x).attr('data-resp')
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
    console.log(bid,csrf_token)
    $.ajax({url:"/book/like/",data:{id:bid,csrfmiddlewaretoken:csrf_token},method:"POST"}).done(function(data)
    {
        console.log(data)
        if(data.status == "liked")
        {
            notification("<i class='fa fa-thumbs-up'></i> Hope you are enjoy our services . we will prefer more book like this ",data.status)
            $(x).removeClass("fa-thumbs-o-up")
            $(x).addClass("fa-thumbs-up")
            $("#nofs_likes_"+bid).html(data.likes)
        }
        else if(data.status == "disliked")
        {
            notification("<i class='fa fa-thumbs-o-up'></i> thanks for your opinion . we will prefer best book , for next time . ",data.status)
            $(x).removeClass("fa-thumbs-up")
            $(x).addClass("fa-thumbs-o-up")
            $("#nofs_likes_"+bid).html(data.likes)

        }
        else
        notification("Opps something wents wronge . please try later.....",data.status)

    }
    )
    
}

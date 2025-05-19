
// Post

$(document).ready(function() {

  $('form.ajax_comment').on('submit', function(data){

    $("#comment_button").html('Submitting...');
    var that =$(this),
    url = that.attr('action'),
    type = that.attr('method'),
    data = {};

    that.find('[name]').each(function(index, value){
      var that =$(this),
      name = that.attr('name'),
      value = that.val();
      data[name] = value;
      data['acct_name'] = '{{ acct_result.account_name }}';
    });

    
    $.ajax({
      url: url,
      type: type,
      data: data,
      dataType: "json",

      success: function(data){

        if(data.pass == '1'){
          // $(".acct_post").html('<span>Thanks for your comment!</span>').css("text-align", "center");
          // $("#comment_text").val("");
          $('.ajax_comment')[0].reset();
          window.location.reload();

        }else if(data.empty == '1'){

          $("#text_chg").html("Please say something : ) ");
          $("#comment_text").val("");

        }else{
          $(".acct_post").html(data.error);
          
        }
      }

    });

    return false;
    
  });

});




// like

$(document).ready(function() {

  $('.ajax_like').on('click', function(data){

    var that =$(this),
    the_post_id = that.attr('name'),
    data = {
      csrfmiddlewaretoken: '{{ csrf_token }}',
      post_id: the_post_id,
      like: '1', 
    };

    $.ajax({
      url: '/ajax/like',
      type: 'post',
      data: data,
      dataType: "json",

      success: function(data){

        if(data.pass == '1'){
          // $("#text_chg").html(data.post_id, "yes").css("text-align", "center");

          window.location.reload();

        }else if(data.login == '0'){
          window.location.replace("/signin/") 
        }else{
          $("#text_chg").html(data.error).css("text-align", "center");
        }
      }

    });

    return false;

  });

});






// dislike

$(document).ready(function() {

  $('.ajax_dislike').on('click', function(data){

    var that =$(this),
    the_post_id = that.attr('name'),
    data = {
      csrfmiddlewaretoken: '{{ csrf_token }}',
      post_id: the_post_id,
      like: '0', 
    };

    $.ajax({
      url: '/ajax/like',
      type: 'post',
      data: data,
      dataType: "json",

      success: function(data){

        if(data.pass == '1'){
          window.location.reload();
          
        }else if(data.login == '0'){
          window.location.replace("/signin/") 
        }else{
          $("#text_chg").html(data.error).css("text-align", "center");
        }
      }

    });

    return false;

  });

});




// show reply textarea

  $(document).ready(function() {
      $(".reply").click (function(e) {
        e.preventDefault();
        $(this).parents().next('li').toggle();
      });
  });




// show replies

  $(document).ready(function() {
      $(".reply_toggle").click(function(e){
        e.preventDefault();
        $(this).parents().next().next('#reply_sec').toggle();
      });
  });




// reply

$(document).ready(function() {

  $('form.ajax_reply').on('submit', function(data){

    $("#reply_button").html('Submitting...');
    var that =$(this),
    url = '/ajax/reply',
    type = that.attr('method'),
    data = {};

    that.find('[name]').each(function(index, value){
      var that =$(this),
      name = that.attr('name'),
      value = that.val();
      data[name] = value;
      data['acct_name'] = '{{ acct_result.account_name }}';
    });

    $.ajax({
      url: url,
      type: type,
      data: data,
      dataType: "json",

      success: function(data){

        if(data.pass == '1'){
          $('.ajax_reply')[0].reset();
          window.location.reload();

        }else if(data.empty == '1'){

          $("#reply_err").html("Please say something : ) ");
          $("#reply_text").val("");
          $("#reply_button").html('Submit');

        }else if(data.login == '0'){
          window.location.replace("/signin/") 
        }else{
          $("#reply_err").html(data.error);
          
        }
      }

    });

    return false;

  });

});






// delete comment/reply

$(document).ready(function() {

  $('.ajax_del').on('click', function(data){

    var that =$(this),
    the_post_id = that.attr('name'),
    data = {
      csrfmiddlewaretoken: '{{ csrf_token }}',
      post_id: the_post_id,
      acct_name: '{{ acct_result.account_name }}',
    };

    $.ajax({
      url: '/ajax/delete',
      type: 'post',
      data: data,
      dataType: "json",

      success: function(data){

        if(data.pass == '1'){
          window.location.reload();
          
        }else if(data.login == '0'){
          window.location.replace("/signin/") 
        }else{
          $("#text_chg").html(data.error).css("text-align", "center");
        }
      }

    });

    return false;

  });

});


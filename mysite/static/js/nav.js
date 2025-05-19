      $(document).ready(function() {

          $('.menu-toggle').click(function(e){
            
              var menu = $(this).data('show-dialog');

              $('.' + menu).slideToggle('fast');

          });

          $('.options-menu-horizontal button.close-menu').click(function(){

              $(this).closest('.options-menu-horizontal').slideUp('fast');
          });
      });



      $(document).ready(function() {

          $('.menu-toggle_user').click(function(e){

              var menu = $(this).data('show-dialog');

              $('.' + menu).slideToggle('fast');

          });

          $('.options-menu-horizontal2 button.close-menu').click(function(){

              $(this).closest('.options-menu-horizontal2').slideUp('fast');
          });
      });

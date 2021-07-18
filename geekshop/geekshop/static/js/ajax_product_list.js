$( document ).on( 'click', '.details a', function(event) {
   if (event.target.hasAttribute('href')) {
           $.ajax({
               url: event.target.href,
               success: function (data) {
                   $('.products_list').html(data.result);
               },
           });

           event.preventDefault();
       }
});
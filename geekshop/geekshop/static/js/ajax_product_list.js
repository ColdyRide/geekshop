$( document ).on( 'click', '.details a', function(event) {
   if (event.target.hasAttribute('href')) {
           $.ajax({
               url: event.target.href,
               success: function (data) {
                   $('.details').html(data.result);
                   window.location.reload()
               },
           });

           event.preventDefault();
       }
});
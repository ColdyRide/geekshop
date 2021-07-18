$( document ).on( 'click', '.details a', function(event) {
   if (event.target.hasAttribute('href')) {
           $.ajax({
               url: event.target.href+"/ajax",
               success: function (data) {
                   $('.details').html(data.result);
               },
           });

           event.preventDefault();
       }
});
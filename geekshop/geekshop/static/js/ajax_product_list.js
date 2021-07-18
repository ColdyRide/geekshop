$( document ).on( 'click', '.details a', function(event) {
   if (event.target.hasAttribute('href')) {
            console.log(event.target.href)
           $.ajax({
               success: function (data) {
                   $('.products_list').html(data.result);
               },
           });

           event.preventDefault();
       }
});
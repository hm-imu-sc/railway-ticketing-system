$("#get_schedule").click(function(){
   $('#trains').html('<h1>Loading...</h1>')
   let source = $("#source").val();
   let date = $("#time").val();
   console.log(source);
   console.log(date);
   $.ajax({
      url : ("get_schedule_by_date/"+source+"/"+date),
      method : "GET",
      success : function(data){
         $('#trains').html(data)

         $(".edit_button").click(function() {
               let id = $(this).attr('id');
               if(confirm('Are you sure you want to Update time of Train from '+$("#sourceOf"+id).text()+' to '+$("#destinationOf"+id).text())){
                   $.ajax({
                       url:("update_train_time/"+id+"/"+$("#timeOf"+id).val()),
                       method: "GET",
                       success : function (){
                           console.log('updated')
                       }
                   })
               }
               else
               {
                   console.log('canceled')
               }

         });

         $(".delete_button").click(function() {
               let id = $(this).attr('id');
               if(confirm('Are you sure you want to delete Train from '+$("#sourceOf"+id).text()+' to '+$("#destinationOf"+id).text())){
                   $.ajax({
                       url:("delete_train/"+id),
                       method: "GET",
                       success : function (){
                           $("#dataOf"+id).remove();
                       }
                   })
               }
               else
               {
                   console.log('canceled')
               }

         });
      }
   });
});

// $(document).on("click", ".edit_button", function() {
//       console.log("in edit button");
//       let id = $(this).attr('id');
//       console.log("clicked edit button of train id " + id);
//     }
// );
//
// $(document).on("click", ".delete_button",function() {
//       console.log("in del button");
//       let id = $(this).attr('id');
//       console.log("clicked delete button of train id " + id);
//     }
// );
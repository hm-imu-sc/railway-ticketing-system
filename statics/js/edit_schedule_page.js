$("#get_schedule").click(function(){
   $('#trains').html('')
   let source = $("#source").val();
   let date = $("#time").val();
   console.log(source);
   console.log(date);
   $.ajax({
      url : ("get_schedule_by_date/"+source+"/"+date),
      method : "GET",
      success : function(data){
         data = JSON.parse(data);
         if(data['status']=="OK")
         {
            let trains = data['data']
            let ret = "<table><tr><th>source</th><th>destination</th><th>departure date</th><th>departure time</th><th>action</th></tr>"
            for(let i=0;i<trains.length;i++)
            {
               ret+="<tr><td>"+trains[i]['source']+"</td><td>"+trains[i]['destination']+"</td><td>"+trains[i]['departure_day']+"-"+trains[i]['departure_month']+"-"+trains[i]['departure_year']+"</td><td>"+trains[i]['departure_hour']+":"+trains[i]['departure_min']+":"+trains[i]['departure_sec']+"</td><td><button class = 'edit_button' id='"+trains[i]['id']+"'>"+"Edit"+"</button><button class = 'delete_button' id='"+trains[i]['id']+"'>"+"Delete"+"</button></td></th>"
            }
            ret+="</table>"
            $('#trains').html(ret)

            $(".edit_button").click(function() {
                  console.log("in edit button");
                  let id = $(this).attr('id');
                  console.log("clicked edit button of train id " + id);
            });

            $(".delete_button").click(function() {
                  console.log("in del button");
                  let id = $(this).attr('id');
                  console.log("clicked delete button of train id " + id);
            });

         }

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
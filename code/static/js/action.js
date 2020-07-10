$(document).ready(function() {

  var state_model = false;

  $("#data_source_zone").hide()
  $("#comparison_zone").hide();
  $('#contact').css("display", "none");
  $('#contact_wait').css("display", "none");
  $('#contact_final_success').css("display", "none");
  $('#contact_final_error').css("display", "none");

  $('#btn_resources').click(function() {
    $("#data_source_zone").show();
    $("#comparison_zone").hide();
    event.preventDefault();
  });

  $('#btn_comparison').click(function() {
    $("#data_source_zone").hide();
    $("#comparison_zone").show();
    event.preventDefault();
  });

  $("#model_options").change(function(){
    var opcion = $("input[name='defaultExampleRadios']:checked").val();
    if(opcion === "yes"){
      $("#files").prop( "disabled", false );
      if(state_model){
        $("#pre_mobilenet").prop( "disabled", false );
        $("#pre_resnet50").prop( "disabled", false );
        $("#pre_mobilenetv2").prop( "disabled", false );
        $("#pre_inceptionv3").prop( "disabled", false );
        $("#email_user").prop( "disabled", false );
        $("#button_send").prop( "disabled", false );
      }else{
        $("#pre_mobilenet").prop( "disabled", true );
        $("#pre_resnet50").prop( "disabled", true );
        $("#pre_mobilenetv2").prop( "disabled", true );
        $("#pre_inceptionv3").prop( "disabled", true );
        $("#email_user").prop( "disabled", true );
        $("#button_send").prop( "disabled", true );
      }
    }else{
      $("#files").prop( "disabled", true );
      $("#pre_mobilenet").prop( "disabled", false );
      $("#pre_resnet50").prop( "disabled", false );
      $("#pre_mobilenetv2").prop( "disabled", false );
      $("#pre_inceptionv3").prop( "disabled", false );
      $("#email_user").prop( "disabled", false );
      $("#button_send").prop( "disabled", false );
    }

  });

  $( "#button_send" ).click(function() {
   var opcion_model = $("input[name='defaultExampleRadios']:checked").val();
   var model_location = '/folder/code/static/own_model/model.h5';
   var pretrained_models = [];
   var validation = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
   var validation_email;
   if($('#email_user').val()){
     validation_email = validation.test($('#email_user').val());
   }
   $.each($("input[name='pretrained_models_compare']:checked"), function(){
                   pretrained_models.push($(this).val());
               });
   var cantidad_modelos = pretrained_models.length;
   if (opcion_model == 'yes' && state_model == false){
       swal({
             title: "Oops!",
             text: "You must upload a valid model",
             icon: "error"
           });
   }
   else if(opcion_model == 'yes' && cantidad_modelos < 1){
     swal({
           title: "Oops!",
           text: "You must select at least one pretrained-model",
           icon: "error"
         });
   }
   else if(opcion_model == 'no' && cantidad_modelos < 2){
     swal({
           title: "Oops!",
           text: "You must select more than one pretrained-model",
           icon: "error"
         });
   }
   else if(!$('#email_user').val()){
     swal({
           title: "Oops!",
           text: "Email is empty",
           icon: "error"
         });
   }
   else if(!validation_email){
       swal({
             title: "Oops!",
             text: "Invalid email",
             icon: "error"
           });
   }
   else{
    $('#contactForm_wait').fadeToggle();
    var email_user = $('#email_user').val()
    var json_final = '{ '
    json_final += '"model_option" : '+'"'+opcion_model+'" ,';
    if (opcion_model == 'yes'){
      json_final += '"model_file" : '+'"'+model_location+'" ,';
    }
    json_final += '"pretrained_models" : '+'"'+pretrained_models+'" ,';
    json_final += '"email_user" : '+'"'+email_user+'" ';
    json_final += ' }'

    var obj_data = JSON.parse(json_final);

    $.ajax({
      data : obj_data,
      type : 'POST',
      url : '/comparar'
    })
    .done(function(data) {
      $("#welcom_section").hide();
      $("#option_section").hide();
      $("#comparison_zone").hide();
      $('#contactForm_wait').fadeToggle();
      if (data.error) {
        $('#contactForm_final_error').fadeToggle();
        //swal("Oops!", data.error,"error");
      }else{
        $("#welcom_section").hide();
        $("#option_section").hide();
        $("#comparison_zone").hide();
        $('#contactForm_final_success').fadeToggle();
        //swal("It`s Okey", data.success,"success");
      }
    });


   }

  });

  $("#files").change(function(){
    var form_data = new FormData($('#upload-file')[0]);
    $('#contactForm').fadeToggle();
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
        })
        .done(function(data) {
          $('#contactForm').fadeToggle();
          if (data.error) {
            state_model = false;
            if(!state_model){
              $("#pre_mobilenet").prop( "disabled", true );
              $("#pre_resnet50").prop( "disabled", true );
              $("#pre_mobilenetv2").prop( "disabled", true );
              $("#pre_inceptionv3").prop( "disabled", true );
              $("#email_user").prop( "disabled", true );
              $("#button_send").prop( "disabled", true );
            }
            swal("Oops!", data.error,"error");
          }else{
            state_model = true;
            if(state_model){
              $("#pre_mobilenet").prop( "disabled", false );
              $("#pre_resnet50").prop( "disabled", false );
              $("#pre_mobilenetv2").prop( "disabled", false );
              $("#pre_inceptionv3").prop( "disabled", false );
              $("#email_user").prop( "disabled", false );
              $("#button_send").prop( "disabled", false );
            }
            swal("It's okey", data.success, "success");
          }
        });
  });


});

function sleep(milliseconds) {
 var start = new Date().getTime();
 for (var i = 0; i < 1e7; i++) {
  if ((new Date().getTime() - start) > milliseconds) {
   break;
  }
 }
}

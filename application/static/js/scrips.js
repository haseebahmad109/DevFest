$(document).ready(function(){

     function RadioCheck(){
        if( $('#teacher').is(':checked') ){
            $('#university').hide();
            $('#subjects').show();
            $('#job_title').show()
            $('#subjects').attr('disabled', false);
            $('#university').attr('disabled', true);
            $('#job_title').attr('disabled', false);
        }
        else if($('#student').is(':checked')){
            $('#university').show();
            $('#subjects').hide();
             $('#job_title').hide();
            $('#subjects').attr('disabled', true);
            $('#university').attr('disabled', false);
            $('#job_title').attr('disabled', true);
        }
    }

    RadioCheck();

    $('input[name="user_type"]').change(function(){
        RadioCheck()
    });
});
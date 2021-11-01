$('#checkbox').click(function(){
    if('password' == $('#password').attr('type'))
         $('#password').prop('type', 'text');
    else
         $('#password').prop('type', 'password');
});
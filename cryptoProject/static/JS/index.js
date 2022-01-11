$(function(){

    var body = $('body')

    $('#step2 .button').click(function(){
        // Trigger the file browser dialog
        $(this).parent().find('input').click();
    });

    // Set up events for the file inputs

    var file = null;

    $('#step2').on('change', '#encrypt-input', function(e){

        // Has a file been selected?

        if(e.target.files.length!=1){
            alert('Please select a file to encrypt!');
            return false;
        }

        file = e.target.files[0];
        body.attr('class', 'encrypt');
        if(file.size > 1024*1024){
            alert('Please choose files smaller than 1mb');
            return;
        }
        else{
            $('.fileName.encrypted').append(file.name);
        }
    });

	$('#step2').on('change', '#decrypt-input', function(e){
		if(e.target.files.length!=1){
			alert('Please select a file to decrypt!');
			return false;
		}
		file = e.target.files[0];
		body.attr('class', 'decrypt');
        $('.fileName.decrypted').append(file.name);
	});
    /* Step 3 */

    $('input.button.process').click(function(){
    console.log("test")

        var input = $(this).parent().find('input[type=password]'),
            a = $('#step4 a.download'),
            password = input.val();

        input.val('');

        if(password.length<5){
            alert('Please choose a longer password!');
            return;
        }

        // The HTML5 FileReader object will allow us to read the
        // contents of the  selected file.

        var reader = new FileReader();
        if(body.hasClass('encrypt')){
            // Encrypt the file!
            console.log('in the if');
            reader.onload = function(e){

                // Use the CryptoJS library and the AES cypher to encrypt the
                // contents of the file, held in e.target.result, with the password

                var encrypted = CryptoJS.AES.encrypt(e.target.result, password);
                // The download attribute will cause the contents of the href
                // attribute to be downloaded when clicked. The download attribute
                // also holds the name of the file that is offered for download.
                $('.message.encrypted').append('Encrypted done!');
                a.attr('href', 'data:application/octet-stream,' + encrypted);
                a.attr('download', file.name + '.encrypted');

            };

            // This will encode the contents of the file into a data-uri.
            // It will trigger the onload handler above, with the result

            reader.readAsDataURL(file);
        }
        else {
			// Decrypt it!
			reader.onload = function(e){
				var decrypted = CryptoJS.AES.decrypt(e.target.result, password)
										.toString(CryptoJS.enc.Latin1);
				if(!/^data:/.test(decrypted)){
					alert("Invalid pass phrase or file! Please try again.");
					return false;
				}
				$('.message.decrypted').append('Decrypted done!');
				a.attr('href', decrypted);
				a.attr('download', file.name.replace('.encrypted',''));
			};
			reader.readAsText(file);
		}
    });
$("#submit_button").submit(function(e){
e.preventDefault();

})

});
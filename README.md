# Digital-Shop
---------------------------------------------------------
DigitalShop is a an Ecommerce Website where user can download the file format like audio,video,jpg,png,pdf etc after once complete the payment.

At the time of SignUp we check is the user is already register or not?.when the user fill the Email at that time we send a request to server through AJAX to check the email is already registerd or not.If the email is already registerd the we simply display a message 'Email Already Exists' and disable the SignUp button.

If the Email is not Registerd then the user proceed for the SignUp,and when the user click on SignUp button then at that time we send an OTP to the user email.After the OTP verification we redirect user to the Login page.

Once complete the login we redirect user to the home page where user can download the products after Payment. Payment Gateway:Instamojo/Razorpay.

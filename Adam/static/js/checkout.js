$(document).ready(function () 
{
    $('.paywithRazorpay').click(function (e) { 
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var district = $("[name='district']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (fname =="" || lname =="" || email =="" || phone =="" || address =="" || district =="" || state =="" || country =="" || pincode =="")
        {
            swal("Alert!", "All fields are mandatory!", "error");
            return false;
        }
        else
        {
            $.ajax({
                method : "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    
                    var options = 
                    {
                        "key": "rzp_test_MeYdZlbbReEQgr", // Enter the Key ID generated from the Dashboard
                        //"amount": 1000, //Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "amount":response.total_price * 100,
                        "currency": "INR",
                        "name": "Adam Dich",
                        "description": "Thank You for shopping with us",
                        //"order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (response1){
                            alert(response1.razorpay_payment_id);
                            data = {
                                    "fname": fname,
                                    "lname": lname,
                                    "email": email,
                                    "phone": phone,
                                    "address":address,
                                    "district": district,
                                    "state": state,
                                    "country": country,
                                    "pincode":pincode,
                                    "payment_mode": "Paid by Razorpay",
                                    "payment_id": response1.razorpay_payment_id,
                                    csrfmiddlewaretoken: token
                                
                            }
                            $.ajax({
                                method: "POST",
                                url: "/place-order",
                                data: data,
                                success: function (response2) {
                                    swal("Congragulations!", response2.status, "success").then((value) => 
                                    {
                                        window.location.href = '/my-orders'
                                    });
                                }
                            });
                            
                        },
                        "prefill": {
                            "name": fname+" "+ lname,
                            "email": email,
                            "contact": phone
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
            
            
        }

        
    });
});
$(document).ready(function() {
    $('#idHomePage').show();
    $('#idLookUpStrategies').hide();

    // Your web app's Firebase configuration
    var firebaseConfig = {
        apiKey: "AIzaSyCT7YnB6GQ2rWw9AqgEpB1RpR6Dn1LkvsE",
        authDomain: "stockpredictor-6e833.firebaseapp.com",
        databaseURL: "https://stockpredictor-6e833.firebaseio.com",
        projectId: "stockpredictor-6e833",
        // storageBucket: "",
        messagingSenderId: "309305983170",
        // appId: "1:309305983170:web:20b2f8d5fb699191143b5b"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
});

$('#idLoginButton').click(function() {
    var email = $('#idEmailAddress').val();
    var password = $('#idPassword').val();

    firebase.auth().signInWithEmailAndPassword(email, password)
    .then(function(data) {
      //set display name for user
      //data.user.updateProfile({'displayName': $('#idCreateNewFirstName').val()});
  
      alert('Successfully signed in ' + data.user.displayName);
    }).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
    
        alert (errorMessage);
    });

    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
        //   var first = $('#idCreateNewFirstName').val();
        //   var last = $('#idCreateNewLastName').val()
        //   user.updateProfile({displayName: first + " " + last})
        //   .then(function() {
        //     //display name has been updated properly
        //     //alert (user.displayName);
        //   });
            alert ('hello');
        }
    });
    // firebase.auth().createUserWithEmailAndPassword(email, password)
    // .then(function(data) {
    //   firebase.database().ref('users/' + data.user.uid).set({
    //     firstName: 'Tyler',
    //     lastName: 'Moore',
    //     emailAddress: email
    //   });

    //   //tell user you have been successfully signed up
    //   alert('You have been successfully signed up');

    //   //update their profile page so that their display name will be saved under their account
    //   firebase.auth().onAuthStateChanged(function(user) {
    //     if (user) {
    //       var first = 'Tyler';
    //       var last = 'Moore'
    //       user.updateProfile({displayName: first + " " + last})
    //       .then(function() {
    //         //display name has been updated properly
    //         //alert (user.displayName);
    //       });
    //     }
    //   });

    // }).catch(function(error) {
    //   // Handle Errors here.
    //   var errorCode = error.code;
    //   var errorMessage = error.message;

    //   alert(errorMessage);
    // });
});

$('#idStocksButton').click(function() {
    $('#idHomePage').hide();
    $('#idLookUpStrategies').show();

    $("#idStockFinder").html('');
    $("#idStockFinder").append('<div> Its loading </div>');

    // var includeRussell = 'true';

    // if (includeRussell) {
    //     stockNames = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil', 'Gold', 'Silver']
    // } else {
    //     stockNames = ['Nasdaq', 'S&P 500', 'Dow', 'Natural Gas', 'Crude Oil', 'Gold', 'Silver']
    // }

    stockNames = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow']
    
    // call function to find the stocks
    findStocks('stocks');

    
});

$('#idCommoditiesButton').click(function() {
    $('#idHomePage').hide();
    $('#idLookUpStrategies').show();

    $("#idStockFinder").html('');
    $("#idStockFinder").append('<div> Its loading </div>');

    stockNames = ['Natural Gas', 'Crude Oil', 'Gold', 'Silver']
    
    // call function to find the stocks
    findStocks('commodities');
});

function findStocks(url) {
    $.ajax({
        url: `/${url}`,
        type: 'get',
        dataType: 'json',
        /* data: {
            "includeRussell": includeRussell,
        }, */
        contentType: 'application/json',
        success: function(data) {
        $("#idStockFinder").html('');

        $.each(data, function(index, value) {
            $("#idStockFinder").append(`<div class="container-fluid" style="border-style:solid; border-radius:30px"> \
                <button style="width:100%; background-color:#ECEBEB; border-radius:30px" class="btn" type="button" data-toggle="collapse" data-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}"> \
                <h5> ${stockNames[index]} </h5> \
                <div class="row" style="text-align:left"> \
                    <div class="col-md-2" style="white-space:normal"> <b>Close Price:</b> &nbsp ${value.basicHistoricalData.closePrice.toFixed(2)} </div> \
                    <div class="col-md-2" style="white-space:normal"> <b> Prev Close:</b> &nbsp ${value.basicHistoricalData.prevClose.toFixed(2)} </div> \
                    <div class="col-md-2" style="white-space:normal"> <b> % Change:</b> &nbsp ${value.basicHistoricalData.percentChange} </div> \
                    <div class="col-md-3" style="white-space:normal"> <b> Volume:</b> &nbsp ${value.basicHistoricalData.volume.toFixed(2)}  </div> \
                    <div class="col-md-3" style="white-space:normal"> <b> 10 Day Average Difference:</b> &nbsp ${value.basicHistoricalData.tenDayAverageDifference.toFixed(2)}  </div> \
                </div> \
                <div class="row" style="text-align:left"> \
                    <div class="col-md-2" style="white-space:normal"> <b>Open Price:</b> &nbsp ${value.basicHistoricalData.openPrice.toFixed(2)} </div> \
                    <div class="col-md-2" style="white-space:normal"> <b> Difference:</b> &nbsp ${value.basicHistoricalData.difference.toFixed(2)} </div> \
                    <div class="col-md-2" style="white-space:normal"> <b> % Change:</b> &nbsp ${value.basicHistoricalData.percentChange} </div> \
                    <div class="col-md-3" style="white-space:normal"> <b> 30 Day Change:</b> &nbsp ${value.basicHistoricalData.thirtyDayChange.toFixed(2)} </div> \
                    <div class="col-md-3" style="white-space:normal"> <b> 20 Day Average Difference:</b> &nbsp ${value.basicHistoricalData.twentyDayAverageDifference.toFixed(2)}  </div> \
                </div> \
                </button> \
                <div class="collapse" id="collapse${index}"> \
                    <div class="card card-body" style="background-color:#ECEBEB; border-style:none; border-radius:30px"> \
                        <h6> <b>Fibonacci Numbers</b> </h6> \
                        <div class="row" style="text-align:center"> \
                        <div style="width:10%; margin-left:10%"> \
                            <b> fibLow </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto"> </div> \
                            <p> ${value.fibonacciNumbers.fibLow.toFixed(2)} </p> \
                        </div> \
                        <div style="width:10%"> \
                            <b> fib24 </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto"> </div> \
                            <p> ${value.fibonacciNumbers.fib24.toFixed(2)} </p> \
                        </div> \
                        <div style="width:10%"> \
                            <b> fib38 </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto"> </div> \
                            <p> ${value.fibonacciNumbers.fib38.toFixed(2)} </p> \
                        </div> \
                        <div style="width:10%"> \
                            <b> fib50 </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto"> </div> \
                            <p> ${value.fibonacciNumbers.fib50.toFixed(2)} </p> \
                        </div> \
                        <div style="width:10%"> \
                            <b> fib62 </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto"> </div> \
                            <p> ${value.fibonacciNumbers.fib62.toFixed(2)} </p> \
                        </div> \
                        <div style="width:10%"> \
                            <b> fib78 </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto"> </div> \
                            <p> ${value.fibonacciNumbers.fib78.toFixed(2)} </p> \
                        </div> \
                        <div\ style="width:10%"> \
                            <b> closePrice </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto; background-color:black"> </div> \
                            <p> ${value.fibonacciNumbers.closePrice.toFixed(2)} </p> \
                        </div> \
                        <div style="width:10%"> \
                            <b> fibHigh </b> \
                            <div style="border-style:solid; height:0.15in; width:0.15in; border-radius:100%; margin-left:auto;margin-right:auto"> </div> \
                            <p> ${value.fibonacciNumbers.fibHigh.toFixed(2)} </p> \
                        </div> \
                        </div> \
                        \
                        <br /> \
                        <br /> \
                        \
                        <div class="idStrategies"> \
                            <div class="row"> \
                                <div id="idFirstStrategyDiv${index}" class="col-md-4" style="border-right-style:solid; border-left-style:solid"> \
                                    <h6> <b> First Strategy </b> </h6> \
                                    <br /> \
                                    <p> Buy Signal: ${value.strategies.firstStrategyBuyOrSellSignal} </p> \
                                    <p> Win Percentage in the Last Year: ${value.strategies.firstStrategyWinPercentageForEntireYear} </p> \
                                    <p> Win Percentage in the Last 50 Days: ${value.strategies.firstStrategyWinPercentageForFiftyDays} </p> \
                                    <p> Win Percentage in the Last 15 Days: ${value.strategies.firstStrategyWinPercentageForFifteenDays} </p> \
                                </div> \
                                <div id="idSecondStrategyDiv${index}" class="col-md-4" style="border-right-style:solid; border-left-style:solid"> \
                                    <h6> <b> Second Strategy </b> </h6> \
                                    <br /> \
                                    <p> ${value.strategies.secondStrategyBuyOrSellSignal} </p> \
                                    <button id="idSecondStrategyButton${index}" class="btn btn-outline-light my-2 my-sm-0" type="submit">Test Second Strategy</button> \
                                </div> \
                                <div id="idThirdStrategyDiv${index}" class="col-md-4" style="border-right-style:solid; border-left-style:solid"> \
                                    <h6> <b> Third Strategy </b> </h6> \
                                    <br /> \
                                    <p> ${value.strategies.thirdStrategyPredictedDifference.toFixed(2)} </p> \
                                    <p> ${value.strategies.thirdStrategyPredictedPercentDifference} </p> \
                                    <button id="idThirdStrategyButton${index}" class="btn btn-outline-light my-2 my-sm-0" type="submit">Test Third Strategy</button> \
                                </div> \
                            </div> \
                        </div> \
                    </div> \
                </div> \
            </div> <br />`);
            });
        },
        error: function(request, status, error) {
        $("#idStockFinder").html(error);
        }
    });
}

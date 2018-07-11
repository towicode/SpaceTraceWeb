
var data = {
  spaceSessions: ['test', 'test2']
};

rivets.formatters.prepend = function (value, prepend) {
  return prepend + value
}

rivets.bind(
  document.querySelector('#listings'), // bind to the element with id "candy-shop"
  {
    data: data // add the data object so we can reference it in our template
  });

fetch('/api/sessions')
  .then(response => response.json())
  .then(results => {
    // Here's a list of repos!
    console.log(data)
    data.spaceSessions = results.list;
    //console.log(spaceSessions)
  });

// Will execute myCallback every 0.5 seconds 
var intervalID = window.setInterval(myCallback, 10000);

function myCallback() {
  fetch('/api/sessions')
    .then(response => response.json())
    .then(results => {
      // Here's a list of repos!
      console.log(data)
      data.spaceSessions = results.list;
      //console.log(spaceSessions)
    });
}
var data = {
    title: 'SpaceTraceWeb',
    step: 0,
};

rivets.formatters['='] = function (value, arg) {
    return value == arg;
}

rivets.formatters['>'] = function (value, arg) {
    return value > arg;
}

rivets.formatters['>='] = function (value, arg) {
    return value >= arg;
}

rivets.formatters['<'] = function (value, arg) {
    return value < arg;
}

rivets.formatters['<='] = function (value, arg) {
    return value <= arg;
}

document.getElementById("uploadBtn").onchange = function () {
    document.getElementById("uploadFile").value = this.files[0].name;
};


rivets.bind(
    document.querySelector('#views'), // bind to the element with id "candy-shop"
    {
        data: data // add the data object so we can reference it in our template
    });

var number = document.location.href.substr(document.location.href.lastIndexOf('/') + 1);
console.log(number)

fetch('/api/updates/' + number)
    .then(response => response.json())
    .then(results => {
        // Here's a list of repos!
        console.log(results)
        data.step = results.step;
        //console.log(spaceSessions)
    });



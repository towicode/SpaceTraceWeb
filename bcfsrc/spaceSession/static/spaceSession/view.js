var data = {
    title: 'SpaceTraceWeb',
    step: 0,
    files: {},
    arguments: "",
    img: "<img class='astro_img' id='astro' src='http://via.placeholder.com/350x150' alt=''>"
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

myCallback();

// Will execute myCallback every 0.5 seconds 
var intervalID = window.setInterval(myCallback, 10000);

function myCallback() {
    fetch('/api/updates/' + number)
        .then(response => response.json())
        .then(results => {
            // Here's a list of repos!
            console.log(results)
            data.step = results.step;

            if ('image' in results) {
                console.log("Yes")
                html_string = "<img class='astro_img' id='astro' src='data:image/png;base64, "
                html_string += results.image;
                html_string += "' alt=''>"

                data.img = html_string;
            }
            //console.log(spaceSessions)
        });
}

var submitStepOne = function () {
    fetch('/api/updates/' + number, {
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ files_to_upload: data.files, arguments: data.arguments })
    }).then(res => res.json())
        .then(res => data.step = 2)
        .catch(function (error) {
            console.log(error);
        });
}

var submitStepThree = function () {

    fetch('/api/updates/' + number, {
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: "test-data" })
    }).then(res => res.json())
        .then(res => data.step = 4)
        .catch(function (error) {
            console.log(error);
        });

}




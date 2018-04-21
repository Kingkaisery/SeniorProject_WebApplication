const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const fs = require('fs');
const csvWriter = require('csv-write-stream');

let app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')));

/*app.get('/', function(req,res){
    //res.sendFile(path.join(__dirname)+'/index2.html');
    res.render('index', {
        message: ""
    });
    res.render('index')            
});*/

app.get('/', function(req,res){
    //res.sendFile(path.join(__dirname)+'/index2.html');
    res.render('prediction');                
});

app.get('/result', function(req,res){
    //res.sendFile(path.join(__dirname)+'/index2.html');
    res.render('result', {
        message: req.query.salary
    });              
});

app.post('/', function (req, res) {
    var writer = csvWriter({ headers: ["title", "level","organozation", "joblocation", "education", 
    "experience", "employmentType", "industry", "jobfunction"]});
    writer.pipe(fs.createWriteStream('./prediction/test.csv'));
    writer.write([req.body.jobtitle, req.body.level,req.body.organization, req.body.joblocation, 
    req.body.edu, req.body.exp, req.body.emp, req.body.ind, req.body.jobfunc]);
    writer.end();
    prediction((message) => {
        res.redirect(req.baseUrl + '/result?salary=' + parseInt(message));
    })
});

// app.post('/', function (req, res) {
//     res.render('prediction');
// });

function prediction(callback) {
    var myPythonScriptPath = './prediction/predict.py';

    // Use python shell
    var PythonShell = require('python-shell');
    var pyshell = new PythonShell(myPythonScriptPath);

    pyshell.on('message', function (message) {
        // received a message sent from the Python script (a simple "print" statement)
        callback(message)
    });
}

/*function savedata(req) {
    var writer = csvWriter({ headers: ["title", "organozation", "joblocation"]});
    writer.pipe(fs.createWriteStream('test.csv'));
    writer.write([req.body.jobtitle, req.body.organization, req.body.joblocation]);
    writer.end();
}*/

app.listen(3000);
console.log('Server is running on port 3000...')
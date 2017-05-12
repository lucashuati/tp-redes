var fs = require('fs'),
    http = require('http');

http.createServer(function (req, res) {
  console.log(req);
  fs.readFile('./template.html', function (err,data) {
    if (err) {
      res.writeHead(404);
      res.end("Not Found");
      return;
    }
    res.writeHead(200);
    res.end(data);
  });
  console.log("Entrei");
}).listen(7897);

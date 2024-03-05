(function() {
    console.log('Sanity Check!');

    fetch('/api/v1/all')
    .then(response => response.json())
    .then(data => {
      console.log(data)
      var table =  $('#dtBasicExample').DataTable();
      data.jobs.forEach(item => {
        table.row.add([
          '<a href="/'+item.task_id+'">'+item.task_id+'</a>', 
          item.lr,
          item.momentum,
          item.epochs,
          item.batch_size,
          item.acc,
          item.f1,
          item.time,
          item.status
        ]).draw();
      });
    }).catch(error => console.error('Error:', error));
})();


function getStatus(taskID) {
  fetch(`api/v1/status/${taskID}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    console.log(res)
    var table =  $('#dtBasicExample').DataTable();
    table.row.add([
      '<a href="/'+res.task_id+'">'+res.task_id+'</a>', 
      res.lr,
      res.momentum,
      res.epochs,
      res.batch_size,
      res.acc,
      res.f1,
      res.time,
      res.status
    ]).draw();
  })
  .catch(err => console.log(err));
}

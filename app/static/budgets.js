$(document).ready(function() {

  $('#add-budget').click(function() {

    var budgetData = {
      "title": "New Budget",
      "amount": Math.round(Math.random() * 10000)
    };

    var request = $.ajax({
      url: "/api/v1/budgets/add",
      method: "POST",
      data: budgetData,
      dataType: "json"
    });

    request.done(function(msg) {

      console.log('successfully added a budget: ' + msg.budget.title);

      if(msg.budget != null && msg.budget != undefined) {

        if(msg.budget.id % 2 == 0) {

          $('#budgets-list').append('<li class="budgets-li even"><a href="/budgets/' + msg.budget.id + '">' + msg.budget.title + ': ' + msg.budget.amount + '</a></li>')
        }
        else {

          $('#budgets-list').append('<li class="budgets-li odd"><a href="/budgets/' + msg.budget.id + '">' + msg.budget.title + ': ' + msg.budget.amount + '</a></li>')
        }
      }

      // Reload the page after a successful clear
      // location.reload();
    });

    request.fail(function(jqXHR, textStatus) {

      console.log('Failed to add budget: ' + textStatus);
    });
  });

  $("#remove-budgets").click(function() {

    console.log('remove budgets called');

    var request = $.ajax({
      url: "/api/v1/budgets/clear",
      method: "POST",
      data: {},
      dataType: "json"
    });

    request.done(function(msg) {

      console.log('successfully cleared budgets: ' + msg.message);

      // Reload the page after a successful clear
      location.reload();
    });

    request.fail(function(jqXHR, textStatus) {

      console.log('Failed to clear budgets: ' + textStatus);
    });
  });
});

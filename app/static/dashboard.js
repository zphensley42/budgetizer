var data = {};

var getBudget = function(elem) {

  if(elem == undefined) { return undefined; }

  for(b in data.budgets) {
    if(data.budgets[b].id == elem.val()) {
      return data.budgets[b];
    }
  }

  return undefined;
}

var removeBudget = function(budget_id) {

  if(budget_id == undefined) { return undefined; }

  var index = undefined;
  for(b in data.budgets) {
    if(data.budgets[b].id == budget_id) {
      index = b;
    }
  }

  if(index != undefined) {
    data.budgets.splice(index, 1);
  }
}

var budgetClicked = function(event) {

  $( '.budget-item' ).each(function( index ) {
    $(this).removeClass('active');
  });

  $(this).addClass('active');

  data.selectedIndex = $(this).index;

  if(data.budgets) {

    var budget = getBudget($(this));
    if(budget != undefined) {
      setBudgetContent(budget);
    }
  }
}

var assignBudgetClickListener = function() {

  console.log('assigning click listeners');

  // Add listener to select and listen for a change, then replace content with proper html content for that budget
  $('#sidebar-panel-body .budget-list .budget-item').click(budgetClicked);
}

var initializeBudgets = function() {

  console.log('test');

  var request = $.ajax({
    url: "/api/v1/budgets",
    method: "GET",
    dataType: "json"
  });

  request.done(function(msg) {

    console.log('successfully retrieved budgets: ' + msg.data);
    data.budgets = msg.data;
    setBudgetContent(data.budgets[0]);

    $('#budget-item-1').addClass('active');
  });

  request.fail(function(jqXHR, textStatus) {

    console.log('Failed to retrieve budgets: ' + textStatus);
  });
}

var setBudgetContent = function(budget) {

  $('#budget-content-panel-body').empty();

  for(category in budget.categories) {

    var elementStr =  '<div class="panel panel-info">'
                    + '<div class="panel-heading">'
                    + '<div class="panel-title" id="category-' + budget.categories[category].id + '">'
                    + '<div class="category-title"><span>' + budget.categories[category].title + '</span></div>'
                    + '<div class="category-amount"><span>' + budget.categories[category].amount + '</span></div>'
                    + '</div>'
                    + '</div>'
                    + '<div class="panel-body">';

    elementStr += '<table class="table table-hover">'
                + '<tr><th>ID</th><th>To</th><th>Inflow</th><th>Outflow</th><th>Notes</th><th>Created At</th></tr>'
    for(transId in budget.categories[category].transactions) {

      transaction = budget.categories[category].transactions[transId];
      elementStr += '<tr>'
                  + '<td>' + transaction.id + '</td>'
                  + '<td>' + transaction.to + '</td>'
                  + '<td>' + transaction.inflow + '</td>'
                  + '<td>' + transaction.outflow + '</td>'
                  + '<td>' + transaction.notes + '</td>'
                  + '<td>' + transaction.createdAt + '</td>'
                  + '</tr>';

    }
    elementStr +=   '</table>'
                  + '</div>'
                  + '</div>';

    $('#budget-content-panel-body').append(elementStr);
  }

}

var addBudget = function(budgetData) {

  var request = $.ajax({
    url: "/api/v1/budgets/add",
    method: "POST",
    data: budgetData,
    dataType: "json"
  });

  request.done(function(msg) {

    console.log(msg.message);

    // Add to sidebar
    $('#budget-list').append('<li value="' + msg.budget.id + '" class="budget-item" id="budget-item-' + msg.budget.id + '">' + msg.budget.title + '</li>');

    // Add to data
    data.budgets.push(msg.budget);

    $('#budget-name-input').css('display', 'none');
    $('#budget-name-input').val('');
    $('#budget-done').css('display', 'none');

    assignBudgetClickListener();
  });

  request.fail(function(jqXHR, textStatus) {

    console.log('Failed to add budget: ' + textStatus);

    $('#budget-name-input').css('display', 'none');
    $('#budget-name-input').val('');
    $('#budget-done').css('display', 'none');
  });
}

var deleteBudget = function(id) {

  var request = $.ajax({
    url: "/api/v1/budgets/delete/" + id,
    method: "POST",
    dataType: "json"
  });

  request.done(function(msg) {

    console.log(msg.message);

    if(msg.budget_id != undefined) {

      // Remove from sidebar & data
      $('#budget-item-' + msg.budget_id).remove();
      removeBudget(msg.budget_id);

      // Select the first element in the bar if it exists
      var active = $('.budget-item').first();
      active.addClass('active');

      var budget = getBudget(active);
      console.log(budget);
      if(budget != undefined) {
        setBudgetContent(budget);
      }
    }

    assignBudgetClickListener();
  });

  request.fail(function(jqXHR, textStatus) {

    console.log('Failed to delete budget: ' + textStatus);
  });
}

$(document).ready(function() {

  // Set the initial content (if we have data)
  data.budgets = []
  data.selectedIndex = 0;
  initializeBudgets();

  assignBudgetClickListener();

  $('#budget-new').click(function(event) {

    $('#budget-name-input').css('display', 'inherit');
    $('#budget-done').css('display', 'inherit');
  });

  $('#budget-done').click(function(event) {

    var budgetData = {
      "title": $('#budget-name-input').val()
    };

    addBudget(budgetData);
  });

  $('#budget-delete').click(function(event) {

    console.log($('.budget-item.active').first());

    deleteBudget($('.budget-item.active').first().val());
  });
});

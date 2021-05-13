async function callClick(){
  var currentLocation = window.location;
  let response = await fetch('http://127.0.0.1:8000/click/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("data").innerHTML = answer;
}

async function getUser(id){
  var currentLocation = window.location;
  let response = await fetch('http://127.0.0.1:8000/users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();

  document.getElementById("user").innerHTML = answer.username;
  let getCycle = await fetch('http://127.0.0.1:8000/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];
  document.getElementById("clickPower").innerHTML = cycle['clickPower'];
  document.getElementById("boostPrice").innerHTML = cycle['boostPrice'];
}

async function buyBoost(){
  let response = await fetch('http://127.0.0.1:8000/buyBoost/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("clickPower").innerHTML = answer.clickPower;
  document.getElementById("boostPrice").innerHTML = answer.boostPrice;
  document.getElementById("data").innerHTML = answer.coinsCount;
}

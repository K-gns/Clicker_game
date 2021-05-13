async function callClick(){
  let response = await fetch('click/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("data").innerHTML = answer;
}

async function getUser(id){
  let response = await fetch('users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();

  document.getElementById("user").innerHTML = answer['username'];
  let getCycle = await fetch('cycle/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];
}

async function buyBoost(){
  let response = await fetch('buyBoost/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("clickPower").innerHTML = answer.clickPower;
  document.getElementById("boostPrice").innerHTML = answer.boostPrice;
  document.getElementById("data").innerHTML = answer.coinsCount;
}

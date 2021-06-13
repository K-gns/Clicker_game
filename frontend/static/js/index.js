async function callClick(){
  const coins_counter = document.getElementById('data')
  let coins_value = parseInt(coins_counter.innerText)
  const click_power = document.getElementById('clickPower').innerText
  coins_value += parseInt(click_power)
  document.getElementById("data").innerHTML = coins_value
  set_all_boosts_availability()
}

async function getUser(id){
  let response = await fetch('users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();

  document.getElementById("user").innerHTML = answer['username'];
  let getCycle = await fetch('/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];
  document.getElementById("clickPower").innerHTML = cycle['clickPower'];
  document.getElementById("auto_click_power").innerHTML = cycle['auto_click_power'];
  document.getElementById("level").innerHTML = cycle['level'];

  let boost_request = await fetch('/boosts/' + answer.cycle, {
    method:'GET'
  })
  let boosts = await boost_request.json()
  render_all_boosts(boosts)
  set_all_boosts_availability()
  set_auto_click()
  set_send_coins_interval()
}

function buyBoost(boost_level) {

  const csrftoken = getCookie('csrftoken')

  fetch('buyBoost/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type':'application/json'
    },
    body: JSON.stringify({
      boost_level: boost_level
      })
    }).then(response => {
      if(response.ok){
        return response.json()
      } else {
        return Promise.reject(response)
      }
    }).then(data => {
      document.getElementById("data").innerHTML = data['coinsCount'];
      document.getElementById("clickPower").innerHTML = data['clickPower'];
      document.getElementById("auto_click_power").innerHTML = data['auto_click_power'];
      var boost = document.getElementById(`boost-holder-${data['level']}`)
      boost.querySelector("#boostPower").innerHTML = data['power'];
      boost.querySelector("#boostLevel").innerHTML = data['level'];
      boost.querySelector("#boostPrice").innerHTML = data['price'];
      set_all_boosts_availability()
    })
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== ''){
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if(cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function render_all_boosts(boosts){
  let parent_left = document.getElementById('boost-wrapper-left');
  parent_left.innerHTML = ''
  let parent_right = document.getElementById('boost-wrapper-right');
  parent_right.innerHTML = ''
  boosts.forEach(boost => {
    render_boost(parent, boost)
  })
}

function render_boost(parent, boost){
  const div = document.createElement('div');
  let parent_left = document.getElementById('boost-wrapper-left');
  let parent_right = document.getElementById('boost-wrapper-right');

  div.setAttribute('id', `boost-holder-${boost.level}`)
  if (boost.boost_type == 1) {
    div.setAttribute('class', 'boost-holder-upper-left')
    div.innerHTML = `
    <div class="boost-holder click-boost-holder">
          <input id="buy" type="image" class="boost-bttn" src="/static/img/finger.jpg" onclick="buyBoost(${boost.level})" />
          <div class="boost-desc">
          <p class = "boost-Name"> Click boost  lvl <a id="boostLevel"> ${boost.level} </a></p>
          <p id="power-desc"><a id="boostPower"> ${boost.power} </a> power </p>
          <div id="priceP" style="cursor: pointer;" onclick="buyBoost(${boost.level})"><a id="boostPrice"> ${boost.price} </a>👆 </div>
          </div>
    </div>
    `
    parent_left.appendChild(div)
  } else {
    div.setAttribute('class', 'boost-holder-upper-right')
    div.innerHTML = `
    <div class="boost-holder autoclick-boost-holder">
          <input id="buy" type="image" class="boost-bttn" src="/static/img/clickun.jpg" onclick="buyBoost(${boost.level})"/>
          <div class="boost-desc">
          <p class = "boost-Name"> Auto-click boost lvl <a id="boostLevel"> ${boost.level} </a></p>
          <p id="power-desc"><a id="boostPower"> ${boost.power} </a> power </p>
          <div id="priceP" style="cursor: pointer;" onclick="buyBoost(${boost.level})"><a id="boostPrice"> ${boost.price} </a>👆 </div>
          </div>
    </div>
    `
    parent_right.appendChild(div)
  }



}


function set_all_boosts_availability() {
    const counter = document.getElementById('data');
    const boosts = document.getElementsByClassName('boost-holder');
    for (let boost of boosts) {
        set_boost_availability(counter.innerHTML, boost)
    }
}


function set_boost_availability(coins, boost) {
    const price = boost.querySelector("#boostPrice").innerHTML;
    if (parseInt(price) > parseInt(coins)) {
        var bttn = boost.querySelector("#buy");
        var priceBttn = boost.querySelector("#priceP");
        bttn.setAttribute('disabled', 'true');
        priceBttn.setAttribute('class', 'disabled');
    } else {
        var bttn = boost.querySelector("#buy");
        var priceBttn = boost.querySelector("#priceP");
        bttn.removeAttribute('disabled');
        priceBttn.removeAttribute('class');
    }
}

function set_auto_click() {
    setInterval(function() {
        const coins_counter = document.getElementById('data')
        let coins_value = parseInt(coins_counter.innerText)

        const auto_click_power = document.getElementById('auto_click_power').innerText
        coins_value += parseInt(auto_click_power)
        document.getElementById("data").innerHTML = coins_value;
    }, 1000)
}

function set_send_coins_interval() {
    setInterval(function() {
        const csrftoken = getCookie('csrftoken')
        const coins_counter = document.getElementById('data').innerText;

        fetch('/set_main_cycle/', {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                coins_count: coins_counter,
            })
        }).then(response => {
            if (response.ok) {
                return response.json()
            } else {
                return Promise.reject(response)
            }
        }).then(data => {
            if (data.boosts)
              render_all_boosts(data.boosts)
            set_all_boosts_availability()
            progress = document.getElementById('progress');
            //console.log("На следующий уровень: " + data['toNextLevel']);
            document.getElementById('nextLvl').innerHTML = data['toNextLevel'];
            progress.value = parseInt((data['coins_count'] / data['toNextLevel'])*100);
            document.getElementById("level").innerHTML = data['level'];
        }).catch(err => console.log(err))

    }, 1000)
}

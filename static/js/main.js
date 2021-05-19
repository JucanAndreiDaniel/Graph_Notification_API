function insertParam(key, value) {
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);

    // kvp looks like ['key1=value1', 'key2=value2', ...]
    var kvp = document.location.search.substr(1).split('&');
    let i = 0;

    for (; i < kvp.length; i++) {
        if (kvp[i].startsWith(key + '=')) {
            let pair = kvp[i].split('=');
            pair[1] = value;
            kvp[i] = pair.join('=');
            break;
        }
    }

    if (i >= kvp.length) {
        kvp[kvp.length] = [key, value].join('=');
    }

    // can return this or...
    let params = kvp.join('&');

    // reload page with new params
    document.location.search = params;
}

function changeModalCoin(coin, value) {
    document.getElementsByName("cryptoid")[0].value = coin
    document.getElementsByName("cryptovalue")[0].value = value
}

function changeNotificationSwitchValue(coin, activated, position) {
    document.getElementsByName("cbox")[position].checked = activated
}

function functionDetails(name,current_value,high_1d,low_1d,ath,atl,image){
    document.getElementById("poza").src = image;
    document.getElementsByClassName("custom-msg")[1].innerHTML=name;
    document.getElementsByClassName("custom-msg")[3].innerHTML=current_value;
    document.getElementsByClassName("custom-msg4")[1].innerHTML=high_1d;
    document.getElementsByClassName("custom-msg4")[3].innerHTML=low_1d;
    document.getElementsByClassName("custom-msg4")[5].innerHTML=ath;
    document.getElementsByClassName("custom-msg4")[7].innerHTML=atl;
}

const capitalize = str => str.length
  ? str[0].toUpperCase() +
    str.slice(1).toLowerCase()
  : '';







ssoLogin = {
    lt: "LT-14370370-oMUIGRJ3EXllUbeSJjXxu7qWkLg9mv-LT",
    execution: "e1s1",
    eventId: "submit",
    publicKey: "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAIxtNAM+5q6UZO3PE8g4D5EagaStqdL8+HHczmhR5Iw5Gp8gIla01Tpb+gWFckVHOyPr6ni1ZWpdUhhem5C4CnPTBbKUdO/Ph8tc3g7AkXHPgAi9pDVCfSxVMjg+s1vMiPpb3DtMjUpr/WEvQ2djd6bxwgDKuLiX20dH/1r0XErrAgMBAAECgYBE0lRWbuJxlyqr3fwM+WSvsbTt92qui+pbK2NBfzkqe+YPLJmHsxJ5ipBLWm55g4J5hWqhhA1TBq9wYBWP5JLCHP6HtBMeM1sJp5tH4hhPXQ5oIgVShZf31vHRb461IrOJfXgGrL2+UN8WwA8YhC8ZfGM0tIcBbr5fHfv/4uiJyQJBAMhE0pPZi69euK82KGVh6v800D8bsBfkEi5S5fDXtireby92faLbSlN9ignZTj16jdAtyoXQaXsZrLjSHCKZNY8CQQCzgTXOc3EElMKqrvUpgT45gyvNUxtBxZ8CroILKS9jUREdgzzvePS/vPvrkyQY8boi88q0DGg4kQBo4NOcXX7lAkBt+1XFumf65EL6ffyLSM38X22p6rO3Oxo89Guw61Xwjv1yjFkM0e8skLn5FKziGGa/GBarjDwRTZVMXp7y5T7DAkAieyaH0tsZ4y2Ftff4EhCO4aiPV3B78Oc7j6QBWtb0gAUGo0gYRCbXkgjeVrRvaje0MRp1/ZAjlY77lnxvo/IVAkB81shSeN65Xt+yEeG/Nx2n/iD3sdCRcGBF6r2MLFQEiijcS5XoNOLjyvit90rKir2eDrfqeBfJrunM3BikvPFm",
    credentialEncrypt:true,
    encryptType: 'RSA'
};

ssoLogin.login = function (loginParam, extAttribute) {

    var encryptAccount = encryptData(loginParam.username);
    var encryptPassword = encryptData(loginParam.password);

    return $.ajax({
        url: 'https://hwssov1.59iedu.com/login;SSO_LT_JSESSIONID=4DAF2EA018AE175FC3C22C5A676CDF26',
        type: 'post',
        data: {
            "lt": ssoLogin.lt,
            "execution": ssoLogin.execution,
            "_eventId": ssoLogin.eventId,
            "accountType": loginParam.accountType,
            "account": encryptAccount,
            "password": encryptPassword,
            "credentialEncrypt":ssoLogin.credentialEncrypt,
            "encryptType":ssoLogin.encryptType,
            "extAttribute": extAttribute,
            "captchaTicket": loginParam.captchaTicket,
            "captchaValue":loginParam.captchaValue
        },
        asnyc: false,
        dataType: 'jsonp',
        jsonp: 'ssoCb',
        success: function (data) {
            if (data.code == 603) {
                if (typeof cauth_login_ticket_timer_id != "undefined") {
                    window.clearInterval(cauth_login_ticket_timer_id);
                }
            }

            processLogin(data);
        }
    });
};

function encryptData(data){

    if (window.ActiveXObject){
        // ie
        return b64Encrypt(data);
    }else{
        try {
            var encrypt = new JSEncrypt();
            encrypt.setPublicKey(ssoLogin.publicKey);
            var encryptedData = encrypt.encrypt(data);
            encryptedData = Base64.encode(encryptedData);
            ssoLogin.encryptType = 'RSA';
            return encryptedData;
        } catch (e) {
            return b64Encrypt(data);
        }
    }
}

function b64Encrypt(data){
    try {
        var encryptedData = Base64.encode(data);
        ssoLogin.encryptType = 'B64';
        return encryptedData;
    } catch (e) {
        ssoLogin.credentialEncrypt= false;
        return data;
    }
}

if (typeof cauth_login_ticket_timer_id != "undefined") {
    window.clearInterval(cauth_login_ticket_timer_id);
}

var cauth_login_ticket_timer_id = window.setInterval(function () {
    var loginScript = $('#_login_script');
    if (loginScript.length > 0) {
        loginScript.remove();
    }
    var script = document.createElement("script");
    script.id = '_login_script';
    script.type = "text/javascript";
    script.src = "https://hwssov1.59iedu.com/login;SSO_LT_JSESSIONID=4DAF2EA018AE175FC3C22C5A676CDF26?TARGET=https://jshazj.59iedu.com/web/sso/auth&js&callback=processLogin&_=1660377600414&nocache=" + new Date().getTime();
    document.getElementsByTagName('head')[0].appendChild(script);
}, 60000);




if (!document.getElementById("ssoLogin_script_rsa")){
    var ssoLogin_script_rsa = document.createElement('script')
    ssoLogin_script_rsa.src = 'https://hwssov1.59iedu.com/js/jsencrypt.min.js';
    ssoLogin_script_rsa.id = "ssoLogin_script_rsa";
    document.getElementsByTagName('head')[0].appendChild(ssoLogin_script_rsa);
}

if (!document.getElementById("ssoLogin_script_b64")){
    var ssoLogin_script_b64 = document.createElement('script')
    ssoLogin_script_b64.src = 'https://hwssov1.59iedu.com/js/b64.js';
    ssoLogin_script_b64.id = "ssoLogin_script_b64";
    document.getElementsByTagName('head')[0].appendChild(ssoLogin_script_b64);
}
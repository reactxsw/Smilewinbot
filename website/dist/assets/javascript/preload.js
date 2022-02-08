var images = [];
function preload() {
    for (var i = 0; i < arguments.length; i++) {
        images[i] = new Image();
        images[i].src = preload.arguments[i];
    }
}

preload(
    "https://smilewinbot.web.app/assets/image/background.jpg",
    "https://smilewinbot.web.app/assets/image/smw.jpg",
    "https://smilewinbot.web.app/assets/image/smwcircle.jpg",
    "https://cdn.discordapp.com/avatars/394447088970104833/10499ed48de3c7cf6417afeca6b81596.png?size=1024",
    "https://cdn.discordapp.com/avatars/485027400120532993/2c7be367d5b539e69ab7d2557627bbff.png?size=1024",
    "https://cdn.discordapp.com/avatars/668433997189087232/a_c3990216dc1a64df4837ccdf61a6bf6b.gif?size=1024",
    "https://cdn.discordapp.com/avatars/816276922492780565/939ac897d2133d0073a49da3483b02aa.png?size=1024",
    "https://cdn.discordapp.com/avatars/841386464179912756/346d2178fc33d8793399392da2cd36fd.png?size=1024",
    "https://cdn.discordapp.com/avatars/868101093090017300/fab77d8f08f04bbc1843a1c11c80b3a9.png?size=1024",
)
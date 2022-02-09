var i=0;
var t=["_","S_","Sm_","Smi_","Smil_","Smile_","Smilew_","Smilewi_","Smilewin_","Smilewin🔥"];
function s(){
    if(i>t.length-1||i==0){
        i=0
    }
    document.title=t[i];
    i++;
}
setInterval(s,444);
await user.updateOne(
    { $set: {
        "Lv": 100,"exp": 10000,"mexp": 10000
    }
})

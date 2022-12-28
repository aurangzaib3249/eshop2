let LocalStream;
let RemoteStream;
let PeerConnection;
let servers = {
    iceServers:[
        {
            urls:['stun:stun1.1.google.com:19302', 'stun:stun2.1.google.com:19302']
        }
    ]
}

let init= async ()=>{
    LocalStream=await navigator.mediaDevices.getUserMedia({
        "video":true,
        "audio":false
    })
    document.getElementById('user-1').srcObject=LocalStream;
}
let createOffer= async ()=>{
    
    PeerConnection=new RTCPeerConnection(servers);
    RemoteStream=new MediaStream()
    document.getElementById("user-2").srcObject=RemoteStream
    
   
   
    LocalStream.getTracks().forEach((track) => {
            PeerConnection.addTrack(track,LocalStream)
        })
    
    PeerConnection.ontrack=async (event)=>{
        event.streams[0].getTracks().forEach((track) => {
            RemoteStream.addTrack(track)
        })
    }
    PeerConnection.onicecandidate=async (event)=>{
        if(event.candidate)
        {
            document.getElementById("offer-sdp").value = JSON.stringify(PeerConnection.localDescription)
           
        }
    }
    let offer= await PeerConnection.createOffer()
    await PeerConnection.setLocalDescription(offer)
    document.getElementById("offer-sdp").value=JSON.stringify(offer)
}
let create_ans=async ()=>{
    PeerConnection=new RTCPeerConnection(servers);
    RemoteStream=new MediaStream()
    document.getElementById("user-2").srcObject=RemoteStream
    
   
   
    LocalStream.getTracks().forEach((track) => {
            PeerConnection.addTrack(track,LocalStream)
        })
    
    PeerConnection.ontrack=async (event)=>{
        event.streams[0].getTracks().forEach((track) => {
            RemoteStream.addTrack(track)
        })
    }
    PeerConnection.onicecandidate=async (event)=>{
        if(event.candidate)
        {
           
           
            document.getElementById("answer-sdp").value = JSON.stringify(PeerConnection.localDescription)
        }
    }
    let offer=document.getElementById("offer-sdp").value;
    if (offer)
    {
        offer=JSON.parse(offer)
        await PeerConnection.setRemoteDescription(offer)
        let ans = await PeerConnection.createAnswer()
        await PeerConnection.setLocalDescription(ans)
        document.getElementById("answer-sdp").value=JSON.stringify(ans)
    }
}
let add_answer=async ()=>{
    alert("FD")
    let ans=document.getElementById("answer-sdp").value;
    if (ans){
        ans=JSON.parse(ans)
        if(!PeerConnection.currentRemoteDescription)
        {
            await PeerConnection.setRemoteDescription(ans)
        }
        
    }
    
}
init()
document.getElementById("create-offer").addEventListener("click",createOffer)
document.getElementById("create-answer").addEventListener("click",create_ans)
document.getElementById("add-answer").addEventListener("click",add_answer)

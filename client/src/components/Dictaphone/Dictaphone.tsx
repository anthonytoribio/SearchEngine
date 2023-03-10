import React, { useEffect } from 'react'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'

import { FaMicrophoneAlt } from 'react-icons/fa';

import './Dictaphone.css'

function Dictaphone(props: any) {

    const { transcript, listening, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition()

    if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
        return null
    }

    const handleStart = (event: any) => {
        SpeechRecognition.startListening();
        // console.log("MICROPHONE CLICKED")
        event.preventDefault();
    }

    // useEffect(()=>{
    //     // props.onData(transcript);
    //     console.log(transcript);
    //     //call your increment function here
    // },[transcript]) //and in the array tag the state you want to watch for


    // props.onData(transcript);


    // props.query = "TEST";
    // props.query = transcript;
    return (
        <div>
            {/* <p>Microphone: {listening ? 'on' : 'off'}</p> */}
            <button className='speech-button' onClick={handleStart} style={{paddingBottom: '3px'}}><FaMicrophoneAlt style={{fontSize: '21px'}}/></button>
            {/* <button onClick={SpeechRecognition.stopListening}>Stop</button>
            <button onClick={resetTranscript}>Reset</button> */}
            <p>{transcript}</p>
            {/* <p onChange={testing}>{transcript}</p> */}
        </div>
    )
}
export default Dictaphone
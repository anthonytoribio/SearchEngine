import React, { useEffect } from 'react'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'

import { FaMicrophoneAlt } from 'react-icons/fa';

import './Dictaphone.css'

function Dictaphone(props: any) {

    const { transcript, listening, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition()

    const handleStart = (event: any) => {
        SpeechRecognition.startListening();
        event.preventDefault();
    }

    // This is in charge of making sure voice queries are entered into the search bar
    useEffect(()=>{
        props.onData(transcript);
    },[transcript]) 

    return (
        <div>
            <button className='speech-button' onClick={handleStart} style={{paddingBottom: '3px'}}><FaMicrophoneAlt style={{fontSize: '21px'}}/></button>
        </div>
    )
}
export default Dictaphone
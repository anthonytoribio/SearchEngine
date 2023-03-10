import React from 'react';
import { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import './SearchPage.css';

import SearchBar from '../../components/SearchBar/SearchBar';

import { useLocation } from 'react-router-dom';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

function SearchPage() {  
    let query = useLocation();
    // console.log(query)

    const [data, setdata] = useState('')
      useEffect(() => {
        fetch("/test/help", {method:"POST",
        mode: "cors",
        headers:{
          "Content-Type":"application/json; charset=UTF-8"
        },
        body: JSON.stringify(query)
      }).then((res) =>
        res.json().then(data => {setdata(data)
        // console.log(data)
      })
        )
    
    }, [query])

    var ourData : any;
    var queryTime : number;
    var urlCount : number;

    ourData = data;
    queryTime = ourData.at(-1)
    ourData = ourData.slice(0,-1)
    urlCount = ourData.length;

    // console.log(queryTime)
    // console.log(ourData)

    return (
        <div>
            <a className='to-home-page' href='/'>
              <h1>CONQUEST</h1>
            </a>
            
            <div style={{paddingTop:'3.2vh'}}>
              <SearchBar/>
            </div>

            <div className='result-stats' style={{color: 'white', paddingTop:'0.5%', paddingLeft:'2.6%', fontSize:'0.8rem', fontStyle:'italic'}}>
                {
                    (typeof queryTime === 'undefined') ? (
                        <p>UNDEFINED</p>
                    ) : (
                        <p>Found {urlCount} results in {queryTime.toFixed(3)} seconds</p>
                    )
                }
            </div>


            <div className='all-cards' style={{paddingTop:'15px'}}>
                {
                    (typeof ourData === 'string') ? (
                        <p>UNDEFINED</p>
                    ) : (
                    ourData.map((d:any,i:any) => (
                        
                        <div className='card-container' key={i}>
                            <Card style={{ width: '100%' }} bg='light' text='dark'>
                                <Card.Body>
                                    <Card.Title className='card-title' style={{fontSize:'1.5rem'}}>
                                        <Card.Link className='card-title-link' href={d.url}>{d.title}</Card.Link>
                                    </Card.Title>
                                    <Card.Subtitle className="mb-2 text-muted" style={{fontSize:'0.8rem'}}>
                                        {d.url}
                                    </Card.Subtitle>
                                    <Card.Text style={{fontSize:'1rem'}}>{d.description}</Card.Text>
                                </Card.Body>
                            </Card>    
                        </div>               
                    )))
                }
            </div>
         
        </div>
        
    )

}

export default SearchPage
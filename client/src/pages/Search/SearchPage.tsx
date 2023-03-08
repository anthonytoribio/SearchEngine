import React from 'react';
import { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import './SearchPage.css';

import SearchBar from '../../components/SearchBar/SearchBar';

import { useLocation } from 'react-router-dom';

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
        console.log(data)
      })
        )
    
    }, [query])

    var ourData : any = data;
    console.log(ourData)   

    return (
        <div>
            <a className='to-home-page' href='/'>
              <h1>CONQUEST</h1>
            </a>
            
            <div style={{paddingTop:'3.2vh'}}>
              <SearchBar/>
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
                                        <Card.Link className='card-title-link' href={d.url}>PLACEHOLDER TITLE</Card.Link>
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
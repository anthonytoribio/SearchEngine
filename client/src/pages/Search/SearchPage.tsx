import React from 'react';
import { useState, useEffect } from 'react';
import './SearchPage.css';

import SearchBar from '../../components/SearchBar/SearchBar';

import { useLocation } from 'react-router-dom';

function SearchPage() {

    let query = useLocation();


    const [data, setData] = useState('')
    
    
    useEffect(() => {
        fetch("/test").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])


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

            {/* <div style={{paddingTop:'15vh', color:'white', justifyContent:'center', display:'flex'}}>
                {query.state}
            </div> */}

            {
                ourData.map((d: { url: any; description: any}) => (<p key={d.url}>{d.url}{d.description}</p>))
            }

          

            
            
        </div>  
    )
}

export default SearchPage
import React from 'react';
import { useState, useEffect } from 'react';
import './SearchPage.css';

import SearchBar from '../../components/SearchBar/SearchBar';

import { useLocation } from 'react-router-dom';

function SearchPage() {

    let query = useLocation();

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

            <div style={{paddingTop:'15vh', color:'white', justifyContent:'center', display:'flex'}}>
                {query.state}
            </div>

            {/* <div style={{color: 'white'}}>
                {
                    ourData.map((d: { url: any; description: any}) => (<p key={d.url}>{d.url}{d.description}</p>))
                }
            </div> */}
            
        </div>
        
    )
    {/* <div style={{color:'white'}}>{query.state}</div> */}
}

export default SearchPage
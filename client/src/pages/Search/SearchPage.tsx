import React from 'react';
import './SearchPage.css';

import SearchBar from '../../components/SearchBar/SearchBar';

import { useLocation } from 'react-router-dom';

function SearchPage() {

    let query = useLocation();

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




            
        </div>
        
    )
    {/* <div style={{color:'white'}}>{query.state}</div> */}
}

export default SearchPage
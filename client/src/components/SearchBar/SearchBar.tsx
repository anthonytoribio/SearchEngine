import React from 'react';
import { useState } from 'react';
import './SearchBar.css';

import { FaSearch } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import Dictaphone from '../Dictaphone/Dictaphone';

import doBarrelRoll from '../../pages/Home/HomePage';

function SearchBar() {
    
    const [query, setQuery] = useState('');
    const navigate = useNavigate();
    let doingBarrelRoll = false;

    function timeout(delay: number) {
        return new Promise( res => setTimeout(res, delay) );
    }
    
    async function doBarrelRoll() {
        console.log("DO A BARREL ROLL");
        const pageElement = document.getElementById("page");
        if (pageElement && !doingBarrelRoll) {
            doingBarrelRoll = true;
            pageElement.classList.add("rotated");
            document.body.classList.toggle("hide-scroll");
            await(timeout(2500));
            pageElement.classList.remove("rotated");
            document.body.classList.remove("hide-scroll");
            doingBarrelRoll = false;
        }
    }

    const handleSubmit = (e: { preventDefault: () => void; }) => {
        if (query.toLowerCase() == "do a barrel roll") {
            e.preventDefault();
            doBarrelRoll();
        }
        else {
            e.preventDefault();
            navigate('/search', {state:query})
        }
    };

    // Used by dictaphone to put voice queries into search bar
    const handleQuery = (data: any) => {
        setQuery(data);
    }

    return (
        <form onSubmit={handleSubmit}>
            <div className='input-container'>
                <input type="text" 
                    value={query} 
                    onChange={(q) => setQuery(q.target.value)}
                />
                <div className='buttons-container'>
                    <button className='search-button' style={{paddingBottom: '6px'}}><FaSearch style={{fontSize: '20px'}}/></button>
                    <div className='dictaphone-button'>
                        <Dictaphone onData={handleQuery}/>
                    </div>
                </div>
            </div>       
        </form>
    )
}

export default SearchBar
import React from 'react';
import { useState } from 'react';
import './SearchBar.css';

import { FaSearch } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import Dictaphone from '../Dictaphone/Dictaphone';

function SearchBar() {
    
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e: { preventDefault: () => void; }) => {
        e.preventDefault();
        console.log("search button clicked")
        navigate('/search', {state:query})
    };

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
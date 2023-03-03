import React from 'react';
import { useState } from 'react';
import './SearchBar.css';

import { FaSearch } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

function SearchBar() {
    
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e: { preventDefault: () => void; }) => {
        e.preventDefault();
        navigate('/search', {state:query})
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className='input-container'>
                <input type="text" 
                    value={query} 
                    onChange={(q) => setQuery(q.target.value)}
                />
                <button><FaSearch style={{fontSize: '20px'}}/></button>
                {/* <div>{query}</div> */}
            </div>
        </form>
    )
}

export default SearchBar
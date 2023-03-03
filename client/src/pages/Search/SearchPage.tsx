import React from 'react';
import './SearchPage.css';

import SearchBar from '../../components/SearchBar/SearchBar';

import { useLocation } from 'react-router-dom';

function SearchPage() {

    let query = useLocation();

    return (
        <div>  
            {query.state}
            <SearchBar/>
        </div>
        
    )
}

export default SearchPage
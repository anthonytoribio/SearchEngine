import React from 'react'
import SearchBar from '../../components/SearchBar/SearchBar'
import './HomePage.css'

function HomePage() {

  return (
    <div>
        <div id='page'>
          <h1 className='home-title'>CONQUEST</h1>
          <SearchBar/>
        </div>

    </div>
  )
}

export default HomePage
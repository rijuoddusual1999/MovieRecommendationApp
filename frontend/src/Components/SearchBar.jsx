import React, { useState } from 'react';
import '../CompStyle/SearchBar.css';
import { FaSearch } from 'react-icons/fa';
import SearchResult from './SearchResult';


const SearchBar = () => {
  const [input, setInput] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [recommendedMovies, setRecommendedMovies] = useState(null);

  const fetchResult = (value) => {
    fetch(`http://127.0.0.1:5000/api/similar_names/${value}`)
      .then((response) => response.json())
      .then((json) => {
        setSearchResults(json.similar_names);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setSearchResults([]); 
      });
  };

  const handleChange = (value) => {
    setInput(value);
    if (value.trim() !== '') {
      fetchResult(value);
    } else {
      setSearchResults([]); 
    }
  };


  const handleSearch = () => {
    if (input.trim() !== '') {
      const redirectUrl = `http://127.0.0.1:5000/api/similarity/${input}`;
      

      fetch(redirectUrl)
        .then((response) => response.json())
        .then((json) => {

          setRecommendedMovies(json);
        })
        .catch((error) => {
          console.error('Error fetching search result:', error);
        });
    }
  };


  const handleItemClick = (selectedItem) => {
    setInput(selectedItem);
    setSearchResults([]); 
  };


  return (
    <div className='searchContainer'>
      <div className='bar'>
        <input
          placeholder='Type to Search....'
          value={input}
          onChange={(e) => handleChange(e.target.value)}
        />
        <button type="button" onClick={handleSearch}>
        <FaSearch id="search-icon" />
       </button>
       </div>
      <div className='results'>
      <ul>
          {searchResults?.slice(0, 10).map((resultItem, index) => (
            <li key={index} onClick={() => handleItemClick(resultItem)}>
              {resultItem}
            </li>
          ))}
        </ul>
      </div>
      <div className='posters'>
      {recommendedMovies && (
        <SearchResult recommendedMovies={recommendedMovies} />
      )}
      </div>
    </div>
    
  );
};

export default SearchBar;

import React, { useEffect, useState } from 'react';

import {validateId, validateCountryCode, santifizeInput} from "../utils";
import useDatatFetcher, { fetchPostData } from "../utils/DataFetcher";
import fetchData from "../utils/DataFetcher";

function PlayerResults() {

    const [players, setPlayers] = useState([]);
    const [inputID, setInputID] = useState('');


    useEffect(() => {
        playerFetch(null, 'players');
    }, []);

    const playerFetch = (ep, prop) => {
        fetchData(ep)
        .then(data => {
            const subsetOfPlayers = data[prop].slice(0,10);
            setPlayers(subsetOfPlayers)
            console.log(subsetOfPlayers)
        })
    }

    const handleSearchById = (input) => {

        if (validateId(input)) {
            // do something
            playerFetch(`/v1/players/${input}`, 'player');
        }
    }

    const handleSearchByCountry = (input) => {

        if (validateCountryCode(input)) {
            // do something
            fetchPostData();
        }
    }

 return (
     <div className="player-results">
         <div className="player-results-header">
             <div className="player-results-search">
                 <label>Player id:</label>
                 <input type="text" value={inputID} onChange={(e) => setInputID(e.target.value)}/>
                 <button onClick={(e)=>handleSearchById(inputID)}>Submit</button>
             </div>
             <div className="player-results-search">
                 <label >Player Country Code:</label>
                 <input type=""/>
                 <button onClick={()=>handleSearchByCountry()}>Submit</button>
             </div>
         </div>
         <div className="players-results-section">
             {/* Body of results should go here */}
             {players.map((player) => {
                 return(
                     <div style={{"display": "flex", "gap": "1vh"}}>
                        <div>{player.playerId}</div>
                        <div>{player.birthCountry}</div>
                     </div>
                 )
             })}
         </div>


    </div>
 )
}

export default PlayerResults;

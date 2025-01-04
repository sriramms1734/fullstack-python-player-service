import React, { createContext, useContext, useEffect, useState } from 'react';

import {validateId, validateCountryCode} from "../utils";
import fetchData, { postData } from "../utils/DataFetcher";
import DynamicForm from './DynamicForm';
import { MyContext } from './MyProvider';

function PlayerResults()  {

    const [players, setPlayers] = useState([]);
    const [inputID, setInputID] = useState('');
    const [country, setCountry] = useState('');
    const {data}  = useContext(MyContext);
    const [newObj, setNewObj] = useState({});

    
    useEffect(() => {
        if(data){
            convertKeys(data.formData);
        } 
        playerFetch(null, 'players');
    }, [data]);

    
    const convertKeys = (form)=> {
        for (const key in form) {
            const newKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
            newObj[newKey] = form[key];
        }
    }
    const playerFetch = async (ep, prop) => {
        const data = await fetchData(ep);  
        const subsetOfPlayers = data[prop]?.slice(0,10) || [];
        setPlayers(subsetOfPlayers);
    }

    const handleSearchById = async (input) => {
        if (validateId(input)) {
            // do something
            await playerFetch(`/v1/players/${input}`, 'player');
        }
    }

    const handleSearchByCountry = async (input) => {
        if (validateCountryCode(input)) {
            // do something
            await playerFetch(`/v1/players/${input}`, 'player');
        }
    }

    const generateTeam = async (bodyInput) => {
        try{
        const data = await postData(bodyInput);
       // setPlayers(data);
        } catch (error) {
            console.error('Error fetching data:', error);
          } finally {
          }
    }
    

 return (
    <div>
        {JSON.stringify(newObj, null, 2)}
        <div className="player-results">
            <div className="player-results-header">
                <div className="player-results-search">
                        <label>Player id:</label>
                        <input type="text" value={inputID} onChange={(e) => setInputID(e.target.value)}/>
                        <button onClick={(e)=>handleSearchById(inputID)}>Submit</button>
                </div>
                <div className="player-results-search">
                    <label>Player Country Code:</label>
                    <input type="text" value={country} onChange={(e) => setCountry(e.target.value)}/>
                    <button onClick={()=>handleSearchByCountry(country)}>Submit</button> 
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
            <div className="player-results-generate-team">
                <div>
                    <DynamicForm/>
                    <button onClick={(e)=>generateTeam({"seed_id":"abbotji01","team_size":10})}>Generate Team</button>
                </div> :
                ''
            </div>
        </div>
      </div>
 )
}

export default PlayerResults;

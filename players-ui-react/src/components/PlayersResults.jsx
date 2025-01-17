import React, { useContext, useEffect, useState } from 'react';

import {validateId, validateCountryCode} from "../utils";
import {fetchData, postData} from "../utils/DataFetcher";
import Pagination from './Pagination';
import { MyContext } from '../Provider';

function PlayerResults() {

    const [players, setPlayers] = useState([]);
    const [playerID, setPlayerId] = useState('');
    const [seedId, setSeedId] = useState('');
    const [country, setCountry] = useState('');
    const [pagePlayers, setPagePlayers] = useState([])
    const {fullStore, setFullStore} = useContext(MyContext)
    const [team, setTeam] = useState({})
    const [teamSize, setTeamSize] = useState(10)
    useEffect(() => {
        fetchData('',fullStore.limit, fullStore.offset)
            .then(data => {
                setResults(data.players);
            })
    }, [fullStore.limit, fullStore.offset]);
    const setResults = (players) => {
        setPlayers(players);
        setPagePlayers(players);
    }

    const handleSearchById = async(input) => {
        if (validateId(input)) {
            // do something
            const data = await fetchData(input, fullStore.limit, fullStore.offset)
            setPlayers(data.player.slice(0,10));
        }
    }

    const generateTeamBySeedId = async(endpoint, body) => {
            // do something
            const data = await postData(endpoint, body)
            setTeam(data);
    }

    const handleSearchByCountry = async(input) => {

        if (validateCountryCode(input)) {
            // do something
            const data = await fetchData(input, fullStore.limit, fullStore.offset)
            setResults(data.player);
        }
    }

 return (
     <div className="player-results">
         <div className="player-results-header">
             <div className="player-results-search">
                 <label>Player id:</label>
                 <input type="text" value={playerID} onChange={(e)=> setPlayerId(e.target.value)}/>
                 <button onClick={(e)=>handleSearchById(playerID)}>Submit</button>
             </div>
             <div className="player-results-search">
                 <label >Player Country Code:</label>
                 <input type="text" value={country} onChange={(e)=> setCountry(e.target.value)}/>
                 <button onClick={(e)=>handleSearchByCountry(`player_country/${country}`)}>Submit</button>
             </div>
         </div>
         <div className="players-results-section">
             {/* Body of results should go here */}
             <div>
                <li>
                    {pagePlayers.map((person) => (
                        <React.Fragment>
                            <span style={{display: "flex"}}>
                            <ul>{person.playerId}</ul> 
                            <ul>{person.birthCountry}</ul>
                            </span>
                        </React.Fragment>
                    ))}
                </li>
                    <Pagination
                        items={players}
                        pageLimit={fullStore.limit}
                        setPageItems={setPagePlayers}
                    />
            </div>
         </div>
         <div className="player-results-llm">
             <div>
                 <label>Seed ID:</label>
                 <input type="text" value={seedId} onChange={(e)=> setSeedId(e.target.value)}/>
                 <label>Team Size:</label>
                 <input type="text" value={teamSize} onChange={(e)=> setTeamSize(e.target.value)}/>
                 <button onClick={()=>generateTeamBySeedId('/v1/team/generate', {seed_id: seedId, team_size: teamSize})}>Generate Team</button>
             </div>
         </div>
         <div><pre>{JSON.stringify(team, null, 2) }</pre></div>



    </div>
 )
}

export default PlayerResults;

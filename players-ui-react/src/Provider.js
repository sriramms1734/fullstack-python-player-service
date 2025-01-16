import { useState, createContext } from "react";

const MyContext = createContext();

const MyProvider = ({children}) => {
    const [fullStore, setFullStore] = useState({limit: 10, offset: 0});
    return (
        <MyContext.Provider value={{fullStore, setFullStore}}>
            {children}
        </MyContext.Provider>
    )
}

export {MyProvider, MyContext}

import React, { createContext, useState, useContext } from 'react';
import PlayerMain from './PlayerMain';
const MyContext = createContext();

const MyProvider = ({ children }) => {
  const [data, setData] = useState({});

  return (
    <MyContext.Provider value={{ data, setData }}>
        {children}
    </MyContext.Provider>
  );
};
export { MyContext, MyProvider};
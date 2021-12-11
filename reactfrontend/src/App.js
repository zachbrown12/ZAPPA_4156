import React, { useState, useEffect } from 'react';
import LandingPage from './components/landingPage';
import Login from './components/login';
import './App.css';
import { useCookies } from 'react-cookie';
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {

  const [token, setToken, deleteToken] = useCookies(['mr-token']);

  useEffect( () => {
    if(!token['mr-token']) window.location.href = '/';
  }, [token])


  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route exact path={"/"} component={Login} />
          <Route exact path={"/games"} component={LandingPage} />
        </Routes>
      </BrowserRouter>
            </div>
  );
}



export default App;

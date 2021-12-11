import React, { useState, useEffect } from "react";
import LandingPage from "./components/landingPage";
import Login from "./components/login";
import Signup from "./components/signup";
import "./App.css";
import { useCookies } from "react-cookie";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route
            path={"/"}
            element={<Signup loggedIn={loggedIn} setLoggedIn={setLoggedIn} />}
          />
          <Route
            path={"/login"}
            element={<Login loggedIn={loggedIn} setLoggedIn={setLoggedIn} />}
          />
          <Route
            path={"/signup"}
            element={<Signup loggedIn={loggedIn} setLoggedIn={setLoggedIn} />}
          />
          <Route
            path={"/games"}
            element={<LandingPage loggedIn={loggedIn} />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

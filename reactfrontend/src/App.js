import React, { useState, useEffect } from "react";
import LandingPage from "./components/landingPage";
import Login from "./components/login";
import Signup from "./components/signup";
import "./App.css";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("");

  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route
            path={"/"}
            element={
              <Signup
                loggedIn={loggedIn}
                setLoggedIn={setLoggedIn}
                username={username}
                setUsername={setUsername}
              />
            }
          />
          <Route
            path={"/login"}
            element={
              <Login
                loggedIn={loggedIn}
                setLoggedIn={setLoggedIn}
                username={username}
                setUsername={setUsername}
              />
            }
          />
          <Route
            path={"/signup"}
            element={
              <Signup
                loggedIn={loggedIn}
                setLoggedIn={setLoggedIn}
                username={username}
                setUsername={setUsername}
              />
            }
          />
          <Route
            path={"/games"}
            element={
              <LandingPage
                loggedIn={loggedIn}
                setLoggedIn={setLoggedIn}
                username={username}
                setUsername={setUsername}
              />
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

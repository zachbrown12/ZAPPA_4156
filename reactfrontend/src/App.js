import React, { useState } from "react";
import LandingPage from "./components/landingPage";
import Login from "./components/login";
import Signup from "./components/signup";
import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import getCookie from "./helpers/csrfHelper";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const csrftoken = getCookie("csrftoken");

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
                csrftoken={csrftoken}
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
                csrftoken={csrftoken}
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

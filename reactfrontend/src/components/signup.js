import React, { useState } from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel, Button } from "@mui/material";

export default function Signup(props) {
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [existingUser, setExistingUser] = useState(false);

  const switchToLogin = () => {
    setExistingUser(true);
  };

  const onSubmit = (e) => {
    e.preventDefault();

    const user = {
      username: props.username,
      password1: password1,
      password2: password2,
    };

    axios
      .post(`/users/register/`, JSON.stringify(user), {
        headers: { "Content-Type": "application/json" },
      })
      .then((res) => {
        console.log(res.status);
        window.location.replace("http://localhost:3000/games");
      })
      .catch((err) => console.log(err.response.data)); // TODO: Add better error
  };

  return (
    <div>
      {!props.loggedIn ? (
        !existingUser ? (
          <div>
            <h1 style={{ margin: "20px" }}>Signup User</h1>
            <FormControl
              required={true}
              variant="standard"
              color="primary"
              margin="normal"
              style={{ margin: "20px" }}
            >
              <InputLabel htmlFor="username">Username</InputLabel>
              <Input
                name="username"
                type="username"
                value={props.username}
                required
                onChange={(e) => props.setUsername(e.target.value)}
              />{" "}
            </FormControl>
            <br></br>
            <FormControl
              required={true}
              variant="standard"
              color="primary"
              margin="normal"
              style={{ margin: "20px" }}
            >
              <InputLabel htmlFor="password">Password</InputLabel> <br />
              <Input
                name="password"
                type="password"
                value={password1}
                required
                onChange={(e) => setPassword1(e.target.value)}
              />{" "}
            </FormControl>
            <br></br>
            <FormControl
              required={true}
              variant="standard"
              color="primary"
              margin="normal"
              style={{ margin: "20px" }}
            >
              <InputLabel htmlFor="password">Confirm Password</InputLabel>{" "}
              <br />
              <Input
                name="password"
                type="password"
                value={password2}
                required
                onChange={(e) => setPassword2(e.target.value)}
              />{" "}
            </FormControl>
            <br></br>
            <Button onClick={onSubmit} style={{ margin: "20px" }}>
              Sign up
            </Button>
            <br></br>
            <Button
              variant="contained"
              onClick={switchToLogin}
              stype={{ margin: "20px" }}
            >
              Log In Existing User
            </Button>
          </div>
        ) : (
          <Navigate to="/login" />
        )
      ) : (
        <Navigate to="/games" />
      )}
    </div>
  );
}
